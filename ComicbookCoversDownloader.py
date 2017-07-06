from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
from time import sleep

def thumbs(url): 
	html = urlopen(url).read()
	soup = BeautifulSoup(html, "lxml")
	images =[]
	for link in soup.findAll('a'):
		images.append(link.get('href'))
	to_download = []
	for img in images:
		if "thumb" in str(img) or "score" in str(img):
			continue
		if "jpg" in str(img) and "Vol" in str(img):
			to_download.append(img)
	for url in to_download:
		download(lista_imagenes(url,1))
	
			
def lista_imagenes(url, variants=0):
	html = urlopen(url).read()
	soup = BeautifulSoup(html, "lxml")
	images =[]
	for img in soup.findAll('img'):
		images.append(img.get('src'))
	to_download = []
	for img in images:
		string = str(img).upper()
		if "THUMB" in string or "SCORE" in string:
			continue
		if "JPG" in string and "VOL" in string:
			if variants == 1:
				if "VARIANT" in string or "TEXTLESS" in strING:
					index = string.index("JPG")
					img = img[:index+3]
					to_download.append(img)
			else:
				index = string.index("JPG")
				img = img[:index+3]
				to_download.append(img)
	return to_download

def download(lista):
	for img in lista:
		print(img)
		urlretrieve("{}".format(img), img.split("/")[-1])
	print("Done!")
		
tipo = input("Galeria normal o the thumbs? (1 o 2) ")
if tipo == "1":
	download(lista_imagenes(input("link: ")))
if tipo == "2":
	thumbs(input("link: "))

