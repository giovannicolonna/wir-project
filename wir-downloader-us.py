from bs4 import BeautifulSoup
import requests
import re
import time
import os
import shutil

LOGFILE = "top-us-log.txt"
log = open(LOGFILE, "w")

parser = "lxml"
baseUrl = "http://www.beeradvocate.com"
url = baseUrl + "/lists/us/"
directory = "top-us/"

t0 = time.clock()

if os.path.exists(directory):
    shutil.rmtree(directory)
os.mkdir(directory)

log.write("Requesting page: " + url + "\n")

netControl = True
while netControl:
    try:
        html = requests.get(url).text  # try except
        netControl = False
        log.write("OK: Connection established\n")
    except requests.RequestException:
        time.sleep(4)
        print "ERR: Connection error (first connection), retrying...\n"
        log.write("ERR: Connection error (first connection)\n")

soup = BeautifulSoup(html, parser)

log.write("Retrieving links...\n")
links = []

line = 0
for a in soup.select("td span a"):
    if line % 3 == 0:  # line is a beer
        link = baseUrl + a["href"]
        links.append(link)
    line += 1

log.write("Links retrieved: " + str(len(links)) + "\n\n")

# per ogni link scarico le prime 100 recensioni e salvo in locale... (4 pag)

log.write("Downloading reviews...\n")
count = 0
for link in links:
    offset = 0
    count += 1
    print "Beer number", count
    log.write("Beer number: " + str(count) + "\n")

    topr = "?sort=topr&start=" + str(offset)
    url = link + topr
    # Connection, try-except
    netControl = True
    while netControl:
        try:
            html = requests.get(url).text
            netControl = False
        except requests.RequestException:
            time.sleep(4)
            print("ERR: Connection error in beer page, retrying...\n")
            log.write("ERR: Connection error in beer page, retrying...\n")
    soup = BeautifulSoup(html, parser)
    rev = soup.find("span", "ba-reviews").string
    rev = int(re.sub(",", "", rev))

    log.write("\tNumber of reviews: " + str(rev) + "\n")
    log.write("\tReviews downloaded: " + str(offset) + "\n\t\t" + str(url) + "\n")
    output = open(directory + str(count) + "-" + str(offset) + ".html", "w")
    output.write(str(soup))
    output.close()

    offset += 25
    while offset < rev and offset <= 100:
        topr = "?sort=topr&start=" + str(offset)
        url = link + topr
        # Connection: try-except
        netControl = True
        while netControl:
            try:
                html = requests.get(url).text
                netControl = False
            except requests.RequestException:
                time.sleep(4)
                print "ERR: Connection error in reviews download page, retrying..."
                log.write("ERR: Connection error in reviews download page, retrying...\n")
        soup = BeautifulSoup(html, parser)
        log.write("\tReviews downloaded: " + str(offset) + "\n\t\t" + str(url) + "\n")
        output = open(directory + str(count) + "-" + str(offset) + ".html", "w")
        output.write(str(soup))
        output.close()
        offset += 25
t1 = time.clock()
log.write("Download completed in "+str(t1-t0)+" sec\n")

log.close()
