from youtube_keywords_search.celery import app
print(app.conf.broker_url)