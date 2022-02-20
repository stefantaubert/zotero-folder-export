import re
from collections import OrderedDict
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Dict, Generator, Iterable, List, Optional
from typing import OrderedDict as OrderedDictType
from typing import Tuple

from zotero_json_parsing import Collection as ZoteroCollection
from zotero_json_parsing import Data as ZoteroData
from zotero_json_parsing import Item as ZoteroItem

Url = str


@dataclass()
class Entry():
  pass


@dataclass()
class NonItem(Entry):
  pass


@dataclass()
class LinkedWebsite(NonItem):
  title: str
  url: Url


@dataclass()
class LinkedFile(NonItem):
  title: str
  path: Path


@dataclass()
class Note(NonItem):
  content: str

  # to distinguish two different notes with the same content
  identifier: str


@dataclass()
class ImportedFile(NonItem):
  # imported file or webpage (html -> Snapshot)
  title: str
  path: Path
  url: Optional[Url]


@dataclass()
class Item(Entry):
  title: str
  url: Optional[Url]
  entries: List[NonItem]


@dataclass()
class Collection():
  name: str
  collections: List['Collection']
  items: List[Item]
  entries: List[NonItem]


@dataclass()
class Unfiled():
  items: List[Item]
  entries: List[NonItem]


@dataclass()
class Tagged():
  items: Dict[str, List[Item]]
  entries: Dict[str, List[NonItem]]


@dataclass()
class Library():
  collections: List[Collection]
  unfiled: Unfiled
  tagged: Tagged


def build_library(data: ZoteroData) -> Library:
  collections = []
  collection_dict = dict(add_collections(data.collections, collections))

  unfiled = Unfiled([], [])
  tagged = Tagged({}, {})

  add_items(data.items, collection_dict, unfiled, tagged)

  result = Library(collections, unfiled, tagged)
  return result


def add_items(zotero_items: Iterable[ZoteroItem], collection_dict: Dict[str, Collection], unfiled: Unfiled, tagged: Tagged) -> None:
  for zotero_item in zotero_items:
    collection_keys = set(zotero_item.collections).intersection(collection_dict.keys())

    if zotero_item.itemType in {"attachment", "note"}:
      entry: NonItem
      if zotero_item.itemType == "attachment":
        entry = get_entry_from_item(zotero_item)
      else:
        entry = Note(zotero_item.note, zotero_item.uri)

      for collection_key in collection_keys:
        collection_dict[collection_key].entries.append(entry)
      if len(collection_keys) == 0:
        unfiled.entries.append(entry)

      for tag in set(zotero_item.tags):
        if tag not in tagged.entries:
          tagged.entries[tag] = []
        tagged.entries[tag].append(entry)

    else:
      item = Item(zotero_item.title, zotero_item.url, [])
      for zotero_attachment in zotero_item.attachments:
        attachment = get_entry_from_attachment(zotero_attachment)
        if attachment is not None:
          item.entries.append(attachment)
      for zotero_note in zotero_item.notes:
        note = Note(zotero_note.note, zotero_item.uri)
        item.entries.append(note)

      for collection_key in collection_keys:
        collection_dict[collection_key].items.append(item)
      if len(collection_keys) == 0:
        unfiled.items.append(item)

      for tag in set(zotero_item.tags):
        if tag not in tagged.items:
          tagged.items[tag] = []
        tagged.items[tag].append(item)


def get_entry_from_item(item: ZoteroItem) -> Optional[Item]:
  return get_entry(item.linkMode, item.title, item.localPath, item.url)


def get_entry_from_attachment(attachment: ZoteroItem.Attachment) -> Optional[NonItem]:
  return get_entry(attachment.linkMode, attachment.title, attachment.localPath, attachment.url)


def get_entry(link_mode: str, title: Optional[str], path: Optional[Path], url: Optional[Url]) -> Optional[NonItem]:
  entry = None
  if link_mode in {"imported_file", "imported_url"}:
    entry = ImportedFile(title, path, url)
  elif link_mode == "linked_file":
    entry = LinkedFile(title, path)
  elif link_mode == "linked_url":
    entry = LinkedWebsite(title, url)
  elif link_mode == "embedded_image":
    logger = getLogger(__name__)
    logger.error("Embedded images are not supported! Entry ignored.")
  elif link_mode is None:
    logger = getLogger(__name__)
    logger.error("Property linkMode is missing! Entry ignored.")
  else:
    logger = getLogger(__name__)
    logger.error(f"Invalid linkMode '{link_mode}'! Entry ignored.")
  return entry


def add_collections(zotero_collections: Iterable[ZoteroCollection], collections: List[Collection]) -> Generator[Tuple[str, Collection], None, None]:
  for zotero_collection in zotero_collections:
    collection = Collection(zotero_collection.fields.name, [], [], [])
    collections.append(collection)
    yield zotero_collection.primary.key, collection
    for descendent in zotero_collection.descendents:
      yield from add_subcollections_from_descendents(descendent, collection)


def add_subcollections_from_descendents(descendent: ZoteroCollection.Descendent, parent: Collection) -> Generator[Tuple[str, Collection], None, None]:
  if descendent.type == "collection":
    collection = Collection(descendent.name, [], [], [])
    parent.collections.append(collection)
    yield descendent.key, collection
    for child in descendent.children:
      yield from add_subcollections_from_descendents(child, collection)
