import json
from logging import getLogger
from pathlib import Path
from typing import Dict, List, cast

import marshmallow_dataclass
from marshmallow import EXCLUDE, Schema
from tqdm import tqdm

from zotero_json_parsing.zotero_data import Collection, Item, ZoteroData


def parse_json(path: Path, encoding: str) -> Dict:
  assert path.is_file()
  with path.open(mode='r', encoding=encoding) as f:
    tmp = json.load(f)
  return tmp


class BaseSchema(Schema):
  class Meta:
    unknown = EXCLUDE


def parse_zotero_json(path: Path, encoding: str = 'utf-8') -> ZoteroData:
  data_schema = marshmallow_dataclass.class_schema(ZoteroData, BaseSchema)
  schema_instance = data_schema()
  json_content = parse_json(path, encoding)
  res = schema_instance.load(json_content)
  res = cast(ZoteroData, res)
  return res


def parse_zotero_json_tqdm(path: Path, encoding: str = 'utf-8') -> ZoteroData:
  logger = getLogger(__name__)
  logger.info("Reading json...")
  json_content = parse_json(path, encoding)

  logger.info("Parsing items...")
  data_schema = marshmallow_dataclass.class_schema(Item, BaseSchema)
  schema_instance = data_schema()
  items: List = json_content["items"]
  zotero_items = schema_instance.load(tqdm(items), many=True)

  logger.info("Parsing collections...")
  data_schema = marshmallow_dataclass.class_schema(Collection, BaseSchema)
  schema_instance = data_schema()
  collections: List = json_content["collections"]
  zotero_collections = schema_instance.load(tqdm(collections), many=True)

  res = ZoteroData(zotero_collections, zotero_items)
  return res
