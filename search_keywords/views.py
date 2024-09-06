import json
import os
from celery import shared_task
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from .forms import *
from .models import Video
import boto3
import subprocess
from django.conf import settings
from .models import Video
from botocore.exceptions import ClientError
from celery.result import AsyncResult
# Initialize DynamoDB and S3 clients

# Create your views here.
def sub(request):
    form = VideoForm()
    if request.method == "POST" and 'search' not in request.POST:
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = request.FILES.get('video')
                if request.user.is_authenticated:
                    username=request.user.username
                else:
                    username="AnonymousUser"
                name=file.name
                content=file.read()
                async_result = upload_video.delay(username,name,content)  # Pass only necessary data
                
                id = async_result.task_id
                return render(request, "index.html", {"form": form, "id": id})

            except Exception as e:
                print(e)
                return redirect("/visub/")
        else:
            print(form.errors)
            try:
                video = Video.objects.get(username=request.user)
                url = video.video.url
                return render(request, "index.html", {"form": form, "file": url})
            except:
                return render(request, "index.html", {"form": form})

    elif request.method == "POST" and 'search' in request.POST:
        keyword = request.POST["search"]
        video = Video.objects.get(username=request.user)
        url = video.video.url
        if request.user.is_authenticated:
            username=request.user.username
        else:
            username="AnonymousUser"
        async_result = search_keyword_in_subtitles.delay(username, keyword)
        id = async_result.task_id
        return render(request, "index.html", {"form": form, "download_id": id, "file":url,"value":keyword})
    return render(request, "index.html", {"form": form})


def check_status(request, task_id):
    result = AsyncResult(task_id)
    if result.ready():
        video_url = result.result  # Get the video URL from the result
        return JsonResponse({'status': True, 'video_url': video_url})
    else:
        return JsonResponse({'status': False})
    
@shared_task
def upload_video(user_id, name,content): 
    from django.core.files.base import ContentFile
    file = ContentFile(content=content,name=name)
    video, created = Video.objects.update_or_create(username=user_id, defaults={'video': file})
    process_video_and_store_subtitle.delay(user_id)
    return video.video.url


@shared_task
def process_video_and_store_subtitle(user):
    s3_client = boto3.client('s3',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,region_name=settings.AWS_S3_REGION_NAME)

    dynamodb_client = boto3.resource('dynamodb',aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,region_name=settings.AWS_S3_REGION_NAME)

    # Get the video object from the database
    video = Video.objects.get(username=user)
    
    # Define S3 bucket and video key
    bucket_name = "project-video"
    s3_key = video.video.name
    local_video_path = s3_key.split("/")[-1]
    username=user
    try:
        s3_client.download_file(bucket_name,s3_key,local_video_path)
        # Run ccextractor to extract subtitles
        subtitle_path = (local_video_path.split('.')[0])+".srt"
        try:
            ccextractor_command = ['CCExtractor_win_portable\ccextractorwinfull.exe',local_video_path,'-o', subtitle_path]
            subprocess.run(ccextractor_command, check=True)
        except:
            subtitle_content=" "
        
        # Read extracted subtitles
        try:
            with open(subtitle_path,'r') as subtitle_file:
                subtitle_content = subtitle_file.read()
        except:
            subtitle_content=" "
        subtitle_contents=str(subtitle_content)
        # Store the subtitles in DynamoDB
        if subtitle_contents=="":
            subtitle_contents=" "
        table = dynamodb_client.Table('video_subtitle')

        table.put_item(
            Item={
                'title': username,  # Partition key (title of the video)
                'subtitles': subtitle_contents  # Subtitles extracted from the video
            }
        )
        return None
    except Exception as e:
        print(e)

@shared_task
def search_keyword_in_subtitles(user, keyword):
    dynamodb_client = boto3.client('dynamodb',aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,region_name=settings.AWS_S3_REGION_NAME)
    username=user
    # Retrieve the subtitles from DynamoDB
    response = dynamodb_client.get_item(
        TableName='video_subtitle',
        Key={
            'title':{'S': username}
        }
    )
    list_response=response['Item']['subtitles']["S"].split("\n")
    time_subtitle={}
    i=0
    block=[]
    while i<len(list_response)-1:
        if list_response[i]=='':
            timestamp=block[1]
            Subtitle=block[2:]
            start_time, end_time=timestamp.split("-->")
            start_time=start_time.split(",")[0]
            time_subtitle[start_time]=Subtitle
            block=[]
            i+=1
        else:
            block.append(list_response[i])
            i+=1
    found=False
    time=[]
    for key, value in time_subtitle.items():
        for j in value:
            if keyword.lower() in j.lower():
                time.append(key)
                found=True
                break
    if found==False:
        time=[]
    return time


def check_download_status(request, task_id):
    result = AsyncResult(task_id)
    if result.ready():
        time = result.result  # Get the video URL from the result
        return JsonResponse({'status': True, 'time': json.dumps(time)})
    else:
        return JsonResponse({'status': False})