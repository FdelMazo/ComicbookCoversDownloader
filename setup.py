#F del Mazo - initial commit July 2017
#https://github.com/FdelMazo/
#federicodelmazo@hotmail.com

from cx_Freeze import setup, Executable

build_exe_options = {
	"packages": ["bs4", "sys", "shutil", "lxml", "os", "requests", "queue", "idna"],
	"includes": ["Wikias"]
	}

setup(  name = "Comicbook Covers Downloader",
        version = "1.2",
        description = "Webscraper for Comicbook Wikias to download CB covers",
        author = 'F del Mazo',
		author_email = 'federicodelmazo@hotmail.com',
		url = 'https://github.com/FdelMazo/ComicbookCovers/releases',
		options = {"build_exe": build_exe_options},
        executables = [Executable("CoversDownloader.py")]
)