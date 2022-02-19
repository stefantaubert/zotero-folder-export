declare const Zotero: any

class ZoteroData {
  collections: Array<any> = new Array<any>();
  items: Array<any> = new Array<any>();
}

function doExport() {
  const data = new ZoteroData();

  let parentCollection: any;
  while (parentCollection = Zotero.nextCollection()) {
    data.collections.push(parentCollection);
  }

  let item: any;
  while ((item = Zotero.nextItem())) {
    data.items.push(item);
  }

  Zotero.write(JSON.stringify(data));
}
