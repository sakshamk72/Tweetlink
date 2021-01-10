from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.db.models import Count
from .models import Tweet
from datetime import datetime
import tweepy
from tweepy import OAuthHandler
import sys
import requests
import tldextract  # Extracts domains from a URL

def index(request,*args,**kwargs):
    if 'access_token' not in request.session:
        return render(request,"index.html",{})
    else:
        return redirect('feed')

def feed(request,*args,**kwargs):                                  #feed route

    if 'access_token' not in request.session:
        return redirect('index')

    auth = OAuthHandler(consumer_key, consumer_secret)
    access_token = request.session['access_token']
    access_token_secret = request.session['access_token_secret']

    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth)
    request.session['user']=api.me().name
    username=api.me().screen_name
    user = api.get_user(screen_name=username)
    Tweet.objects.all().delete()  #clear database
    
    get_tweets(username)    #difined at the end
    arr = Tweet.objects.all().order_by('date').reverse()
    
    html = []
    for tweet in arr:
        #getting Tweet Embeds for the tweets to show
        URL="https://publish.twitter.com/oembed?url=https://twitter.com/" + tweet.author + "/status/" + str(tweet.tweet_id)
        r = requests.get(url = URL)
        json_data = r.json()
        html.append(json_data["html"])
    
    #Getting the most trending user and the domain
    trending_username =""
    trending_domain   =""
    trending_fullname =""
    trending_url      =""
    if(len(html)!=0):
        trending_username=Tweet.objects.values('author').annotate(count=Count('tweet_id')).order_by('count').reverse()[:1][0]['author']
        trending_user = api.get_user(screen_name=trending_username)
        trending_fullname=trending_user.name
        trending_url=trending_user.profile_image_url
        trending_domain=Tweet.objects.values('domain').annotate(count=Count('tweet_id')).order_by('count').reverse()[:1][0]['domain']

    followers=user.followers_count
    following=user.friends_count
    name=user.name
    image_url=user.profile_image_url
    profile_url="twitter.com/" + username
    obj = {
        'data'              :html,
        'screen_name'       :username,
        'followers'         :followers,
        'following'         :following,
        'image_url'         :image_url,
        'profile_url'       :profile_url,
        'name'              :name,
        'trending_username' :trending_username,
        'trending_fullname' :trending_fullname,
        'trending_url'      :trending_url,
        'trending_domain'   :trending_domain
    }
    return render(request,"feed.html",obj)


# Function to extract tweets
def get_tweets(username):
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # Access to user's access key and access secret 
    auth.set_access_token(access_key, access_secret)
    # Calling api 
    api = tweepy.API(auth)
    connections = []
    connections.append(username)
    for friend in api.friends(username):
        connections.append(friend.screen_name)   #Getting the following users
    
    for friend in connections:
        i=0
        tweets = api.user_timeline(screen_name=friend) #retreiving tweets from twitter api
        for tweet in tweets:
            i=i+1
            if(i==30): #limiting the number of tweets per user
                break
            if((datetime.now() - tweet.created_at).days>7): #if a tweet is more than a week old
                break
            urls=tweet.entities["urls"]
            domain = ""
            flag=0
            for url in urls:
                info =tldextract.extract(url['expanded_url'])  #extracting domains
                if(info.domain!="twitter"):
                    domain=info.domain
                    flag=1
                    break
            if(flag==0):
                continue
            temp_tweet = Tweet(           #updating the database
                tweet_id = tweet.id,
                date     = tweet.created_at,
                domain   = domain,
                author   = friend
            )
            temp_tweet.save()


def auth(request):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret,'https://tweetlinks18.herokuapp.com/callback')

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    response = HttpResponseRedirect(redirect_url)
    request.session['request_token']=auth.request_token

    return response

def callback(request):
    verifier = request.GET.get('oauth_verifier')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    token = request.session['request_token']
    request.session.delete('request_token')
    auth.request_token = token

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    request.session['access_token']=auth.access_token
    request.session['access_token_secret']=auth.access_token_secret

    return HttpResponseRedirect(reverse('feed'))

consumer_key = "uzVPzAYt6bJZRaaXCGGkYStHT"
consumer_secret = "145Pdn8YRkkQobmHBEgIB4Afu8twsVnUBWXXjHszlU4xdumM8J"
access_key = "1311740936037101568-GsTx8wA75pFGHrqNsAFmpGS7pVQciy"
access_secret = "p6KdsMX9fljWpdPSrqh0xMwez4neH4BkpDJkY1SYGzbBl"
