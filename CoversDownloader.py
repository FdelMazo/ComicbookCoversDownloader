#F del Mazo - initial commit July 2017

#REQS: pip install: beautifulsoup4, lxml, requests

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests

NUMBER_IMG = 20 #Every x iterations it asks the user to keep going or not

def get_company():
	comp = input("Marvel or DC? ")
	assert comp.upper() == "MARVEL" or comp.upper() == "DC"
	return comp.upper()

def get_base(company):
	if company == "DC":
		return "http://dc.wikia.com/"
	elif company == "MARVEL":
		return "http://marvel.wikia.com/"

def get_searcher(company):
	if company == "DC":
		return "index.php?title=Category:Volumes&from="
	elif company == "MARVEL":
		return "wiki/Category:Comic_Lists?pagefrom="	
		
def get_img_link(company, img):
	if get_base(company) not in img:
		return get_base(company)+img
	else:
		return img
	
def select_volume(company, character):
	initial_letters = character[:2]
	short_url = get_searcher(company) +"{}".format(initial_letters)
	req = requests.get(get_base(company)+short_url)
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

def select_type(company, cbseries):
	if company == "MARVEL": return cbseries
	req = requests.get(get_base(company)+cbseries)
	html = req.content
	soup = BeautifulSoup(html, "lxml")
	possible_links = []
	for link in soup.findAll('a'):
		if "cover" in str(link.get('href')).lower() and not [linkx for linkx in possible_links if link.get('title') in linkx.get('title')]:
			possible_links.append(link)
	if not possible_links:
		raise Exception("No covers found")
	for i,link in enumerate(possible_links,1):
		print("{} - {}".format(i, link.get('title')))
	selection = input("\n Which type of cover? (write number) ")
	assert selection.isdigit() or 0 <= int(selection) < len(possible_links)
	selected_link = possible_links[int(selection)-1]
	return selected_link.get('href')

def get_images(company, link):
	req = requests.get(get_base(company)+link)
	html = req.content
	soup = BeautifulSoup(html, "lxml")
	images = []
	for link in soup.findAll('a'):
		if "File:" in str(link.get('href')):
			if link.get('href') not in images: images.append(link.get('href'))
	if not images:
		raise Exception("No covers found")
	return images

def download(company, img):
	req = requests.get(get_img_link(company, img))
	print(get_img_link(company,img))
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
	company = get_company()
	character = input("\n Write a character or a comicbook series: ")
	cbseries = select_volume(company, character)
	link = select_type(company, cbseries)
	images = get_images(company, link)
	keepgoing = True
	counter = 0
	while keepgoing:
		for i in range(counter,counter+NUMBER_IMG):
			if i<len(images): download(company,images[i])
		selection = input("Keep going? (y/n) ")
		if selection.lower() == "y": 
			keepgoingepgoing = True
			counter+=1
		else:
			keepgoing = False
		
main()	
	
	
	