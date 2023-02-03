import os
from pathlib import Path

import utils.inventory_handler as inv
from utils.social_handler import get_insta_client

cl = None


def upload_photo_insta(file_path):
    image = Path(file_path)
    global cl
    if cl is None:
        cl = get_insta_client()
    caption_path = file_path.replace(file_path.split('.')[1], 'txt')
    with open(caption_path, encoding='utf-8') as file:
        caption = file.read()
    _temp = cl.photo_upload(image, caption)
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
        if 'jpg' in str(file):
            uploaded_flag = upload_photo_insta(str(file))
        if uploaded_flag is not None:
            count += 1
        if count >= no_of_files:
            break
    print(f"Uploaded {count} posts on instagram")
