import re
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Generator, Iterable, List
from typing import OrderedDict as OrderedDictType
from typing import Tuple

from zotero_json_parsing import Collection, Item, ZoteroData


@dataclass()
class ExportWebpage():
  title: str
  url: str
  # True, if the webpage was linked
  linked: bool


@dataclass()
class ExportNote():
  # contains the HTML-content of the note
  content: str


@dataclass()
class ExportFolder():
  # represent folders inside Zotero directories

  # contains the path to the folder
  path: Path


@dataclass()
class ExportFile():
  # True, if the file was a linked file
  linked: bool

  # True, if the file was found in the Zotero directory but was not present in Zotero
  hidden: bool

  # contains the path to the file
  path: Path


class ExportAttachment():
  title: str

  files: List[ExportFile]
  folders: List[ExportFolder]

  webpages: List[ExportWebpage]


@dataclass()
class ExportItem():
  title: str
  attachments: List[ExportAttachment]

  # notes without items
  notes: List[ExportNote]

  # webpages without items
  webpages: List[ExportWebpage]


@dataclass()
class ExportCollection():
  structure: Tuple[str, ...]
  items: List[ExportItem]

  # notes without items
  notes: List[ExportNote]


def process(data: ZoteroData) -> None:
  paths = get_collections_paths(data.collections)
  paths = ((key, get_collection_folder(path)) for key, path in paths)
  paths = OrderedDict(paths)
  print(paths)


def get_items(items: Iterable[Item]):
  for item in items:
    is_from_item = item.parentItem is not None
    if is_from_item:
      pass
    else:
      pass

    if item.itemType == "attachment":
      pass


def get_collection_folders(paths: Iterable[Tuple[str, ...]]) -> Generator[Path, None, None]:
  for path in paths:
    yield get_collection_folder(path)


def get_collection_folder(path: Tuple[str, ...]) -> Path:
  clean_parts = list(clean_name(part) for part in path)
  path = Path(*clean_parts)
  return path


def clean_name(name: str) -> str:
  result = re.sub(r'[^\w\d\-_\. ]', '_', name)
  return result


def get_collections_paths(collections: Iterable[Collection]) -> Generator[Tuple[str, Tuple[str, ...]], None, None]:
  for collection in collections:
    yield from get_collection_paths(collection, path=[collection.fields.name])


def get_collection_paths(collection: Collection, path: List[str]) -> Generator[Tuple[str, Tuple[str, ...]], None, None]:
  for descendent in collection.descendents:
    yield from get_descendent_paths(descendent, path)


def get_descendent_paths(descendent: Collection.Descendent, path: List[str]) -> Generator[Tuple[str, Tuple[str, ...]], None, None]:
  if descendent.type == "collection":
    new_path = path.copy()
    new_path.append(descendent.name)
    yield descendent.key, tuple(new_path)
    for child in descendent.children:
      yield from get_descendent_paths(child, new_path)
