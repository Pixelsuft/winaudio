import os


def get_windows_sounds(ext_filter: tuple = ()) -> dict:
    lower_filter = tuple(x.lower() for x in ext_filter)
    media_path = os.path.join(
        os.getenv('windir'),
        'Media'
    )
    media_files = os.listdir(media_path)
    result = {}
    for media_file in media_files:
        file_full_path = os.path.join(
            media_path,
            media_file
        ).replace('/', '\\')
        if os.path.isdir(file_full_path):
            continue
        file_ext = media_file.split('.')[-1].lower().strip()
        if lower_filter and file_ext not in lower_filter:
            continue
        file_no_ext = '.'.join(media_file.split('.')[:-1])
        result[file_no_ext] = file_full_path
    return result
