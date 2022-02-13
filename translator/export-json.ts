declare const Zotero: any
declare const OS: any
// declare const fs: any

function log(msg, src: string = "test") {
  Zotero.debug(`Folder export: ${src} -> ${msg}`)
}

//const fs = require('fs')

interface IDescendent {
  id: number;
  name: string;
  key: string;
  // type is 'item' or 'collection'
  type: string;
  children?: IDescendent[];
}

interface IParentCollection {
  primary: {
    key: string;
  };
  fields: {
    name: string;
  }
  descendents: IDescendent[];
}

interface IItem {
  // can be: 'note', 'attachment', 'journalArticle', 'book'
  itemType: string;
}

interface ITopItem extends IItem {
  // can be: 'note', 'attachment', 'journalArticle', 'book'
  collections: string[];
}

interface IDefaultItem extends ITopItem {
  title: string;
  attachments: IAttachment[];
  notes: INote[];
}

interface IAttachmentItem extends ITopItem {
  title: string;
  filename: string;
  localPath: string;
}

interface INoteItem extends ITopItem {
  attachments: IAttachment[];
  note: string
}

interface IAttachment extends IItem {
  title: string;
  filename: string;
  localPath: string;
}

interface INote extends IItem {
  note: string
}

interface IExportItem {
  type: string;
  structure: string[];
}

interface IExportDefault extends IExportItem {
  item: string;
}

interface IExportAttachment extends IExportItem {
  path: string;
  item?: string;
}

interface IExportNote extends IExportItem {
  content: string;
  item?: string;
}

interface IExportCollection extends IExportItem {
}

interface IExport {
  attachments: IExportAttachment[];
  notes: IExportNote[];
  items: IExportItem[];

}

class Exporter {
  public getPathsForCollection(collection: IParentCollection): Record<string, Array<string>> {
    let paths: Record<string, Array<string>> = {}
    const parentFolders = new Array<string>();
    parentFolders.push(collection.fields.name);
    paths[collection.primary.key] = parentFolders

    log(collection, "parent-collection");
    log(collection.descendents, "parent-collection desc");
    for (let desc of collection.descendents) {
      for (let res of this.getDescendentPathsRecursive(desc, parentFolders)) {
        const key = res[0];
        const subPath = res[1];
        paths[key] = subPath;
      }
    }

    return paths;
  }

  private *getDescendentPathsRecursive(descendent: IDescendent, parentFolders: Array<string>): IterableIterator<[string, Array<string>]> {
    if (descendent.type == "collection") {
      var newFolder: Array<string> = Object.assign([], parentFolders);
      newFolder.push(descendent.name);
      yield [descendent.key, newFolder];
      if (descendent.children != null) {
        for (let child of descendent.children) {
          for (const tuple of this.getDescendentPathsRecursive(child, newFolder)) {
            yield tuple;
          }
        }
      }
    }
  }

  private join(...p: string[]) {
    return p.filter(_ => _).join('/')
  }

  clean(filename: string): string {
    const result = filename.replace(/[\x00-\x1F\x7F\/\\:*?"<>|$%]/g, encodeURIComponent);
    return result;
  }

  split(filename: string): string[] {
    const dot = filename.lastIndexOf('.')
    return (dot < 1 || dot === (filename.length - 1)) ? [filename, ''] : [filename.substring(0, dot), filename.substring(dot)]
  }


  public exportItem(item: ITopItem, paths: Record<string, string[]>) {
    switch (item.itemType) {
      case "attachment":
        this.exportAttachmentItem(item as IAttachmentItem, paths);
        break;
      case "note":
        // export not possible because method does not exist
        // this.exportNoteItem(item as INoteItem, paths);
        break;
      default:
        this.exportDefaultItem(item as IDefaultItem, paths);
        break;
    }
  }

  private exportDefaultItem(item: IDefaultItem, paths: Record<string, string[]>) {
    Zotero.debug(item);
    for (let collection of item.collections) {
      if (collection in paths) {

        const res: IExportDefault = {
          type: "item",
          structure: paths[collection],
          item: item.title,
        };
        Zotero.write(JSON.stringify(res) + "\n")

        const folder = this.join(...paths[collection]);
        const itemFolderName = this.clean(item.title);
        const [folder_base, folder_ext] = this.split(itemFolderName);
        if (item.attachments.length == 1) {
          const attachment = item.attachments[0];
          const fileName = this.clean(attachment.filename)
          const [file_base, file_ext] = this.split(fileName);
          const fileHasSameNameAsItem = folder_base === file_base;
          var fullPath: string;
          if (fileHasSameNameAsItem) {
            fullPath = this.join(folder, fileName);
          }
          else {
            fullPath = this.join(folder, folder_base, fileName);
          }

          log(JSON.stringify(fullPath), "saving")
          // attachment.saveFile(fullPath, true);
          //fs.writeFileSync(fullPath, "test");
          // is more or less required
          Zotero.write(`${attachment.localPath};${fullPath}\n`)
          Zotero.write(JSON.stringify(attachment) + "\n")
        }
        else {
          for (let attachment of item.attachments) {
            const fileName = this.clean(attachment.filename)
            const fullPath = this.join(folder, folder_base, fileName);
            log(JSON.stringify(fullPath), "saving")
            // attachment.saveFile(fullPath, true);
            //fs.writeFileSync(fullPath, "test");
            // is more or less required
            Zotero.write(`${attachment.localPath};${fullPath}\n`)
            Zotero.write(JSON.stringify(attachment) + "\n")
          }
        }
      }
    }
  }

  private exportAttachmentItem(item: IAttachmentItem, paths: Record<string, string[]>) {
    // const existingInPaths = item.collections.filter(s => s in paths);
    Zotero.debug(item);
    for (let collection of item.collections) {
      if (collection in paths) {
        const folder = this.join(...paths[collection]);
        const fileName = this.clean(item.filename)
        const fullPath = this.join(folder, fileName);
        log(JSON.stringify(fullPath), "saving")
        // item.saveFile(fullPath, true);
        Zotero.write(`${item.localPath};${fullPath}\n`)
        Zotero.write(JSON.stringify(item) + "\n")
      }
    }
  }

  // private exportNoteItem(item: INoteItem, paths: Record<string, string>) {
  //   Zotero.debug(item);
  //   for (let collection of item.collections) {
  //     if (collection in paths) {
  //       const folder = paths[collection];
  //       const fileName = "Note";
  //       //const fullPath = this.join(folder, fileName);
  //       //log(JSON.stringify(fullPath), "save as")
  //       //item.saveFile(fullPath, true);
  //       // is more or less required
  //       // Zotero.write(`${fullPath}\n`)
  //     }
  //   }
  // }
}

function doExport() {
  if (!Zotero.getOption('exportFileData')) throw new Error('File Hierarchy needs "Export File Data" to be on')

  const exporter = new Exporter();

  let finalPaths: Record<string, string[]> = {}
  let parentCollections: IParentCollection;

  while (parentCollections = Zotero.nextCollection()) {
    log(JSON.stringify(parentCollections), "constructor");
    const paths = exporter.getPathsForCollection(parentCollections);
    log(JSON.stringify(paths), "paths");
    finalPaths = Object.assign(finalPaths, paths)
  }

  log(JSON.stringify(finalPaths), "final paths");

  for (let path of Object.values(finalPaths)) {
    const res: IExportCollection = {
      type: "collection",
      structure: path
    }
    Zotero.write(JSON.stringify(res) + "\n");
  }

  log('collections: ' + JSON.stringify(this.path), "constructor2")

  let item: ITopItem;
  while ((item = Zotero.nextItem())) {
    log(JSON.stringify(item), "item");
    exporter.exportItem(item, finalPaths);
    // exporter.save(item)
  }
}
