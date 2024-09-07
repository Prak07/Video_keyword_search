from django.shortcuts import render

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from .models import *
from .forms import *
from django.core.mail import send_mail
import uuid
from django.conf import settings

def Guest(request):
    return redirect("/visub/")
def login(request):
    if request.user.is_authenticated!=True:
        form=LoginForm()
        if request.method=="POST":
            form=LoginForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data["username"]
                password=form.cleaned_data["password"]
                try:
                    user=Profile.objects.get(username=username)
                    if user is not None:
                        if user.check_password(password):
                                auth.login(request, user)
                                return redirect("/visub/")
                        else:
                                messages.error(request, "Invalid password")
                                return redirect("/login/")
                    else:
                            messages.error(request, "Invalid email")
                            return redirect("/login/")
                except:
                    try:
                        user=Profile.objects.get(email=username)
                        if user is not None:
                            if user.check_password(password):
                                auth.login(request, user)
                                return redirect("/visub/")
                            else:
                                messages.error(request, "Invalid password")
                                return redirect("/login/")
                        else:
                            messages.error(request, "Invalid email")
                            return redirect("/login/")
                    except:
                        messages.error(request, "Invalid credentials")
                        return redirect("/login/")
            else:
                messages.error(request,"Wrong input")
                return redirect("/login/")
        return render(request,"login.html",{"form":form})
    else:
        return redirect("/visub/")
    
def signup(request):
    if request.user.is_authenticated!=True:
        form=SignupForm()
        if request.method=='POST':
            form=SignupForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                email=form.cleaned_data['email']
                password=form.cleaned_data['password']
                confirm_password=form.cleaned_data['confirm_password']
                if password==confirm_password:
                    if Profile.objects.filter(username=username).exists():
                        messages.error(request,"Username Already Taken")
                        return redirect("/signup/")
                    elif Profile.objects.filter(email=email).exists():
                        messages.error(request,"Email Already Taken")
                        return redirect("/signup/")        
                    else:    
                        user=Profile.objects.create_user(username=username,email=email,password=password)
                        Profile.save
                        messages.success(request,"Account created now login to continue")
                        return redirect("/login/")
                else:
                    messages.error(request,"Passwords doesn't match")
                    return redirect("/signup/")
            else:
                messages.error(request,"Wrong input")
                return redirect("/signup/")
        return render(request,"signup.html",{"form":form})
    else:
        return redirect("/visub/")
def forgot_pass(request):
    if request.user.is_authenticated!=True:
        form=EmailForm()
        if request.method=="POST":
            form=EmailForm(request.POST)
            if form.is_valid():
                email=form.cleaned_data["email"]
                try:
                    user = Profile.objects.get(email=email)
                    if user is not None:
                        token=send_forgot_email(email)
                        try :
                            pass_user=ForgotPass.objects.get(user=user)
                            pass_user.forgot_pass_token=token
                            pass_user.save()
                        except:
                            ForgotPass.objects.update_or_create(user=user,forgot_pass_token=token)
                        messages.success(request,"Email sent Successfully")
                        return redirect("/forgot_pass/")
                except Exception:
                    messages.error(request,"This email is not registerd")
                    return redirect("/forgot_pass/")
            else:
                messages.error(request,"Wrong input")
                return redirect("/forgot_pass/")
            
        return render(request,"forgot_pass.html",{"form":form})
    else:
        return redirect("/visub/")

def new_pass(request,token):
    if request.user.is_authenticated!=True:
        form=NewPassForm()
        if request.method=="POST":
            form=NewPassForm(request.POST)
            try:
                user_pass=ForgotPass.objects.get(forgot_pass_token=token)
                if form.is_valid():
                    new_password=form.cleaned_data['new_password']
                    confirm_password=form.cleaned_data['confirm_password']
                    if new_password==confirm_password:
                        user_pass.user.set_password(new_password)
                        user_pass.user.save()
                        messages.success(request,"Password Updated Successfully")
                        user_pass.forgot_pass_token=None
                        user_pass.save()
                        return redirect("/login/")
                    else:
                        messages.error(request,"Passwords doesn't match")
                        return redirect("/new_pass/")
            except Exception:

                return HttpResponse("<h2>This is not a Valid link<h2>")
        return render(request,"new_pass.html",{"form":form})
    else:
        return redirect("/visub/")
    
def logout(request):
    auth.logout(request)
    messages.error(request,"You are logged out")
    return redirect("/login/")

def send_forgot_email(email):
    token=str(uuid.uuid4())
    subject= "Your change password link is here"
    message= f"Hi, click on the link to reset your password http://127.0.0.1:8000/new_pass/{token} And This link is valid for only one time use"
    sender=settings.EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,sender,recipient)
    return token

