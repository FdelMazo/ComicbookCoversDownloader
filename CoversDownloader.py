#F del Mazo - initial commit July 2017

#REQS: pip install: beautifulsoup4, lxml, requests

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests

COMPANY = "MARVEL"
if COMPANY == "DC":
	BASE = "http://dc.wikia.com/"
	VOLUME_SEARCHER = "index.php?title=Category:Volumes&from="
	
if COMPANY == "MARVEL":
	BASE = "http://marvel.wikia.com/"
	VOLUME_SEARCHER = "/wiki/Category:Comic_Lists?pagefrom="

NUMBER_IMG = 20 #Every x iterations it asks the user to keep going or not


def select_volume(character):
	initial_letters = character[:2]
	short_url = VOLUME_SEARCHER +"{}".format(initial_letters)
	req = requests.get(BASE+short_url)
	html = req.content
	soup = BeautifulSoup(html, "lxml")
	possible_links = []
	for link in soup.findAll('a'):
		if character.title() in str(link.get('title')) and link not in possible_links:
			possible_links.append(link)
	if not possible_links:
		raise Exception("No series found")
	for i,link in enumerate(possible_links,1):
		print("{} - {}".format(i, link.get('title')))
	selection = input("\n Which series? (write number) ")
	assert selection.isdigit() or 0 <= int(selection) < len(possible_links)
	selected_link = possible_links[int(selection)-1]
	return selected_link.get('href')

def select_type(cbseries):
	if COMPANY == "MARVEL": return cbseries
	req = requests.get(BASE+cbseries)
	html = req.content
	soup = BeautifulSoup(html, "lxml")
	possible_links = []
	for link in soup.findAll('a'):
		if "cover" in str(link.get('href')).lower() and link not in possible_links:
			possible_links.append(link)
	if not possible_links:
		raise Exception("No covers found")
	for i,link in enumerate(possible_links,1):
		print("{} - {}".format(i, link.get('title')))
	selection = input("\n Which type of cover? (write number) ")
	assert selection.isdigit() or 0 <= int(selection) < len(possible_links)
	selected_link = possible_links[int(selection)-1]
	return selected_link.get('href')

def get_images(link):
	req = requests.get(BASE+link)
	html = req.content
	soup = BeautifulSoup(html, "lxml")
	images = []
	for link in soup.findAll('a'):
		if "File:" in str(link.get('href')):
			if link.get('href') not in images: images.append(link.get('href'))
	if not images:
		raise Exception("No covers found")
	return images

def download(img):
	req = requests.get(BASE+img)
	html = req.content
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
	keepgoing = True
	counter = 0
	while keepgoing:
		for i in range(counter,counter+NUMBER_IMG):
			if(images[i]): download(images[i])
		selection = input("Downloaded {} images. Keepgoing? (y/n) ".format(NUMBER_IMG))
		if selection.lower() == "y": 
			keepgoingepgoing = True
			counter+=1
		else:
			keepgoing = False
		
main()	
	
	
	