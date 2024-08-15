import os


def get_convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def get_file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return get_convert_bytes(file_info.st_size)