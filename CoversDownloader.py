#F del Mazo - initial commit July 2017

#REQS: pip install: beautifulsoup4, lxml

from urllib.request import urlopen,urlretrieve
from bs4 import BeautifulSoup

COMPANY = "DC"
BASE = "http://dc.wikia.com/"

def select_volume(character="Nightwing"):
	initial_letters = character[:2]
	short_url = "index.php?title=Category:Volumes&from={}".format(initial_letters)
	html = urlopen(BASE+short_url).read()
	soup = BeautifulSoup(html, "lxml")
	possible_links = []
	for link in soup.findAll('a'):
		if character.capitalize() in str(link.get('href')):
			possible_links.append(link)
	if not possible_links:
		raise Exception("No series found")
	for i,link in enumerate(possible_links):
		print("{} - {}".format(i, link.get('title')))
	selection = input("\n Which series? (write number) ")
	if not selection.isdigit or int(selection) > len(possible_links):
		raise ValueError("Series wrongly selected, it must be one of the numbers onscreen")
	selected_link = possible_links[int(selection)]
	return selected_link.get('href')

def select_type(cbseries):
	html = urlopen(BASE+cbseries).read()
	soup = BeautifulSoup(html, "lxml")
	possible_links = []
	for link in soup.findAll('a'):
		if "cover" in str(link.get('href')).lower():
			possible_links.append(link)
	if not possible_links:
		raise Exception("No covers found")
	for i,link in enumerate(possible_links):
		print("{} - {}".format(i, link.get('title')))
	selection = input("\n Which type of cover? (write number) ")
	if not selection.isdigit or int(selection) > len(possible_links):
		raise ValueError("Type wrongly selected, it must be one of the numbers onscreen")
	selected_link = possible_links[int(selection)]
	return selected_link.get('href')

def get_images(link):
	html = urlopen(BASE+link).read()
	soup = BeautifulSoup(html, "lxml")
	images = set()
	for link in soup.findAll('a'):
		if "File:" in str(link.get('href')):
			images.add(link.get('href'))
	if not images:
		raise Exception("No covers found")
	return images

def download(img):
	html = urlopen(img).read()
	soup = BeautifulSoup(html, "lxml")
	for link in soup.findAll('a'):
		if link.get('download') and ".jpg" in link.get('href'):
			url = link.get('href')
			index = url.index(".jpg") +4
			url = url[:index]
			title = img.split(':')[-1]
			urlretrieve(link.get('href'), title)
			print("Downloaded: {}".format(title))
			
def main():
	character = input("\n Write a character or a comicbook series: ")
	cbseries = select_volume(character)
	link = select_type(cbseries)
	images = get_images(link)
	for img in images:
		download(img)
	
main()	
	
	
	