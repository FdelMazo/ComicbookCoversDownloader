#F del Mazo - initial commit July 2017
#https://github.com/FdelMazo/
#federicodelmazo@hotmail.com

#Company: BaseSite, Volume Search, Bool Type
COMPANIES = {
	"DC":("http://dc.wikia.com/","index.php?title=Category:Volumes&from=",True),
	"MARVEL":("http://marvel.wikia.com/","wiki/Category:Comic_Lists?pagefrom=",False),
	"DARK HORSE":("http://darkhorse.wikia.com/","wiki/Category:Comic_Lists?display=page&pagefrom=",False),
	"IMAGE":("http://imagecomics.wikia.com/","http://imagecomics.wikia.com/wiki/Category:Comic_Lists?display=page&pagefrom=",False),
	"DYNAMITE":("http://dynamiteentertainment.wikia.com/", "wiki/Category:Comic_Lists?display=page&pagefrom=",False),
	"VALIANT":("http://valiant.wikia.com/","wiki/Category:Volumes?pagefrom=",False)
	}

class Wiki:
	def __init__(self, company):
		company = company.upper()
		assert company in COMPANIES
		self.title = company
		self.site = COMPANIES[self.title][0]
		self.volume_search = COMPANIES[self.title][1]
		self.bool_type = COMPANIES[self.title][2]
	
	def __repr__(self):
		return self.title
	
	def fix_link(self, link):
		if self.site not in link:
			return self.site+link
		else:
			return link