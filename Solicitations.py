#F del Mazo - initial commit July 2017
#https://github.com/FdelMazo/
#federicodelmazo@hotmail.com

from Wikias import *
import os
import shutil

def solicitations():
	solicits = input("\n Write a solicitation with COMPANY  MONTH YEAR: ")
	link = cbr_solicitation_crawler(solicits)
	soup = request_soup(link.get('href'))
	if soup:
		dir_name=soup.title.string
		os.makedirs(dir_name,exist_ok=True)
		images = []
		for div in soup.findAll("div",{"class":"responsiveImg img_article_content"}):
			if not div.next_sibling: continue
			comic_name = str(div.next_sibling.next_sibling.next_sibling.string)
			comic_name = ''.join(list(c if c not in INVALID_CHARACTERS else "_" for c in comic_name)).title()
			comic_name+=".jpg"
			for picture in div.picture.findAll("source"):
				img = picture["srcset"]
				index = img.index(".jpg") +4
				img = img[:index]
				if comic_name != "None.jpg" and (comic_name,img) not in images: images.append((comic_name,img))
		for comic_name,img in images:
			r = requests.get(img)
			with open(comic_name, "wb") as f:
				f.write(r.content)
			print("Downloaded: {}".format(comic_name))
			try: shutil.move(comic_name, dir_name)
			except: pass