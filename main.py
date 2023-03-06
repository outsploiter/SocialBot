import argparse
from utils import downloader, uploader, inventory_handler


def main():
    description = '''
    Example script for parsing command line arguments. 
    python main.py -r subredditName -n 3
    (or)
    python main.py -m file_path -s hh:mm:ss -e hh:mm:ss
    '''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-r', '--reddit', type=str, default=None, help='enter the subreddit')
    parser.add_argument('-d', '--no_of_download', default=None, type=int, help='enter the no of posts to be '
                                                                               'downloaded from subreddit')
    parser.add_argument('-u', '--no_of_upload', default=None, type=int, help='enter the no of posts to be uploaded to '
                                                                             'instagram')
    parser.add_argument('-y', '--youtube_link', default=None, type=str, help='enter the movie file path')
    parser.add_argument('-s', '--start', type=str, default=None, help='enter the start of the clip')
    parser.add_argument('-e', '--end', type=str, default=None, help='enter the end of the clip')
    parser.add_argument('-c', '--clean', type=bool, default=False)
    args = parser.parse_args()

    no_of_download = args.no_of_download
    no_of_upload = args.no_of_upload
    subreddit = args.reddit

    youtube_link = args.youtube_link

    clean = args.clean

    if subreddit and no_of_download:
        if subreddit.startswith('r/'):
            subreddit = subreddit.split('r/')[1]
        downloader.download_from_subreddit(subreddit, no_of_download)

    if no_of_upload:
        uploader.upload(no_of_upload)

    if clean:
        inventory_handler.cleanup_uploaded_files()


if __name__ == '__main__':
    main()
