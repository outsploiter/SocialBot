import os
import sys
from pathlib import Path
from itertools import islice


def show_inventory(dir_path: Path = 'data/', level: int = -1, limit_to_directories: bool = False, length_limit: int = 1000):
    space = '    '
    branch = '│   '
    tee = '├── '
    last = '└── '
    """Given a directory Path object print a visual tree structure"""
    dir_path = Path(dir_path)  # accept string coerceable to Path
    files = 0
    directories = 0
    file_list = []

    def inner(dir_path: Path, prefix: str = '', level=-1):
        nonlocal files, directories
        if not level:
            return  # 0, stop iterating
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]
        else:
            try:
                contents = list(dir_path.iterdir())
            except FileNotFoundError:
                print('No files are found..')
                sys.exit()
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space
                yield from inner(path, prefix=prefix + extension, level=level - 1)
            elif not limit_to_directories:
                file_list.append(path)
                yield prefix + pointer + path.name
                files += 1

    print(dir_path.name)
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line)
    if next(iterator, None):
        print(f'... length_limit, {length_limit}, reached, counted:')
    print(f'\n{directories} directories' + (f', {files} files' if files else ''))
    file_list.sort(key=lambda x: os.path.getctime(x))
    return file_list


def find_files(path='data', no_of_files=5):
    files = show_inventory()

    if len(files) < no_of_files*2:
        return [file for file in files if 'txt' not in str(file)]
    return [file for file in files[:no_of_files*2] if 'txt' not in str(file)]


def cleanup_uploaded_files():
    import datetime
    print('Cleaning uploaded files..')
    file_list = show_inventory()

    for file in file_list:
        if os.path.isfile(file):
            creation_time = os.path.getctime(file)
            creation_date = datetime.datetime.fromtimestamp(creation_time)
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            if creation_date.date() <= yesterday.date():
                print(f"Deleting the file since the file {file} was created yesterday or before.")
                os.remove(file)
