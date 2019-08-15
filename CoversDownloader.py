from Wikias import *
import os
import shutil
import logging
import argparse

INVALID_CHARACTERS = '/?<>\:*|" ' #Windows


def select_link(possible_links, flags):
	if len(possible_links) == 0:
		logging.warning("No series found")
		return False, False
	elif len(possible_links) == 1 or flags.get('no_confirm'):
		selected_link = possible_links[0]
	else:
		for i, tuple in enumerate(possible_links, 1):
			print("\t {:<3} -  {}".format(i, tuple[1].get('title').replace("Category:",'').replace("/",' ')))
		logging.debug("Press return to stop ")
		selection = input("\n Which series? [Number] ").lower()
		while not selection.isdigit() or not 0 < int(selection) <= len(possible_links) and selection != "":
			if not selection:
				logging.warning("User canceled action")
				return False
			selection = input("Just write the number: ").lower()
		selected_link = possible_links[int(selection) - 1]
	return selected_link

def get_cover_type(wiki, cbseries, flags):
	if not wiki.bool_cover_type: return cbseries
	possible_links = []
	soup = request_soup(wiki.fix_link(cbseries.get('href')))
	for link in soup.findAll('a',title=True,href=True):
		if "Cover" in link.get('href') and not [linkx for linkx in possible_links if link.get('title') in linkx[1].get('title')]:
			possible_links.append((wiki,link))
	return select_link(possible_links, flags)

def download_series(search_terms=None, flags=None):
	if not search_terms: search_terms = input("\n Write a comicbook series: ")
	wiki = get_wiki()
	possible_links = wiki.category_to_pages(search_terms)
	wiki, link = select_link(possible_links, flags)
	wiki, link = get_cover_type(wiki, link, flags)
	if not link: return False, False
	images = wiki.gallery_to_list_img(link.get('href'))
	return wiki, link, images

def manage(wiki, link, images, dry_run):
	dir_name = link.get('title').replace('Category','').strip()
	dir_name = "Covers/" + ''.join(list(c if c not in INVALID_CHARACTERS else "_" for c in dir_name)).strip('_')
	os.makedirs(os.path.join(wiki.title,dir_name), exist_ok=True)
	for img in images:
		filename = wiki.download_jpg(img)
		if filename: 
			try: shutil.move(filename, os.path.join(wiki.title,dir_name))
			except: pass

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('command_line_series',help='Series can be called from the CLA', nargs='?', action = 'store', default = None)
	parser.add_argument('-y', '--no-confirm', help='No confirmation required from you', action='append_const', const=("no_confirm",True), dest='flags')
	parser.add_argument('--dry-run', help='Only show what would be done without modifying files', action='append_const', const=("dry_run",True), dest='flags')
	parser.add_argument('-l', '--log', help='Log everything to PosterDownloader.log', action='store_true')
	parser.add_argument('-v', '--verbose', help='Verbose/Debug logging', action='store_const', const=logging.DEBUG, dest='loglevel')
	args = parser.parse_args()
	flags = dict(args.flags) if args.flags else {}

	superformat = '%(levelname)s: %(message)s - %(funcName)s() at %(filename)s.%(lineno)d'
	if args.log:
		console = logging.StreamHandler()
		console.setLevel(args.loglevel or logging.INFO)
		console.setFormatter(logging.Formatter(superformat))
		logging.basicConfig(level=logging.DEBUG, format=superformat, filename='CoversDownloader.log')
		logging.getLogger('').addHandler(console)
	elif args.loglevel:
		logging.basicConfig(level=args.loglevel, format=superformat)
	else:
		logging.basicConfig(level=logging.INFO, format='%(message)s')
	logging.getLogger("requests").setLevel(logging.WARNING)
	try:
		wiki, link, images = download_series(args.command_line_series, flags)
		if link and images: manage(wiki, link, images, flags.get('dry_run'))
	except KeyboardInterrupt:
		logging.error('KeyboardInterrupt')
		pass

main()
