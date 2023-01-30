import os
import re
import requests

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def mention_id(new_image):
    draw = ImageDraw.Draw(new_image)

    # Choose a font and size
    font = ImageFont.truetype('assets/fonts/Changa.ttf', 25)

    # Position of the text (bottom right corner)
    width, height = new_image.size
    text_position = (width * .03, height * .90)

    # Text color and transparency (r, g, b, a)
    text_color = (225, 225, 225, 220)
    insta_id = "@_galibaa_"

    # Add text to the image
    draw.text(text_position, insta_id, font=font, fill=text_color, stroke_width=1, stroke_fill='black')
    return new_image


def process_image(image, add_mention=True):
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

    # Save the image
    if add_mention:
        new_image = mention_id(new_image)

    return new_image


def download_image(post, subreddit):
    path = f'data/{subreddit}/images'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    url = post.url
    print(url)
    file_name = url.split("/")
    if len(file_name) == 0:
        file_name = re.findall("/(.*?)", url)
    file_name = file_name[-1]
    if "." not in file_name:
        file_name += ".jpg"

    file_name = path + '/' + file_name
    if not os.path.exists(file_name):
        print('downloading file', file_name)
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        processed_image = process_image(image)
        processed_image.save(file_name)
    else:
        print("File already exists and not downloaded")


def download_from_subreddit(subreddit_name, no_posts=10):
    reddit = social_handler.get_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)
    thread_list = subreddit.top(time_filter="day", limit=no_posts)
    for i in thread_list:
        if i.is_self:
            print('text exists', end=', ')
        if i.domain == 'i.redd.it' and 'gif' not in i.url:
            print('image exists', end=', ')
            download_image(i, subreddit_name)
        if i.domain == 'v.redd.it' or 'gif' in i.url:
            print('video', end='.')
        print()
