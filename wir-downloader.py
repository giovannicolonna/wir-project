from bs4 import BeautifulSoup
import requests
import re
import time


LOGFILE = "top250-log.txt"
log = open(LOGFILE, "w")

parser = "lxml"
baseUrl = "http://www.beeradvocate.com"
url = baseUrl+"/lists/top/"

log.write("Requesting page: "+url+"\n")

netControl = True
while(netControl):
    try:
        html = requests.get(url).text  # try except
        netControl = False
        log.write("OK: Connection established\n")
    except requests.ConnectionError:
        #cannot connect, wait and retry
        time.sleep(4)
        log.write("ERR: Connection error, retrying...\n")

soup = BeautifulSoup(html, parser)

log.write("Retrieving links...\n")
links = []

line = 0
for a in soup.select("td span a"):
	if line%3 == 0:  # line is a beer
		link = baseUrl+a["href"]
		links.append(link)
	line += 1

log.write("Links retrieved: "+str(len(links))+"\n\n")

#per ogni link scarico le prime 100 recensioni e salvo in locale... (4 pag)
#file.write(soup.prettify())
log.write("Downloading reviews...\n")
count = 0
for link in links:
	offset = 0
	count += 1
	print "Beer number", count
	log.write("Beer number: "+str(count)+"\n")

	topr = "?sort=topr&start="+str(offset)
	url = link+topr
	#Connection, try-except
	netControl = True
	while (netControl):
		try:
			html = requests.get(url).text
			netControl = False
		except requests.ConnectionError:
			time.sleep(4)
			log.write("ERR: Connection error in beer page, retrying....")
	soup = BeautifulSoup(html, parser)
	rev = soup.find("span", "ba-reviews").string
	rev = int(re.sub(",", "", rev))

	log.write("\tNumber of reviews: "+str(rev)+"\n")
	log.write("\tReviews downloaded: "+str(offset)+"\n\t\t"+str(url)+"\n")
	output = open("top250/"+str(count)+"-"+str(offset)+".html", "w")
	output.write(str(soup))
	output.close()

	offset += 25
	while (offset < rev and offset <= 100):
		topr = "?sort=topr&start="+str(offset)
		url = link+topr
		#Connection: try-except
		netControl = True
		while (netControl):
			try:
				html = requests.get(url).text
				netControl = False
			except requests.ConnectionError:
				time.sleep(4)
				log.write("ERR: Connection error in reviews download page, retrying....")
		soup = BeautifulSoup(html, parser)
		log.write("\tReviews downloaded: "+str(offset)+"\n\t\t"+str(url)+"\n")
		output = open("top250/"+str(count)+"-"+str(offset)+".html", "w")
		output.write(str(soup))
		output.close()
		offset += 25

	if count > 3:
		break


##
##    TODO: building dataset from HTML files for top-250
##



log.close()
