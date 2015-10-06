from pprint import PrettyPrinter
from bs4 import BeautifulSoup
import requests

pp = PrettyPrinter()

parser = "lxml"
baseUrl = "http://www.beeradvocate.com"
url = baseUrl+"/lists/top/"

html = requests.get(url).text
soup = BeautifulSoup(html, parser)

links = []

line = 0
for a in soup.select("td span a"):
	if line%3 == 0:  # line is a beer
		link = baseUrl+a["href"]
		links.append(link)
	line += 1

print len(links)
#pp.pprint(links)

#per ogni link scarico le prime 100 recensioni e salvo in locale... (4 pag)
#file.write(soup.prettify())

offset = "0"
topr = "?sort=topr&start="+offset

for link in links:
	url = link+topr
	print url
	html = requests.get(url).text
	soup = BeautifulSoup(html, parser)
	print soup.find()
	break
