import json
from pathlib import Path
from typing import Dict, cast

import marshmallow_dataclass
from marshmallow import EXCLUDE, Schema

from zotero_json_parsing.zotero_data import ZoteroData


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
