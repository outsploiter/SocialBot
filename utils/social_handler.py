import json
import os

from instagrapi import Client
import praw


def get_insta_client(profile):
    import auth
    profile = auth.insta_profile[profile]
    cookie_file = f'{profile["user"]}.json'
    if os.path.exists(cookie_file):
        cl = Client(json.load(open(cookie_file)))
    else:
        cl = Client()
        cl.login(profile['user'], profile['password'])
    json.dump(cl.get_settings(), open(cookie_file, 'w'), indent=4)

    return cl


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
        print("Something went wrong in reddit client...", e)
        reddit_cl = None

    return reddit_cl
