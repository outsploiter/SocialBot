from utils import downloader, uploader


def main():
    no_of_post = 2
    subreddit = 'dankmemes'
    downloader.download_from_subreddit(subreddit, no_of_post)
    uploader.upload(no_of_post)


if __name__ == '__main__':
    main()
