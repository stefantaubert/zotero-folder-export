from typing import Dict, Generator, Iterable, List, Tuple

from zotero_json_parsing import ZoteroData
from zotero_json_parsing.zotero_data import Collection


def process(data: ZoteroData) -> None:
  paths = get_collections_paths(data.collections)
  paths = dict(paths)
  print(paths)


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
