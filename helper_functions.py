import json
import os.path
from pathlib import Path

from instagrapi import Client
import praw

import downloader


def get_insta_client():
    if os.path.exists('cookies.json'):
        cl = Client(json.load(open('cookies.json')))
    else:
        import auth
        cl = Client()
        cl.login(auth.insta_user, auth.insta_password)
    json.dump(cl.get_settings(), open('cookies.json', 'w'), indent=4)

    return cl


def upload_to_insta(file):
    photo_path = Path(file)
    cl = get_insta_client()
    cl.photo_upload(photo_path, "hello this is a test from api")


def get_reddit_client():
    import auth
    try:
        reddit_cl = praw.Reddit(
            client_id=auth.reddit_client_id,
            client_secret=auth.reddit_client_secret,
            user_agent=auth.reddit_user_agent,
            username=auth.reddit_username,
            passkey=auth.reddit_password,
            check_for_async=False,
        )

    except Exception as e:
        print("Something went wrong...", e)
        reddit_cl = None

    return reddit_cl


def download_from_subreddit(subreddit_name):
    reddit = get_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)
    thread_list = subreddit.top(time_filter="day", limit=5)
    for i in thread_list:
        if i.is_self:
            print('text exists', end=', ')
        if i.domain == 'i.redd.it' and 'gif' not in i.url:
            print('image exists', end=', ')
            downloader.download_image(i, subreddit_name)
        if i.domain == 'v.redd.it' or 'gif' in i.url:
            print('video', end='.')
        print()
