import argparse
from utils import downloader, uploader, inventory_handler


def main():
    description = '''
    Example script for parsing command line arguments. 
    python main.py -r subredditName -n 3
    (or)
    python main.py -y https://youtube_link.com/gtecop -s hh:mm:ss -e hh:mm:ss
    '''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-r', '--reddit', type=str, default=None, help='enter the subreddit')
    parser.add_argument('-d', '--no_of_download', default=None, type=int,
                        help='enter the no of posts to be downloaded from subreddit')

    parser.add_argument('-y', '--youtube_link', default=None, type=str, help='enter the movie file path')
    parser.add_argument('-m', '--movie_name', default=None, type=str, help='enter the movie name you are downloading')
    parser.add_argument('-s', '--start', type=str, default=None, help='enter the start of the clip')
    parser.add_argument('-e', '--end', type=str, default=None, help='enter the end of the clip')

    parser.add_argument('-p', '--profile', type=str, default='profile_1',
                        help='Enter the profile as entered in auth.py')
    parser.add_argument('-u', '--no_of_upload', default=None, type=int,
                        help='enter the no of posts to be uploaded to instagram')

    parser.add_argument('-c', '--clean', type=bool, default=False, help='Enter True or False to run cleanup')

    args = parser.parse_args()

    no_of_download = args.no_of_download
    no_of_upload = args.no_of_upload
    subreddit = args.reddit

    youtube_link = args.youtube_link
    movie_name = args.movie_name
    start = args.start
    end = args.end

    insta_profile = args.profile

    clean = args.clean

    if subreddit and no_of_download and insta_profile:
        if subreddit.startswith('r/'):
            subreddit = subreddit.split('r/')[1]
        downloader.download_from_subreddit(subreddit, no_of_download, insta_profile)

    elif youtube_link and start and end and insta_profile:
        pattern = r'^([0-5][0-9]):([0-5][0-9]):([0-5][0-9])$'
        import re
        if re.match(pattern, start) and re.match(pattern, end):
            downloader.download_yt_video(youtube_link, start, end, insta_profile, movie_name)
        else:
            print('Start and End should be given in "hh:mm:ss" format')
            print(f'you have provide this.. \nstart: {start}\nend:{end}')

    if no_of_upload and insta_profile:
        uploader.upload(no_of_upload, insta_profile)

    if clean:
        inventory_handler.cleanup_uploaded_files()


if __name__ == '__main__':
    main()
