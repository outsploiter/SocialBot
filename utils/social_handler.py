import json
import os

from instagrapi import Client
import praw


def get_insta_client():
    if os.path.exists('cookies.json'):
        cl = Client(json.load(open('cookies.json')))
    else:
        import auth
        cl = Client()
        cl.login(auth.insta_user, auth.insta_password)
    json.dump(cl.get_settings(), open('cookies.json', 'w'), indent=4)

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
