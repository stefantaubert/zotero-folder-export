const fs = require('fs')

const body = fs.readFileSync('dist/export-json.js', 'utf-8')
const header = JSON.stringify({
  'translatorID': '86ffd88b-6f4e-4bec-a5be-839c1034beb3',
  'label': 'Export as JSON',
  'description': 'Export JSON file containing details about collections, notes, items and attachments.',
  'creator': 'Stefan Taubert',
  'target': 'json',
  'minVersion': '4.0.27',
  'maxVersion': '',
  'configOptions': {
		'getCollections': true,
  },
  'displayOptions': {
		"exportCharset": "UTF-8xBOM",
  },
  'translatorType': 2,
  'browserSupport': 'gcsv',
  'priority': 100,
  'inRepository': true,
  'lastUpdated': fs.statSync('export-json.ts').mtime.toISOString().replace('T', ' ').replace(/\..*/, ''),
}, null, 2)

fs.writeFileSync('dist/export-json.js', header + '\n\n' + body)
