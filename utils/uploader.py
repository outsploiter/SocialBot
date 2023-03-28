import os
from pathlib import Path

import utils.inventory_handler as inv
from utils.social_handler import get_insta_client

insta_client = None


def upload_to_insta(file_path, profile):
    content = Path(file_path)
    global insta_client
    if insta_client is None:
        insta_client = get_insta_client(profile)
    caption_path = file_path.replace(file_path.split('.')[1], 'txt')
    _temp = None
    caption = None
    if os.path.exists(caption_path):
        with open(caption_path, encoding='utf-8') as file:
            caption = file.read()
    if caption is not None and len(caption)>2000:
        print('')
        caption = '''Look at this amazing video\n#movies #movie #flim #instagood'''

    if file_path.endswith('jpg'):
        _temp = insta_client.photo_upload(content, caption)
    elif file_path.endswith('mp4'):
        thumbnail_path = file_path.replace(file_path.split('.')[1], 'jpg')
        if os.path.exists(thumbnail_path):
            _temp = insta_client.video_upload(content, caption=caption, thumbnail=thumbnail_path)
        else:
            _temp = insta_client.video_upload(content, caption)

    # Renaming file so we don't upload them again
    if _temp is not None:
        new_file_path = file_path.replace('.jpg', '_uploaded.jpg').replace('.mp4', '_uploaded.mp4')
        os.rename(file_path, new_file_path)
        try:
            new_caption_path = caption_path.replace('.txt', '_uploaded.txt')
            os.rename(caption_path, new_caption_path)
        except FileNotFoundError:
            print('no caption file')
    return _temp


def upload(no_of_files, profile):
    files_to_upload = inv.find_files(profile)
    count = 0
    uploaded_flag = None
    for file in files_to_upload:
        if str(file).endswith('_insta.jpg') or str(file).endswith('_insta.mp4') or str(file).endswith('_reels.mp4'):
            uploaded_flag = upload_to_insta(str(file), profile)
        if uploaded_flag is not None:
            count += 1
        if count >= no_of_files:
            break
    print(f"Uploaded {count} posts on instagram")
