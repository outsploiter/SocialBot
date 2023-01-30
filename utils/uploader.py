from social_handler import get_insta_client
from pathlib import Path


def upload_to_insta(file):
    photo_path = Path(file)
    cl = get_insta_client()
    cl.photo_upload(photo_path, "hello this is a test from f")