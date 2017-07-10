#F del Mazo - initial commit July 2017
#https://github.com/FdelMazo/
#federicodelmazo@hotmail.com

from Wikias import Wiki, COMPANIES
import sys
import os
import shutil
from bs4 import BeautifulSoup
import lxml
import requests

def request_soup(url):
	try:
		req = requests.get(url)
		html = req.content
		soup = BeautifulSoup(html, "lxml")
	except requests.exceptions.ConnectionError:
		raise ConnectionError("Connection refused. Try again in a few minutes")
	return soup
	
def volume_search_per_url(wiki, character, short_url=None):
	possible_letter_links = []
	if short_url == None: short_url = wiki.volume_search +"{}".format("'")
	short_url = wiki.fix_link(short_url)
	next_shorturl = False
	soup = request_soup(wiki.fix_link(short_url))
	character_lst = character.split(' ')
	character_lst = list(map(lambda x: x.title(), character_lst))
	for link in soup.findAll('a',title=True,href=True):
		if any(word in str(link.get('title')) for word in character_lst):
			possible_letter_links.append((wiki, link))
		if 'next 200' in link:
			next_shorturl = link.get('href')
	return next_shorturl, possible_letter_links
		
def volume_search(wikis, character):
	possible_links = []
	counter = 1
	for wiki in wikis:
		possible_local_links = []
		print("Currently searching in the {} Wiki".format(wiki))
		next_url, list = volume_search_per_url(wiki,character)
		if list: possible_local_links.extend(list)
		while next_url:
			possible_local_links.extend(list)
			next_url, list = volume_search_per_url(wiki,character,next_url)
		if not possible_local_links:
			print("No series or characters found in the {} wiki".format(wiki))
			break
		possible_links.extend(possible_local_links)
		print("\n From The {} wiki:".format(wiki))
		for i,tuple in enumerate(possible_local_links,counter):
			link = tuple[1]
			print("{} - {}".format(i, link.get('title')))
		counter +=len(possible_local_links)
	if not possible_links:
		print("No series found")
		return False,False	
	selection = input("\n Which series? (write number) ")
	if selection.lower() in "skip":	return False,False
	while not selection.isdigit() or not 0 < int(selection) <= len(possible_links):
		selection = input("Try again. Just write the number: ")
	selected_link = possible_links[int(selection)-1]
	return selected_link	
	
def select_type(wiki, cbseries):
	possible_links = []
	if not wiki.bool_type: return cbseries
	cbseries = cbseries.get('href')
	soup = request_soup(wiki.fix_link(cbseries))	
	for link in soup.findAll('a',title=True,href=True):
		if "cover" in str(link.get('href')).lower() and not [linkx for linkx in possible_links if link.get('title') in linkx.get('title')]:
			possible_links.append(link)
	if not possible_links:
		print("No covers found")
		return False
	for i,link in enumerate(possible_links,1):
		print("{} - {}".format(i, fix_name(link.get('title'))))
	selection = input("\n Which type of cover? (write number) ")
	while not selection.isdigit() or not 0 < int(selection) <= len(possible_links):
		selection = input("Try again. Just write the number: ")
	selected_link = possible_links[int(selection)-1]
	return selected_link
	
def get_images(wiki, link):
	link = link.get('href')+"?display=page"
	soup = request_soup(wiki.fix_link(link))
	images = []
	for link in soup.findAll('a',title=True,href=True):
		print(link.get('href'))
		if "File:" in str(link.get('href')):
			if link.get('href') not in images: images.append(link.get('href'))
	if not images:
		print("No covers found")
		return False
	return images

def download(wiki, img):
	soup = request_soup(wiki.fix_link(img))
	url = ""
	for link in soup.findAll('a',href=True,download=True):
		if ".jpg" in link.get('href'):
			url = link.get('href')
			index = url.index(".jpg") +4
			url = url[:index]
			filename = img.split(':')[-1]
			r = requests.get(url)
			with open(filename, "wb") as f:
				f.write(r.content)
			print("Downloaded: {}".format(filename))
			return filename
	return False

def fix_name(name):
	name = name.replace('/',' ').replace(':',' ').replace('"',' ').replace(' ',' ').strip()
	name = name.split(' ')
	if "Category" in name:
		dir.remove("Category")
	return ' '.join(name)
			
def create_dir(wiki, link):
	link = link.get('title')
	link = fix_name(link).replace(' ','_')
	dir = os.path.join(wiki.title,link)
	if not os.path.exists(dir):
		if not os.path.exists(wiki.title):
			os.mkdir(wiki.title)
		os.mkdir(dir)
	return dir
	
def move(title, dir):
	try:
		shutil.move(title, dir)
	except:
		pass
	
def main():
	character = input("\n Write a character or a comicbook series: ")
	company_sel = [input("\n Which company? {} or ALL: ".format(', '.join(COMPANIES)))]
	while company_sel[0].upper() not in COMPANIES and company_sel[0].upper() != "ALL":
		company_sel = [input("\n No company with that name. Try again: ".format(', '.join(COMPANIES)))]
	if company_sel[0].upper() == "ALL": company_sel = COMPANIES
	wikis = []
	for company in company_sel:
		wikis.append(Wiki(company))
	wiki, cbseries = volume_search(wikis, character)
	if not cbseries: return
	link = select_type(wiki, cbseries)
	if not link: return
	images = get_images(wiki, link)
	if not images: return
	dir = create_dir(wiki, link)
	for img in images:
		title = download(wiki, img)
		if title: move(title, dir)
	
flag = "run"
while flag == "run":
	main()
	flag = input("Press any key to exit or 'run' to run again: ")	