from bs4 import BeautifulSoup
import requests
import re
import logging
import shutil
import os
import time
import sys


def request(URL):
    net_control = True
    while net_control:
        try:
            HTML = requests.get(URL).text  # try except
            net_control = False
            logging.info("OK: Connection established")
        except requests.RequestException:
            time.sleep(4)
            logging.error("Connection error (first connection), retrying")
    return HTML

logging.basicConfig(filename='downloader.log',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y/%m/%d %H:%M',
                    filemode='w',
                    level=logging.DEBUG)

INPUT = sys.argv[1]
parser = "lxml"
baseUrl = "http://www.beeradvocate.com"
directory = INPUT+"/"

if os.path.exists(directory):
    shutil.rmtree(directory)
os.mkdir(directory)

t0 = time.time()

if INPUT == "top-states":
    states = {}
    st = open("states.tsv", "r")
    for line in st:
        line = line.split("\t")
        states[line[1]] = line[0]
    st.close()

    state_num = 0
    logging.debug("Downloading html pages from "+baseUrl+" for "+INPUT+" beers")

    for state in states:

        logging.debug("STATE: " + state)
        state_num += 1
        print state, state_num
        url = baseUrl + "/lists/state/" + states[state]
        logging.info("Requesting page: " + url)

        html = request(url)
        soup = BeautifulSoup(html, parser)

        logging.info("Retrieving links...")
        links = []

        line = 0
        for a in soup.select("td span a"):
            if line % 3 == 0:  # line is a beer
                link = baseUrl + a["href"]
                links.append(link)
            line += 1

        logging.debug("Links retrieved: " + str(len(links)) + "\n")
        logging.info("Downloading reviews...")

        count = 0
        for link in links:

            offset = 0
            count += 1
            print "Beer number", count
            logging.info("Beer number: " + str(count))

            topr = "?sort=topr&start=" + str(offset)
            url = link + topr

            html = request(url)

            soup = BeautifulSoup(html, parser)
            rev = soup.find("span", "ba-reviews").string
            rev = int(re.sub(",", "", rev))

            logging.info("\tNumber of reviews: " + str(rev))
            logging.debug("\tReviews downloaded: " + str(offset) + "\n\t\t" + str(url))
            output = open(directory + states[state] + "-" + str(count) + "-" + str(offset) + ".html", "w")
            output.write(str(soup))
            output.close()

            offset += 25
            while offset < rev and offset <= 100:

                topr = "?sort=topr&start=" + str(offset)
                url = link + topr
                html = request(url)
                soup = BeautifulSoup(html, parser)

                logging.debug("\tReviews downloaded: " + str(offset) + "\n\t\t" + str(url) + "\n")
                output = open(directory + states[state] + "-" + str(count) + "-" + str(offset) + ".html", "w")
                output.write(str(soup))
                output.close()
                offset += 25

        count = 0


else:
    if INPUT == "top-250":
        url = baseUrl + "/lists/top/"
    else:
        url = baseUrl + "/lists/us/"

    logging.debug("Downloading html pages from "+baseUrl+" for "+INPUT+" beers")
    logging.info("Requesting page: " + url)

    html = request(url)

    soup = BeautifulSoup(html, parser)

    logging.info("Retrieving links...")
    links = []

    line = 0
    for a in soup.select("td span a"):
        if line % 3 == 0:  # line is a beer
            link = baseUrl + a["href"]
            links.append(link)
        line += 1

    logging.info("Links retrieved: " + str(len(links)) + "\n")

    # for each link download first 100 reviews and save in local... (4 pages)

    logging.info("Downloading reviews...")
    count = 0
    for link in links:
        offset = 0
        count += 1
        print "Beer number", count
        logging.debug("Beer number: " + str(count))

        topr = "?sort=topr&start=" + str(offset)
        url = link + topr

        html = request(url)

        soup = BeautifulSoup(html, parser)
        rev = soup.find("span", "ba-reviews").string
        rev = int(re.sub(",", "", rev))

        logging.info("Number of reviews: " + str(rev))
        logging.debug("\tReviews downloaded: " + str(offset) + "\n\t\t" + str(url))
        output = open(directory + str(count) + "-" + str(offset) + ".html", "w")
        output.write(str(soup))
        output.close()

        offset += 25
        while offset < rev and offset <= 100:

            topr = "?sort=topr&start=" + str(offset)
            url = link + topr
            html = request(url)
            soup = BeautifulSoup(html, parser)

            logging.debug("\tReviews downloaded: " + str(offset) + "\n\t\t" + str(url))
            output = open(directory + str(count) + "-" + str(offset) + ".html", "w")
            output.write(str(soup))
            output.close()
            offset += 25

t1 = time.time()
logging.info("Download completed in "+str(t1-t0)+" sec")

