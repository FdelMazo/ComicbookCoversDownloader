# ComicbookCovers
Webscraper for DC, Marvel and more Comicbook Wikias to download CB covers.

Currently works with the wikias of: DC, Marvel, Dark Horse, Image, Valiant, Dynamite

## Installation & Quick Usage

### Executable:
* Download the latest executable from ['releases'](https://github.com/FdelMazo/ComicbookCoversDownloader/releases)
* After that, just start the ComicbookCovers.exe (Windows) or write `./ComicbookCovers` in the terminal (Linux)
    * Executables are generated with [PyInstaller](http://www.pyinstaller.org/) by just writing `pyinstaller CoversDownloader.py -F`

### Python script:
* Clone repo `git clone https://github.com/FdelMazo/ComicbookCoversDownloader.git`
* Install the dependencies `python setup.py install`
* Execute `python CoversDownloader.py`
    
## Complete options (Only when run on terminal):

`python CoversDownloader.py ["Robin"] -flags` with ["Comicbook Series"] being optional and the -flags being:

* `-h, --help`            Show this help message and exit
* `-y, --no-confirm`      No confirmation required from you
* `--dry-run`             Only show what would be done, without modifying files
* `-l, --log`             Log everything to CoversDownloader.log
* `-v, --verbose`         Verbose/Debug logging

## I have a problem! How can I contact you?

The easiest would be for you to describe your problem to me in the [issues](https://github.com/FdelMazo/comicbookcoversdownloader/issues) section. To make it even easier you could replicate your error (search the same covers, etc etc) but this time logging it:
`Python CoversDownloader.py --log`

Also see:

* Solicitations downloader: https://gist.github.com/FdelMazo/de6137eef33a27b10183075f356ce741
* Movie Poster Downloader: https://github.com/FdelMazo/PosterDownloader