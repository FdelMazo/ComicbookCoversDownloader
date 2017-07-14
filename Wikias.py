#F del Mazo - initial commit July 2017
#https://github.com/FdelMazo/
#federicodelmazo@hotmail.com

import requests
from bs4 import BeautifulSoup


COMPANIES = {
	#Company: BaseSite, Volume Category, Artist Category, Bool Cover Type
	"DC":("http://dc.wikia.com/","wiki/Category:Volumes","wiki/Category:Images/Cover_Artist", True),
	"MARVEL":("http://marvel.wikia.com/","wiki/Category:Comic_Lists","wiki/Category:Cover_Artist_Galleries",False),
	"VALIANT":("http://valiant.wikia.com/","wiki/Category:Volumes",False),
	"DARK HORSE":("http://darkhorse.wikia.com/","wiki/Category:Comic_Lists","wiki/Category:Cover_Artists",False),
	"IMAGE":("http://imagecomics.wikia.com/","wiki/Category:Comic_Lists","wiki/Category:Cover_Artist_Galleries",False),
	"DYNAMITE":("http://dynamiteentertainment.wikia.com/", "wiki/Category:Comic_Lists","wiki/Category:Cover_Artists","wiki/Category:Cover_Artists",False)
	}

	
def get_wikis(bool):
	all = "or ALL" if bool else ""
	company_sel = [input("\n Which company? {} {}: ".format(', '.join(COMPANIES),all)).upper()]
	while company_sel[0] not in COMPANIES and company_sel[0] != "ALL":
		company_sel = [input("\n No company with that name. Try again: ".format(', '.join(COMPANIES)))]
	if bool and company_sel[0] == "ALL": company_sel = COMPANIES
	wikis = [Wiki_Crawler(comp) for comp in company_sel]
	return wikis

def request_soup(url):
	try:
		req = requests.get(url)
		html = req.content
		soup = BeautifulSoup(html, "lxml")
	except requests.exceptions.ConnectionError:
		raise ConnectionError("Connection with {} refused. Try again in a few minutes".format(url))
	return soup

class Wiki_Crawler:
	def __init__(self, company):
		assert company in COMPANIES
		self.title = company
		self.site = COMPANIES[self.title][0]
		self.categories = {'Volume': COMPANIES[self.title][1], 'Artist': COMPANIES[self.title][2]}
		self.bool_cover_type = COMPANIES[self.title][3]
	
	def __repr__(self):
		return self.title
	
	def fix_link(self, link):
		if "vignette" in link:
			return link
		if self.site not in link:
			return self.site+link+"?display=page"
		else:
			return link+"?display=page"
	
	def category_to_pages(self, category, search_terms, any_all, url=None, links=[]):
		if url == None: url = self.categories[category.title()]
		search_terms = search_terms.title().strip()
		soup = request_soup(self.fix_link(url))
		next_shorturl = False
		for link in soup.findAll('a',title=True,href=True):
			if any_all(word in link.get('title') for word in search_terms.split(' ')):
				if (self,link) not in links: links.append((self,link))
				if search_terms == link.get('title').title(): return [(self, link)]
			if not next_shorturl and 'next 200' in link:
				next_shorturl = link.get('href')
		if not next_shorturl: return links
		return self.category_to_pages(category, search_terms, any_all, next_shorturl, links)
	
	def gallery_to_list_img(self, link):
		try:
			soup = request_soup(self.fix_link(link))
		except ConnectionError as e:
			print(e)
			return False
		images = []
		for link in soup.findAll('a',title=True,href=True):
			if "File:" in link.get('href'):
				if link.get('href') not in images: images.append(link.get('href'))
		if not images:
			print("No covers found")
			return False
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
	try:
		soup = request_soup(url)
	except ConnectionError as e:
		print(e)
		return False
	for link in soup.findAll('a',title=True,href=True):
		if all(word in link.get('title').lower() for word in search_terms.split(' ')):
			return link
	counter+=1
	return cbr_solicitation_crawler(search_terms, links, counter)
		
		
