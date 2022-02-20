import dataclasses
from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass()
class Collection():
  name: str
  id: int

  @dataclass()
  class Primary():
    collectionID: int
    libraryID: int
    key: str

  primary: Primary

  @dataclass()
  class Fields():
    name: str
    parentKey: Union[bool, str]

  fields: Fields

  childCollections: Union[Dict[str, str], List[int]] = dataclasses.field(default_factory=list)

  childItems: List[int] = dataclasses.field(default_factory=list)

  @dataclass()
  class Descendent():
    id: int
    key: str
    type: str
    parent: int
    level: Optional[int]
    name: Optional[str]
    children: List["Descendent"] = dataclasses.field(default_factory=list)

  descendents: List[Descendent] = dataclasses.field(default_factory=list)


@dataclass()
class Tag():
  tag: str


@dataclass()
class Item():
  version: int
  itemType: str
  title: Optional[str]
  #contentType: str
  #charset: str
  #filename: str
  #dataAdded: Optional[str]
  #dataModified: str
  uri: str
  url: Optional[str]
  linkMode: Optional[str]
  localPath: Optional[str]
  note: Optional[str]
  parentItem: Optional[str]

  #language: str
  #libraryCatalog: str
  # pages: str

  # @dataclass()
  # class Creator():
  #   firstName: str
  #   lastName: str
  #   creatorType: str

  # creators: List[Creator] = dataclasses.field(default_factory=list)

  tags: List[Tag] = dataclasses.field(default_factory=list)
  collections: List[str] = dataclasses.field(default_factory=list)
  relations: Dict[str, List[str]] = dataclasses.field(default_factory=list)

  @dataclass()
  class Attachment():
    title: Optional[str]
    filename: Optional[str]
    localPath: Optional[str]
    itemType: str
    linkMode: str
    url: Optional[str]
    tags: List[Tag] = dataclasses.field(default_factory=list)

  attachments: List[Attachment] = dataclasses.field(default_factory=list)

  @dataclass()
  class Note():
    key: str
    uri: str
    note: str
    tags: List[Tag] = dataclasses.field(default_factory=list)

  notes: List[Note] = dataclasses.field(default_factory=list)


@dataclass()
class Data():

  collections: List[Collection]  # = dataclasses.field(default_factory=list)

  items: List[Item]  # = dataclasses.field(default_factory=list)
  # Schema: ClassVar[Type[Schema]] = Schema  # For the type checker
