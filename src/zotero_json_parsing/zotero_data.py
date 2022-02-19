
import dataclasses
from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass()
class ZoteroData():

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

    childCollections: List[int]

    childItems: List[int]

    @dataclass()
    class Descendent():
      id: int
      key: str
      type: str
      parent: int
      level: Optional[int]
      name: Optional[str]
      children: List["Descendent"] = dataclasses.field(default_factory=lambda: [])

    descendents: List[Descendent]  # = dataclasses.field(default_factory=lambda: [])

  collections: List[Collection]  # = dataclasses.field(default_factory=lambda: [])

  @dataclass()
  class Item():
    version: int
    itemType: str
    #title: str
    #contentType: str
    #charset: str
    #filename: str
    #dataAdded: Optional[str]
    #dataModified: str
    uri: str
    linkMode: Optional[str]
    localPath: Optional[str]
    note: Optional[str]

    #language: str
    #libraryCatalog: str
    # pages: str

    # @dataclass()
    # class Creator():
    #   firstName: str
    #   lastName: str
    #   creatorType: str

    # creators: List[Creator] = dataclasses.field(default_factory=lambda: [])
    tags: List[str] = dataclasses.field(default_factory=lambda: [])
    collections: List[str] = dataclasses.field(default_factory=lambda: [])
    relations: Union[Dict[str, str], List[str]] = dataclasses.field(default_factory=lambda: [])

    @dataclass()
    class Attachment():
      title: Optional[str]
      filename: Optional[str]
      localPath: Optional[str]

    attachments: List[Attachment] = dataclasses.field(default_factory=lambda: [])

    @dataclass()
    class Note():
      title: Optional[str]
      filename: Optional[str]
      localPath: Optional[str]

    notes: List[Note] = dataclasses.field(default_factory=lambda: [])

  items: List[Item]  # = dataclasses.field(default_factory=lambda: [])
  # Schema: ClassVar[Type[Schema]] = Schema  # For the type checker
