import re

def get_file_extension(filename: str) -> str:
    match = re.search(r'\.([a-zA-Z0-9]+)$', filename)
    return match.group(1) if match else ''
