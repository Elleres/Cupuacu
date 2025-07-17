import re
from typing import List


def get_file_extension(filename: str) -> str:
    match = re.search(r'\.([a-zA-Z0-9]+)$', filename)
    return match.group(1) if match else ''

def get_max_index_filename_list(curr_objects: List[str]) -> int:
    max_index = 0
    for arquivo in curr_objects:
        match = re.search(r"(?<=_)\d+(?=\.)", arquivo)
        if match:
            atual = int(match.group())
            if atual > max_index:
                max_index = atual
    return max_index