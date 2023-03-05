import os
from pathlib import Path

import utils.inventory_handler as inv
from utils.social_handler import get_insta_client

insta_client = None


def upload_to_insta(file_path):
    content = Path(file_path)
    global insta_client
    if insta_client is None:
        insta_client = get_insta_client()
    caption_path = file_path.replace(file_path.split('.')[1], 'txt')
    _temp = None
    with open(caption_path, encoding='utf-8') as file:
        caption = file.read()

    if file_path.endswith('jpg'):
        _temp = insta_client.photo_upload(content, caption)
    elif file_path.endswith('mp4'):
        _temp = insta_client.video_upload(content, caption)

    if _temp is not None:
        os.remove(file_path)
        os.remove(caption_path)
    return _temp


def upload(no_of_files=5):
    files_to_upload = inv.find_files()
    # print(str(files_to_upload[0]).replace('png', 'txt'))
    count = 0
    uploaded_flag = None
    for file in files_to_upload:
        if str(file).endswith('jpg') or str(file).endswith('_insta.mp4'):
            uploaded_flag = upload_to_insta(str(file))
        if uploaded_flag is not None:
            count += 1
        if count >= no_of_files:
            break
    print(f"Uploaded {count} posts on instagram")
