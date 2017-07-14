#F del Mazo - initial commit July 2017
#https://github.com/FdelMazo/
#federicodelmazo@hotmail.com

from Wikias import *
import sys
import os
import shutil

INVALID_CHARACTERS = '/?<>\:*|" ' #Windows

def get_cbseries(wikis, search_type, search_terms, any_all):
	possible_links, counter = [], 1
	for wiki in wikis:
		try:
			possible_wiki_links = wiki.category_to_pages(search_type, search_terms, any_all)
		except ConnectionError as e:
			print(e)
			continue
		if not possible_wiki_links:
			print("Nothing found on the {} wiki".format(wiki))
			continue
		possible_links.extend(possible_wiki_links)
		print("\n From The {} wiki:".format(wiki))
		for i,tuple in enumerate(possible_wiki_links,counter):
			print("{} - {}".format(i, tuple[1].get('title')))
		counter +=len(possible_wiki_links)
	if not possible_links:
		print("No series found")
		return False,False	
	if len(possible_links)==1:
		print("\n {} selected \n".format(possible_links[0][1].get('title')))
		return possible_links[0]
	selection = input("\n Which series? (write number or 'skip') ").lower()
	while not selection.isdigit() or not 0 < int(selection) <= len(possible_links) and selection not in "skip":
		if selection in "skip":	return False,False
		selection = input("Try again. Just write the number or 'skip': ").lower()
	selected_link = possible_links[int(selection)-1]
	return selected_link	
	
def get_cover_type(wiki, cbseries):
	if not wiki.bool_cover_type: return cbseries
	possible_links = []
	cbseries = cbseries.get('href')
	try:
		soup = request_soup(wiki.fix_link(cbseries))	
	except ConnectionError as e:
		print(e)
		return False
	for link in soup.findAll('a',title=True,href=True):
		if "Cover" in link.get('href') and not [linkx for linkx in possible_links if link.get('title') in linkx.get('title')]:
			possible_links.append(link)
	if not possible_links:
		print("No covers found")
		return False
	if len(possible_links)==1: return possible_links[0]
	for i,link in enumerate(possible_links,1):
		print("{} - {}".format(i, link.get('title').replace("Category:",'').replace("/",' ')))
	selection = input("\n Which type of cover? (write number) ")
	while not selection.isdigit() or not 0 < int(selection) <= len(possible_links):
		selection = input("Try again. Just write the number: ")
	selected_link = possible_links[int(selection)-1]
	return selected_link

def character_or_series(search_type, any_all, term):
	search_terms = input("\n Write a comicbook {}: ".format(term))
	if search_type=="Series" or search_type=="Character":
		wikis = get_wikis(True)
	elif search_type=="Artist":
		wikis = get_wikis(False)
	wiki, link = get_cbseries(wikis, search_type, search_terms, any_all)
	if not link: return
	if search_type=="Series" or search_type=="Character":
		link = get_cover_type(wiki, link)
	if not link: return
	images = wiki.gallery_to_list_img(link.get('href'))
	if not images: return
	dir_name = link.get('title').replace('Category','').strip()
	dir_name = ''.join(list(c if c not in INVALID_CHARACTERS else "_" for c in dir_name))
	os.makedirs(os.path.join(wiki.title,dir_name), exist_ok=True)
	for img in images:
		filename = wiki.download_jpg(img)
		if filename: 
			try:
				shutil.move(filename, os.path.join(wiki.title,dir_name))
			except:
				pass

def character():
	character_or_series("Volume", any, "Character")

def series():
	character_or_series("Volume", all, "Series")

def artist():
	character_or_series("Artist", all, "Artist")		
	
def solicitations():
	solicits = input("\n Write a solicitation with COMPANY, MONTH, YEAR: ")
	link = cbr_solicitation_crawler(solicits)
	soup = request_soup(link.get('href'))
	if soup:
		dir_name=soup.title.string
		os.makedirs(dir_name,exist_ok=True)
		images = []
		for div in soup.findAll("div",{"class":"responsiveImg img_article_content"}):
			comic_name = str(div.next_sibling.next_sibling.next_sibling.string)
			comic_name = ''.join(list(c if c not in INVALID_CHARACTERS else "_" for c in comic_name)).title()
			comic_name+=".jpg"
			for picture in div.picture.findAll("source"):
				img = picture["srcset"]
				index = img.index(".jpg") +4
				img = img[:index]
				if (comic_name,img) not in images: images.append((comic_name,img))
		for comic_name,img in images:
			r = requests.get(img)
			with open(comic_name, "wb") as f:
				f.write(r.content)
			print("Downloaded: {}".format(comic_name))
			try:
				shutil.move(comic_name, dir_name)
			except:
				pass			
	
"""UNIVERSAL"""				
def menu():
	functions = {}
	functions["Character"] = character
	functions["Series"] = series
	functions["Artist"] = artist
	functions["Solicitations"] = solicitations
	return functions
		
def main():
	flag = "run"
	while flag == "run":
		try:
			commands = list(menu().keys())
			sel = input("\n Choose the source for the covers from {}: ".format(', '.join(commands))).title()
			while not sel in commands:
				sel = input("Just write one of this keywords: {} \n\t".format(', '.join(commands))).title()
			menu()[sel]()
		except KeyboardInterrupt:
			pass
		flag = input("\nPress any key to exit or 'run' to run again: ").lower()	
		
main()