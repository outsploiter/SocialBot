import os
import re
import subprocess

import requests

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

import auth
from utils.social_handler import get_reddit_client

TAGS = '''
.
.
.
#memes #cute #dogs #funny #photography #cats #puppy #puppies #doggies
'''


def mention_id(new_image, user_name):
    draw = ImageDraw.Draw(new_image)
    font = ImageFont.truetype('assets/fonts/Changa.ttf', 25)
    width, height = new_image.size
    text_position = (width * .03, height * .90)
    text_color = (225, 225, 225, 220)
    insta_id = f'@{user_name}'
    draw.text(text_position, insta_id, font=font, fill=text_color, stroke_width=1, stroke_fill='black')
    return new_image


def process_image(image, add_mention, profile):
    width, height = image.size
    aspect_ratio = width / height
    # Create a new image with the new aspect ratio
    if aspect_ratio > 1 and aspect_ratio > 1.97:
        # Horizontal image
        new_aspect_ratio = 90 / 47
        new_height = int(width / new_aspect_ratio)
        new_size = (width, new_height)
        new_image = Image.new("RGB", new_size, (255, 255, 255))
    elif aspect_ratio < 1 and aspect_ratio < 0.8:
        # Vertical image
        new_aspect_ratio = 4 / 5
        new_width = int(height * new_aspect_ratio)
        new_size = (new_width, height)
        new_image = Image.new("RGB", new_size, (255, 255, 255))
    else:
        new_image = image
        new_size = image.size
    # paste the original image on the new image and center it
    new_image.paste(image, (int((new_size[0] - width) / 2), int((new_size[1] - height) / 2)))

    if add_mention:
        user_name = auth.insta_profile[profile]['user']
        new_image = mention_id(new_image, user_name)

    return new_image


def download_image(post, subreddit, profile):
    path = f'{profile}/{subreddit}/images'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    url = post.url
    caption = post.title + TAGS
    print(url)
    file_name = url.split("/")
    if len(file_name) == 0:
        file_name = re.findall("/(.*?)", url)
    file_name = file_name[-1]
    if "." not in file_name:
        file_name += ".jpg"

    file_name = file_name.replace('.jpg', '_insta.jpg')

    file_name = path + '/' + file_name
    text_file = file_name.split('.')[0] + '.txt'
    if not os.path.exists(file_name):
        print('downloading file', file_name)
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        processed_image = process_image(image, True, profile)
        image_name = file_name.replace(file_name.split('.')[1], 'jpg')
        processed_image.save(image_name)
        # save title as caption text file
        text_file = open(text_file, "w", encoding="utf-8")
        n = text_file.write(caption)
        text_file.close()
    else:
        print("File already exists and not downloaded")
    return True


def unshorten_url(url):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = session.head(url, allow_redirects=True, headers=headers)
    return response.url


def create_tittle_and_caption_txt(post, path, file_name):
    title = post.title
    if len(title) > 60 or len(title) < 8:
        title = 'Wait for it..'
    words = title.split()
    lines = []
    while words:
        line_words = [words.pop(0)]
        # 35 character per line
        while words and len(' '.join(line_words + [words[0]])) <= 35:
            line_words.append(words.pop(0))
        lines.append(' '.join(line_words))
    formatted_tittle = '\n'.join(lines)
    print(formatted_tittle)
    with open(path + '/' + file_name + '_tittle.txt', 'w', encoding='utf-8') as file:
        file.write(formatted_tittle)

    post.comment_sort = 'best'
    post.comment_limit = 1
    for top_level_comment in post.comments:
        if str(top_level_comment.__class__) == "<class 'praw.models.reddit.comment.Comment'>":
            with open(path + '/' + file_name + '_insta.txt', 'w', encoding='utf-8') as file:
                file.write(str(top_level_comment.body) + TAGS)
    print('Created caption file')


def download_video(post, subreddit, profile):
    path = f'{profile}/{subreddit}/videos'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    url = post.url
    file_name = url.split("/")
    if len(file_name) == 0:
        file_name = re.findall("/(.*?)", url)
    file_name = file_name[-1]
    video_filename = file_name + '.mp4'
    audio_filename = file_name + '.mp3'

    video_url = post.media['reddit_video']['fallback_url']
    audio_url = post.url + '/DASH_audio.mp4'
    video_content = requests.get(video_url, stream=True).content

    audio_content = requests.get(audio_url).content

    if os.path.exists(path + '/' + video_filename):
        print('Already downloaded file proceeding with next step')
        return

    print('Downloading video file...')
    with open(path + '/' + video_filename, 'wb') as f:
        f.write(video_content)
    with open(path + '/' + audio_filename, 'wb') as f:
        f.write(audio_content)

    create_tittle_and_caption_txt(post, path, file_name)
    user_name = auth.insta_profile[profile]['user']

    print('Editing the video as reel')
    video_edit_command = f'''ffmpeg -i {path + '/' + video_filename} -i {path + '/' + audio_filename} -filter:v "crop=ih*9/16:ih,scale=-1:1080,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:white, drawtext=fontfile=assets/fonts/type.ttf:text='@{user_name}':fontcolor=black:fontsize=50:x=50:y=(h-text_h-50), drawtext=fontfile=assets/fonts/emoji.ttf:text='R R R':fontcolor=black:fontsize=90:x=(w-tw)/2:y=h-th-280, drawtext=textfile='{path}/{file_name}_tittle.txt':fontfile='assets/fonts/cute.ttf':fontsize=50:fontcolor=black:x=(w-text_w)/2:y=(h-text_h)/10" -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 256k {path}/{file_name}_insta.mp4'''
    shell_flag = subprocess.run(["powershell", video_edit_command], shell=True, stdout=subprocess.DEVNULL)
    if shell_flag.returncode == 0:
        print('Reel created\n')
        return True
    else:
        print('Edit failed')


def download_from_subreddit(subreddit_name, no_posts, profile):
    reddit = get_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)
    thread_list = subreddit.top(time_filter="day", limit=25)
    count = 0
    for i in thread_list:
        if count >= no_posts:
            break
        if i.is_self:
            print('text exists', end=', ')
        if i.domain == 'i.redd.it' and 'gif' not in i.url:
            print('image exists', end=', ')
            if download_image(i, subreddit_name, profile):
                count += 1
        if i.domain == 'v.redd.it':
            print('video', end='.\n')
            if download_video(i, subreddit_name, profile):
                count += 1
        print()


def edit_yt_video(path, profile):
    user_name = auth.insta_profile[profile]['user']
    output_path = path.replace('.mp4', '_reels.mp4')
    video_edit_command = f'''ffmpeg -i {path} -filter:v "crop=ih*9/16:ih,scale=-1:1080:flags=lanczos, drawtext=fontfile=assets/fonts/bgfont.ttf:text='@{user_name}':fontcolor=white:fontsize=25:x=50:y=(h-text_h-50)" -c:a copy -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart {output_path}'''
    shell_flag = subprocess.run(["powershell", video_edit_command], shell=True, stdout=subprocess.DEVNULL)
    if shell_flag.returncode == 0:
        print('Reel created\n')
        return True
    else:
        print('Edit failed')
        return False


def download_movie_caption(movie_name, path):
    print('downloading captions')
    base_url = "http://www.omdbapi.com/"
    api_key = auth.omdb_api_key

    response = requests.get(base_url, params={"t": movie_name, "plot": "full", "apikey": api_key})
    json_movie_data = response.json()

    keys = list(json_movie_data.keys())

    with open('assets/templates/caption_template.txt', 'r') as f:
        template = f.read()

    output_path = path.replace('mp4', 'txt')

    with open(fr'{output_path}', 'w') as f:
        f.write(template.format(**{k: json_movie_data[k] for k in keys}))

    poster_url = json_movie_data['Poster']
    response = requests.get(poster_url)

    poster_path = path.replace('mp4', 'jpg')

    with open(poster_path, "wb") as f:
        f.write(response.content)

    return True


def download_yt_video(youtube_link, start, end, profile, movie_name, do_not_edit):
    if movie_name is None:
        movie_name = 'Unnamed-collections'
    path = f'{profile}/youtube/{movie_name}'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    video_id = youtube_link.split('/')[-1].replace('watch?v=', '')
    video_output_path = f"{path}/{video_id}_insta.mp4"
    command_to_download = f'''yt-dlp --format "b*" --external-downloader ffmpeg --external-downloader-args "-ss {start} -to {end}" -f mp4 -o "{video_output_path}" {youtube_link}'''
    shell_flag = subprocess.run(["powershell", command_to_download], shell=True, stdout=subprocess.DEVNULL)
    if shell_flag.returncode == 0:
        print('Yt video Downloaded\n')

    _edited = False
    if not do_not_edit:
        _edited = edit_yt_video(video_output_path, profile)

    if _edited:
        if os.path.exists(video_output_path):
            os.remove(video_output_path)
        video_output_path = video_output_path.replace('.mp4', '_reels.mp4')

    if movie_name == 'Unnamed-collections':
        print('Caption not downloaded...')
        return 1
    else:
        download_movie_caption(movie_name, video_output_path)
