# ComicbookCovers
Webscraper for DC, Marvel and more Comicbook Wikias to download CB covers.

Currently works with the wikias of: DC, Marvel, Dark Horse, Image, Valiant, Dynamite

## Installation

### Python script:
* Clone repo `git clone https://github.com/FdelMazo/ComicbookCoversDownloader.git`
* Install the dependencies `python setup.py install`
* Execute `python CoversDownloader.py`

### Executable (Windows & Linux):
* Download the latest executable from ['releases'](https://github.com/FdelMazo/ComicbookCoversDownloader/releases)
* After that, just start the ComicbookCovers.exe (Windows) or write `./ComicbookCovers` in the terminal (Linux)
    * Executables are generated with [PyInstaller](http://www.pyinstaller.org/) by just writing `pyinstaller CoversDownloader.py -F`

## Usage (as Python script)

`python CoversDownloader.py ["Robin"] -flags` with ["Comicbook Series"] being optional and the -flags being:

* `-h, --help`            Show this help message and exit
* `-y, --no-confirm`      No confirmation required from you
* `--dry-run`             Only show what would be done, without modifying files
* `-l, --log`             Log everything to CoversDownloader.log
* `-v, --verbose`         Verbose/Debug logging
