import argparse
from utils import downloader, uploader


def main():
    description = '''
    Example script for parsing command line arguments. 
    python main.py -r subredditName -n 3
    (or)
    python main.py -m file_path -s hh:mm:ss -e hh:mm:ss
    '''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-r', '--reddit', type=str, help='enter the subreddit')
    parser.add_argument('-n', '--number', type=int, help='enter the no of posts to be uploaded to instagram')
    parser.add_argument('-m', '--movie_path', type=str, help='enter the movie file path')
    args = parser.parse_args()
    no_of_post = args.number
    subreddit = args.reddit
    movie_path = args.movie_path
    print(no_of_post, subreddit, movie_path)

    if subreddit and no_of_post:
        if subreddit.startswith('r/'):
            subreddit = subreddit.split('r/')[1]
        downloader.download_from_subreddit(subreddit, no_of_post)
        pass
    if no_of_post:
        uploader.upload(no_of_post)
        pass


if __name__ == '__main__':
    main()
