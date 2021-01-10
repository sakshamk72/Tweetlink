from django.db import models
from django.utils import timezone

class Tweet(models.Model):
    tweet_id = models.CharField(max_length=100)
    date     = models.DateTimeField(default=timezone.now)
    author   = models.CharField(max_length=100)
    tweet_id = models.CharField(max_length=100)
    domain   = models.CharField(max_length=100)