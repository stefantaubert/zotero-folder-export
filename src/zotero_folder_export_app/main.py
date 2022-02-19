from pathlib import Path

from zotero_json_parsing import parse_zotero_json


def main(path: Path, encoding: str = 'utf-8'):
  data = parse_zotero_json(path, encoding)
