import argparse
from utils import downloader, uploader


def main():
    description = '''Example script for parsing command line arguments. 
    python main.py -r subredditName -n 3
    (or)
    python main.py -m file_path -s hh:mm:ss -e hh:mm:ss'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-r', '--reddit', type=str, default='aww', help='enter the subreddit name with r/')
    parser.add_argument('-n', '--number', type=int, default=1, help='enter the no of posts to be uploaded to instagram')
    args = parser.parse_args()
    no_of_post = args.number
    subreddit = args.reddit
    downloader.download_from_subreddit(subreddit, no_of_post)
    uploader.upload(no_of_post)


if __name__ == '__main__':
    main()
