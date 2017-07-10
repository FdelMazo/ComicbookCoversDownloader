#F del Mazo - initial commit July 2017
#https://github.com/FdelMazo/
#federicodelmazo@hotmail.com

#CONSTANT INDEXES MUST CORRELATE TO EACH OTHER
COMPANIES = ["DC", "MARVEL"]
SITES = ["http://dc.wikia.com/", "http://marvel.wikia.com/"]
VOLUME_SEARCH = ["index.php?title=Category:Volumes&from=", "wiki/Category:Comic_Lists?pagefrom="]
BOOL_TYPE = [True, False]

class Wiki:
	def __init__(self, company):
		company = company.upper()
		assert company in COMPANIES
		self.title = company
		self.ind = COMPANIES.index(company)
		self.site = SITES[self.ind]
		self.volume_search = VOLUME_SEARCH[self.ind]
		self.bool_type = BOOL_TYPE[self.ind]
	
	def __repr__(self):
		return self.title
	
	def fix_link(self, link):
		if self.site not in link:
			return self.site+link
		else:
			return link