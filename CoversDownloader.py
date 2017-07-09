#F del Mazo - initial commit July 2017
#https://github.com/FdelMazo/

import sys
import os
import shutil
try:
	import pip
except ImportError:
	print("You must have pip installed: Refer to https://pip.pypa.io/en/stable/installing/")
	sys.exit()

try:
	from urllib.request import urlretrieve
	from bs4 import BeautifulSoup
	import lxml
	import requests
	import string
except ImportError:
	pip.main(['install', '--user', 'beautifulSoup4'])
	pip.main(['install', '--user', 'requests'])
	pip.main(['install', '--user', 'lxml'])

def get_company():
	comp = input("Marvel or DC? ")
	while comp.upper() != "MARVEL" and comp.upper() != "DC":
		comp = input("Try again. Just write Marvel or DC: ")
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
	character_lst = character.split(' ')
	character_lst = list(map(lambda x: x.title(), character_lst))
	for link in soup.findAll('a'):
		if any(word in str(link.get('title')) for word in character_lst) and link not in possible_links:
			possible_links.append(link)
	if not possible_links:
		print("No series found")
		return deep_volume_search(company, character)
	for i,link in enumerate(possible_links,1):
		print("{} - {}".format(i, link.get('title')))
	selection = input("\n Which series? (write number or 'deep search') ")
	if selection in "deep search": return deep_volume_search(company,character)
	while not selection.isdigit() or not 0 < int(selection) <= len(possible_links):
		selection = input("Try again. Just write the number or 'deep search': ")
	selected_link = possible_links[int(selection)-1]
	return selected_link

def deep_volume_search(company, character):
	print("Deep search will be executed now. Keep in mind it's a little bit slower")
	all_letters = sorted(list(string.ascii_lowercase) + [x+'m' for x in string.ascii_lowercase])
	possible_links = []
	for letter in all_letters:
		short_url = get_searcher(company) +"{}".format(letter)
		req = requests.get(get_base(company)+short_url)
		html = req.content
		soup = BeautifulSoup(html, "lxml")
		character_lst = character.split(' ')
		character_lst = list(map(lambda x: x.title(), character_lst))
		for link in soup.findAll('a'):
			if any(word in str(link.get('title')) for word in character_lst) and link not in possible_links:
				possible_links.append(link)
	if not possible_links: raise ValueError("No series found. Try again with the other company")
	for i,link in enumerate(possible_links,1):
		print("{} - {}".format(i, link.get('title')))
	selection = input("\n Which series? (write number) ")
	while not selection.isdigit() or not 0 < int(selection) <= len(possible_links):
		selection = input("Try again. Just write the number: ")
	selected_link = possible_links[int(selection)-1]
	return selected_link	
	
def select_type(company, cbseries):
	if company == "MARVEL": return cbseries
	cbseries = cbseries.get('href')
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
	while not selection.isdigit() or not 0 < int(selection) <= len(possible_links):
		selection = input("Try again. Just write the number: ")
	selected_link = possible_links[int(selection)-1]
	return selected_link
	
def get_images(company, link):
	link = link.get('href')
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
			return title

def create_dir(link):
	link = link.get('title')
	link = link.replace('/','_').replace(':','_').replace('"','_')
	if not os.path.exists(link):
		os.mkdir(link)
	return link
	
def move(title, dir):
	shutil.move(title, dir)
	
def main():
	company = get_company()
	character = input("\n Write a character or a comicbook series: ")
	cbseries = select_volume(company, character)
	link = select_type(company, cbseries)
	images = get_images(company, link)
	dir = create_dir(link)
	for img in images:
		title = download(company, img)
		move(title, dir)
		
main()
