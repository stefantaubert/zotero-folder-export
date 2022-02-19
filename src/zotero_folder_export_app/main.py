from pathlib import Path

from zotero_folder_export_core.main import process
from zotero_json_parsing import parse_zotero_json_tqdm


def main(path: Path, encoding: str = 'utf-8'):
  data = parse_zotero_json_tqdm(path, encoding)
  process(data)
