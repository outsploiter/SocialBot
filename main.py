from utils import social_handler


def main():
    social_handler.download_from_subreddit('terriblefacebookmemes', no_posts=10)


if __name__ == '__main__':
    main()
