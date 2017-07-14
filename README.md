# ComicbookCovers
Webscraper for DC, Marvel and more Comicbook Wikias to download CB covers.
Currently works with the wikias of: DC, Marvel, Dark Horse, Image, Valiant, Dynamite
Currently finds covers for: Comicbook Series, Characters, Artists and Solicitations

This easy and light program does the following:
* Asks you if you want to find covers for a Character, Series, Artist or Month of solicitations
* Asks which of the found series would you like
* Downloads every cover found in the wikia for that series

Windows and Linux users:
* Download from 'releases' the latest one and extract everything
* After that, just start the CoversDownloader.exe (Windows) or write ./CoversDownloader in the terminal (Linux)

If you want to tweak and see the source code (Python 3.6):
* Just download from the repo page both "CoversDownloader.py" and "Wikias.py" and start with 'python CoversDownloader.py'
* Keep in mind you need pip (default in Py3.4 onwards) and: requests, bs4 and lxml

Keep in mind, I don't encourage downloading several times in a short time span, as the wikias tend to get angry when you request them so many images at once. Try to space out your downloads
