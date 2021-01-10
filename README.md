# TweetLinks

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

TweetLinks is a webbased app which aims to collect tweets which contains links from user stream i.e user tweets and user's friends tweet of the past 7 days. Once fetched and stored in a database, the app should:
  - Display Actual Tweets containing links
  - Display the most trending user who has shared the most links
  - Display the most trending Domains that have been shared so far

### Tech Stack

```
- Programming Languages
    - Python 3.6
- Frameworks
    - Django 3.1.2
- Database
     - SQLite3
- Frontend
    - HTML 5
    - CSS 3
    - Bootstrap 4
- API
    - Tweepy Api
```

### Installation

Install the dependencies and devDependencies and start the server.

-Note: Python must be installed on your system with versions 3.0 or above. You will also need a twitter developer account which you can get one at https://developer.twitter.com/en.
```sh
$ pip install -r requirements.txt
$ python manage.py runserver
```

### Deployement

The app is live and deployed to https://tweetlinks18.herokuapp.com 

### Database Structure and Schema
```
class Tweet(models.Model):
    tweet_id = models.CharField(max_length=100)
    date     = models.DateTimeField(default=timezone.now)
    author   = models.CharField(max_length=100)
    tweet_id = models.CharField(max_length=100)
    domain   = models.CharField(max_length=100)

```
### Images

![Login](https://github.com/AshutoshSundriyal/tweetlinks/blob/master/previews/login.JPG)
![Feed](https://github.com/AshutoshSundriyal/tweetlinks/blob/master/previews/tweetlinks.JPG)

### A Glimpse into the Backend
The backend of this app is managed by Django and Python. Tweepy API connects to the twitter's account of the user. Once connected the API fetches all the tweets of the user along with that of his/her friends. Then as clients requirement only tweets within the past 7 days are required , so a filtering function is used for that purpose. Moreover only those tweets are required which have links assosated with them, so second filter mechanism filter those tweets which have links.

So finally we are left with the required tweets of the user. Same process goes for users friends as well and we are left with the tweets that have to be displayed on the user's dashboard. Now every tweet list length of the user, gives details about the user's activity of that week and links shared by user along with his/her friends gives detail about the trending links. These are SQL databse queries which makes this opeartion less costly.

Now we are requred to give out the top user and the top domain. We are only considering domain names not exacty where the links refers.


