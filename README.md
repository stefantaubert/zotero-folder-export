# zotero-folder-export
Tool for exporting Zotero collection to folders.


		"exportCharset": "UTF-8",

if Zotero.getOption("exportNotes")
if Zotero.getOption("exportFileData")
Zotero.Utilities.unescapeHTML(note.note)

{
	"translatorID": "b6e39b57-8942-4d11-8259-342c46ce395f",
	"translatorType": 2,
	"label": "BibLaTeX",
	"creator": "Simon Kornblith, Richard Karnesky and Anders Johansson",
	"target": "json",
	"minVersion": "2.1.9",
	"maxVersion": "null",
	"priority": 100,
	"inRepository": true,
	"configOptions": {
		"getCollections": true
	},
	"displayOptions": {
		"exportCharset": "UTF-8",
		"exportNotes": false,
		"exportFileData": false,
		"useJournalAbbreviation": false
		"Export Collections": true
	},
	"lastUpdated": "2019-12-15 14:26:00"
}


chrome/locale/en-US/zotero/zotero.properties:835
exportOptions.exportNotes=Export Notes
exportOptions.exportFileData=Export Files
exportOptions.includeAnnotations=Include Annotations
exportOptions.includeAppLinks=Include %S Links
exportOptions.useJournalAbbreviation=Use Journal Abbreviation


chrome/content/zotero/xpcom/attachments.js:28
	this.LINK_MODE_IMPORTED_FILE = 0;
	this.LINK_MODE_IMPORTED_URL = 1;
	this.LINK_MODE_LINKED_FILE = 2;
	this.LINK_MODE_LINKED_URL = 3;
	this.LINK_MODE_EMBEDDED_IMAGE = 4;

chrome/content/zotero/xpcom/attachments.js:3047
		case this.LINK_MODE_IMPORTED_FILE:
			return 'imported_file';
		case this.LINK_MODE_IMPORTED_URL:
			return 'imported_url';
		case this.LINK_MODE_LINKED_FILE:
			return 'linked_file';
		case this.LINK_MODE_LINKED_URL:
			return 'linked_url';
		case this.LINK_MODE_EMBEDDED_IMAGE:
			return 'embedded_image';


## Dev

https://www.zotero.org/support/dev/translators/coding

npm i @types/node

/opt/Zotero_linux-x86_64/zotero
after each start: Help -> Debug Output Logging -> Enable

http://web.archive.org/web/20210531173818/https://developer.mozilla.org/en-US/docs/Mozilla/JavaScript_code_modules/OSFile.jsm

Symbolic Links:
http://web.archive.org/web/20150426182832/https://developer.mozilla.org/en-US/docs/Mozilla/JavaScript_code_modules/OSFile.jsm/OS.File_for_the_main_thread#OS.File.stat

https://firefox-source-docs.mozilla.org/dom/ioutils_migration.html
```
For various reasons (complexity, safety, availability of underlying system calls, usefulness, etc.) the following OS.File methods have no analogue in IOUtils. They also will not be implemented.

    void unixSymlink(in string targetPath, in string createPath)
    ...
```

Zotero.write() -> writes a line
chrome/content/zotero/xpcom/translation/translate_firefox.js:774

if header is changed, zotero need to be restarted

## Concept

Export Notes, Attachments as JSON in one Line

Then python script that creates hardlinks of all files in folder

Export:

```json
{
    "collections": IExportCollection[],
    "notes": IExportNotes[],
    "items": IExportItems[],
    "attachments": IExportAttachments[],
}
```

Attachment:

```json
{
    // collection structure
    "structure": string[],
    // path to file
    "path": string,
    // parent item if one exist
    "item?": string,
}
```

Note:

```json
{
    // collection structure
    "structure": string[],
    // content of note
    "content": string,
    // parent item if one exist
    "item?": string,
}
```

Item:

```json
{
    // collection structure
    "structure": string[],
    "item": string,
}
```

Collection:

```json
{
    // collection structure
    "structure": string[],
}
```
