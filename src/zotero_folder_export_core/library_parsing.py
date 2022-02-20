from collections import OrderedDict
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Dict, Generator, Iterable, List, Optional
from typing import OrderedDict as OrderedDictType
from typing import Tuple

from ordered_set import OrderedSet
from zotero_json_parsing import Collection as ZoteroCollection
from zotero_json_parsing import Data as ZoteroData
from zotero_json_parsing import Item as ZoteroItem
from zotero_json_parsing import Tag as ZoteroTag

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
  non_items: List[NonItem]


@dataclass()
class Collection():
  name: str
  collections: List['Collection']
  entries: List[Entry]


@dataclass()
class Library():
  collections: List[Collection]

  # contains entries that are in no collection
  unfiled: List[Entry]

  # contains to each tag the entries with that tag
  tags: OrderedDictType[str, List[Entry]]


def build_library(data: ZoteroData) -> Library:
  collections = []
  collection_dict = dict(add_collections(data.collections, collections))

  unfiled = []
  tags = OrderedDict()
  add_items(data.items, collection_dict, unfiled, tags)

  result = Library(collections, unfiled, tags)
  return result


def add_items(zotero_items: Iterable[ZoteroItem], collection_dict: Dict[str, Collection], unfiled: List[Entry], tags: OrderedDictType[str, List[Entry]]) -> None:
  collection_keys = set(collection_dict.keys())
  for zotero_item in zotero_items:
    entry: Entry
    if zotero_item.itemType == "attachment":
      non_item = get_non_item(zotero_item.linkMode, zotero_item.title,
                              zotero_item.localPath, zotero_item.url)
      entry = non_item
    elif zotero_item.itemType == "note":
      note = Note(zotero_item.note, zotero_item.uri)
      entry = note
    else:
      item = Item(zotero_item.title, zotero_item.url, [])

      for zotero_attachment in zotero_item.attachments:
        attachment = get_non_item(zotero_attachment.linkMode, zotero_attachment.title,
                                  zotero_attachment.localPath, zotero_attachment.url)
        if attachment is not None:
          item.non_items.append(attachment)

        for tag in get_tags_from_zotero_tag(zotero_attachment.tags):
          if tag not in tags:
            tags[tag] = []
          tags[tag].append(attachment)

      for zotero_note in zotero_item.notes:
        note = Note(zotero_note.note, zotero_item.uri)
        item.non_items.append(note)

        for tag in get_tags_from_zotero_tag(zotero_note.tags):
          if tag not in tags:
            tags[tag] = []
          tags[tag].append(note)

      entry = item

    intersecting_collection_keys = set(zotero_item.collections).intersection(collection_keys)
    for collection_key in intersecting_collection_keys:
      collection_dict[collection_key].entries.append(entry)
    if len(intersecting_collection_keys) == 0:
      unfiled.append(entry)

    for tag in get_tags_from_zotero_tag(zotero_item.tags):
      if tag not in tags:
        tags[tag] = []
      tags[tag].append(entry)


def get_tags_from_zotero_tag(tags: List[ZoteroTag]) -> OrderedSet[str]:
  tag_names = (tag.tag for tag in tags)
  unique_names = OrderedSet(tag_names)
  return unique_names


def get_non_item(link_mode: str, title: Optional[str], path: Optional[Path], url: Optional[Url]) -> Optional[NonItem]:
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
    parent_key = zotero_collection.fields.parentKey
    has_no_parents = isinstance(parent_key, bool) and parent_key == False
    if has_no_parents:
      collection = Collection(zotero_collection.fields.name, [], [])
      collections.append(collection)
      yield zotero_collection.primary.key, collection
      for descendent in zotero_collection.descendents:
        yield from add_subcollections_from_descendents(descendent, collection)


def add_subcollections_from_descendents(descendent: ZoteroCollection.Descendent, parent: Collection) -> Generator[Tuple[str, Collection], None, None]:
  if descendent.type == "collection":
    collection = Collection(descendent.name, [], [])
    parent.collections.append(collection)
    yield descendent.key, collection
    for child in descendent.children:
      yield from add_subcollections_from_descendents(child, collection)
