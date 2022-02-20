import re
from pathlib import Path

from zotero_folder_export_core import build_library
from zotero_json_parsing import parse_zotero_json_tqdm


def main(path: Path, encoding: str = 'utf-8'):
  data = parse_zotero_json_tqdm(path, encoding)
  library = build_library(data)


def clean_name(name: str) -> str:
  result = re.sub(r'[^\w\d\-_\. ]', '_', name)
  return result
