#F del Mazo - initial commit July 2017
#https://github.com/FdelMazo/
#federicodelmazo@hotmail.com

from Wikias import *
import sys
import os
import shutil

INVALID_CHARACTERS = '/?<>\:*|" ' #Windows

"""COMMAND: CHARACTER / SERIES"""	
def get_cbseries(wikis, search_terms, any_all):
	possible_links, counter = [], 1
	for wiki in wikis:
		try:
			possible_wiki_links = wiki.category_to_pages("Volume", search_terms, any_all)
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
	if len(possible_links)==1: return possible_links[0]
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

def character_or_series(any_all, term):
	search_terms = input("\n Write a comicbook {}: ".format(term))
	wikis = get_wikis()
	wiki, cbseries = get_cbseries(wikis, search_terms, any_all)
	if not cbseries: return
	link = get_cover_type(wiki, cbseries)
	if not link: return
	images = wiki.gallery_to_list_img(link.get('href'))
	if not images: return
	dir_name = link.get('title').replace('Category','')
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
	character_or_series(any, "Character")

def series():
	character_or_series(all, "Series")	

"""ARTIST"""
def fix_artist_name(link):
		artist_name = link.get('title')
		if "/" in artist_name:
			artist_name = artist_name[:artist_name.index("/")]
		if ":" in artist_name:
			artist_name = artist_name[artist_name.index(":")+1:]
		return artist_name

def artist_or_artistlink(wikis, artist, search_type):
	possible_artists = []
	for wiki in wikis:
		try:
			possible_wiki_links = wiki.category_to_pages("Artist", artist, all)
		except ConnectionError as e:
			print(e)
			continue
		for wiki,link in possible_wiki_links:
			if search_type=="Artist":
				if fix_artist_name(link) not in possible_artists: 
					possible_artists.append((wiki,fix_artist_name(link)))
			if search_type=="Artist Link":
				possible_artists.append((wiki,link))
	if len(possible_artists)==1: return possible_artists[0]
	for i,artist in enumerate(possible_artists,1):
		print("{} - {}".format(i, artist))
	if not possible_artists:
		print("No artists found")
		return False,False	
	selection = input("\n Which artist? (write number or 'skip') ").lower()
	while not selection.isdigit() or not 0 < int(selection) <= len(possible_artists) and selection not in "skip":
		if selection in "skip":	return False,False
		selection = input("Try again. Just write the number or 'skip': ").lower()
	artist_name = possible_artists[int(selection)-1]
	return artist_name		
	
def artist():
	artist_sel = input("\n Write a cover artist, can be name, surname or both: ")
	wikis = [Wiki_Crawler(comp) for comp in COMPANIES]
	artist = artist_or_artistlink(wikis, artist_sel, "Artist")[1]
	if not artist: return
	print("\n {} found!".format(artist))
	for wiki in wikis:
		artist_link= artist_or_artistlink([wiki], artist, "Artist Link")[1]
		issues = wiki.category_to_pages("Issues","Vol",all, url=artist_link.get('href'))
		dir_name=os.path.join(artist.replace(' ','_'), wiki.title)
		os.makedirs(dir_name, exist_ok=True)
		for issue in issues:
			img = wiki.issue_to_cover(issue[1].get('href'))
			if img:
				filename = img.split('/')[-1]
				r = requests.get(img)
				with open(filename, "wb") as f:
					f.write(r.content)
				print("Downloaded: {}".format(filename))
				try:
					shutil.move(filename, dir_name)
				except:
					pass
			
"""SOLICITATIONS"""

	
"""UNIVERSAL"""				
def menu():
	functions = {}
	functions["Character"] = character
	functions["Series"] = series
	functions["Artist"] = artist
	# functions["Solicitations"] = solicitations
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