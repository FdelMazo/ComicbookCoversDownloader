#F del Mazo - initial commit July 2017
#https://github.com/FdelMazo/
#federicodelmazo@hotmail.com

import requests
from bs4 import BeautifulSoup
import logging


COMPANIES = {
	#Company: BaseSite, Volume Category, Bool divided by cover type
	"DC":("http://dc.wikia.com/","wiki/Category:Volumes", True),
	"MARVEL":("http://marvel.wikia.com/","wiki/Category:Comic_Lists",False),
	"VALIANT":("http://valiant.wikia.com/","wiki/Category:Volumes",False),
	"DARK HORSE":("http://darkhorse.wikia.com/","wiki/Category:Comic_Lists",False),
	"IMAGE":("http://imagecomics.wikia.com/","wiki/Category:Comic_Lists",False),
	"DYNAMITE":("http://dynamiteentertainment.wikia.com/","wiki/Category:Comic_Lists",False)
	}

def get_wiki():
	company_sel = input("\n Which company? {}: ".format(', '.join(COMPANIES))).upper()
	while company_sel not in COMPANIES:
		company_sel = input("\n No company with that name. Try again: ".format(', '.join(COMPANIES))).upper()
	return Wiki_Crawler(company_sel)

def request_soup(url):
	try:
		req = requests.get(url)
		html = req.content
		soup = BeautifulSoup(html, "lxml")
	except requests.exceptions.ConnectionError:
		logging.error("Connection with {} refused. Try again in a few minutes".format(url))
		raise ConnectionError()
	return soup

class Wiki_Crawler:
	def __init__(self, company):
		assert company in COMPANIES
		self.title = company
		self.site = COMPANIES[self.title][0]
		self.volume = COMPANIES[self.title][1]
		self.bool_cover_type = COMPANIES[self.title][2]

	def fix_link(self, link):
		if "vignette" in link:	return link
		if self.site not in link: return self.site+link+"?display=page"
		return link+"?display=page"
	
	def category_to_pages(self, search_terms, url=None, links=[]):
		if url == None: url = self.volume
		search_terms = search_terms.lower().strip()
		soup = request_soup(self.fix_link(url))
		next_shorturl = False
		for link in soup.findAll('a',title=True,href=True):
			if all(word in link.get('title').lower() for word in search_terms.split(' ')):
				if (self,link) not in links: links.append((self,link))
				if search_terms == link.get('title').lower(): return [(self, link)]
			if not next_shorturl and 'next 200' in link:
				next_shorturl = link.get('href')
		if not next_shorturl: return links
		return self.category_to_pages(search_terms, next_shorturl, links)
	
	def gallery_to_list_img(self, link):
		soup = request_soup(self.fix_link(link))
		images = []
		for link in soup.findAll('a',title=True,href=True):
			if "File:" in link.get('href'):
				if link.get('href') not in images: images.append(link.get('href'))
		if not images:
			logging.warning("No covers found")
		return images

	def issue_to_cover(self, link):
		try:
			soup = request_soup(self.fix_link(link))
		except ConnectionError as e:
			print(e)
			return False
		for link in soup.findAll('a',title=True,href=True):
			if ".jpg" in link.get('href'):
				return '/'.join(link.get('href').split('/')[:-2])
		return False
		
	def download_jpg(self, img):
		try:
			soup = request_soup(self.fix_link(img))
		except ConnectionError as e:
			print(e)
			return False
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
		try:
			soup = request_soup(self.fix_link(img))
		except ConnectionError as e:
			print(e)
			return False
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
		

def cbr_solicitation_crawler(search_terms, links=[], counter=0):
	url = "http://www.cbr.com/tag/solicitations/page/{}".format(counter)
	search_terms = search_terms.lower().strip()
	soup = request_soup(url)

	for link in soup.findAll('a',title=True,href=True):
		if all(word in link.get('title').lower() for word in search_terms.split(' ')):
			return link
	counter+=1
	return cbr_solicitation_crawler(search_terms, links, counter)
		
		
