# ComicbookCovers
Webscraper for DC and Marvel Wikias to download CB covers.

Before getting started you must have installed BeautifulSoup, lxml and requests. To do so write in the terminal:
	- $ apt-get install python3-bs4 or $ easy_install beautifulsoup4 or $ pip install beautifulsoup4
	- $ apt-get install python-lxml or $ easy_install lxml or $ pip install lxml
	- $ pip install requests
	
This easy and light program does the following:
	- Prompts you a character name or comicbook series
	- Asks which of the found series would you like
	- Downloads every cover found in the wikia for that series
	
Important: The constant at line 9 is the one that determines which wikia the program will scrape. You must modify it if you want other results.