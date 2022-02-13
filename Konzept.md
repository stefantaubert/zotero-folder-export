
Optionen:

- Inkludiere: Anhänge, Notizen, Kollektionen, Einträge

## Python

In Python wird das exportierte JSON gelesen und die Daten exportiert.

### Kollektionen

Jede Kollektion wird als Ordner erstellt.

### Einträge

Jeder Eintrag wird als Ordner erstellt.

Optionen:

- Format: Ordner, Datei ohne Extension

### Notizen

Jede Notiz wird als Datei exportiert.

Optionen:

- Format: `html`, `txt`
  - bei `txt` wird nur der reine Text exportiert
- Modus: erste Zeile und bei leeren Notizen (nur Whitespace) den Standardname, immer Standardname
- Name: Standardname einer Notiz, standardmäßig `note`

### Anhänge

Jede Datei wird exportiert.

Optionen:

- Modus: Kopieren, Symbolischer Link, Hardlink+Symbolischer Link,
  - Verschieben wird nicht unterstützt, da es zu zu großen Problemen führt
- Modus Duplikate nur bei Modus Kopieren: Kopieren, Hardlink
- Angabe, ob Dateien die mit im Ordner liegen ebenfalls exportiert werden sollen
  - Dateinamen, die ignoriert werden sollen. Standardmäßig `.zotero-ft-cache`, `.zotero-ft-info`
- Modus Eintragsordner:
  - Immer: immer einen Eintragsordner erstellen (Standard)
  - Immer, außer bei einzelnen Anhängen: nur einen Eintragsordner erstellen wenn es mehr als eine Datei ist
  - Immer, außer bei einzelnen Anhängen, wenn der Name nicht äquivalent zum Dateiname ist (mit/ohne Endung)
  - Nie: keinen Eintragsordner erstellen
- Angabe, ob der Eintrags-Ordner (falls ein Eintrag existiert) nicht erstellt werden soll, wenn der Name des Eintrags äquivalent zum Dateiname ist oder der Dateiname ohne Ende ist und nur eine Datei dem Eintrag zugeordnet ist (inkl. der Dateien im Ordner).

Eintragszieldateien sind:

- Anhänge
- Dateien neben den Anhängen im gleichen Ordner (ignorierte werden nicht mitgezählt)
- Notizen

### Generell

Optionen:

- Pfad zur `json`-Datei
- Encoding der Datei. Standard: UTF-8
- Zielverzeichnis
- Angabe, ob das Zielverzeichnis überschrieben werden darf
