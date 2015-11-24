__author__ = 'Federica'

import os
import json
import requests
import time
import sys
import logging
from bs4 import BeautifulSoup
from collections import OrderedDict

# Parses the html files downloaded from the top-250 beers of BeerAdvocate, and builds the JSON array of these beers

# INPUTFILE can take values "top-250", "top-us", "top-states"
try:
    INPUT = sys.argv[1]
except IndexError:
    logging.error("Invalid source folder name: 'top-250','top-us' or 'top-states' are required.")
    print "Please, insert a valid source folder: 'top-250','top-us' or 'top-states'"
    exit(1)

output_directory = "data"
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

logging.basicConfig(filename='parser.log',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y/%m/%d %H:%M',
                    filemode='w',
                    level=logging.DEBUG)
logging.debug("Parsing htmls for "+INPUT+".")


if INPUT == "top-250" or INPUT == "top-us":
    beers = []
    old = "1"
    beer = OrderedDict()  # OrderedDict keeps insertion order
    reviews = []
    directory = INPUT+"/"
    if not os.path.exists(directory):
        logging.error(directory+" input folder does not exists.")
        print directory+" input folder does not exists. Execute downloader first."
        exit(1)
    htmls = sorted(os.listdir(directory))
    for html in htmls:

        if html[0] == ".":
            continue

        logging.info("Reading html file: "+str(html))
        b = html.split("-")[0]
        r = html.split("-")[1]

        if b != old:
            beer['reviews'] = reviews
            beers.append(beer)
            beer = OrderedDict()
            reviews = []

        soup = BeautifulSoup(open(directory+html), "lxml")

        if int(r.split('.')[0]) == 0:
            position = b
            name = soup.find('title').string.split("|")[0].strip()
            brewer = soup.find('title').string.split("|")[1].strip()
            ba_score = soup.find('span', 'BAscore_big ba-score').string.strip()
            num_rev = soup.find('span', 'ba-reviews').string.strip()
            hads = soup.find('span', 'ba-ratings').string.strip()
            avg = soup.find('span', 'ba-ravg').string.strip()
            pDev = soup.find('span', 'ba-pdev').string.strip()

            for link in soup.select("td a"):

                url = link['href']
                if "/place/directory" in url:
                    if link.string.strip() == "United States":
                        continue
                    state = link.string.strip()

                if "/beer/style" in url:
                    style = link.string.strip()
                    abv = link.nextSibling.replace("|", "").strip()

            beer['position'] = position
            beer['name'] = name
            beer['brewer'] = brewer
            beer['ba_score'] = ba_score
            beer['num_rev'] = num_rev
            beer['hads'] = hads
            beer['avg'] = avg
            beer['pDev'] = pDev
            beer['state'] = state
            beer['style'] = style
            beer['abv'] = abv

        for block in soup.find_all(id='rating_fullview_content_2'):

            logging.info("Reading reviews...")
            rate = block.find('span', 'BAscore_norm').get_text().strip()

            try:
                rDev = block.find('span', attrs={'style': 'color:#006600;'}).get_text().strip()
            except Exception:
                try:
                    rDev = block.find('span', attrs={'style': 'color:#990000;'}).get_text().strip()
                except Exception:
                    rDev = block.find('span', 'rAvg_norm').get_text().strip()

            # text = block.get_text()
            # text = sistemaTesto(text)

            i = 1
            for muted in block.find_all('span', 'muted'):

                if i == 1:
                    if 'look' in muted.get_text():
                        ratings = muted.get_text().encode('utf-8').split("|")
                        look = ratings[0].split(":")[1].strip()
                        smell = ratings[1].split(":")[1].strip()
                        taste = ratings[2].split(":")[1].strip()
                        feel = ratings[3].split(":")[1].strip()
                        overall = ratings[4].split(":")[1].strip()
                    else:
                        logging.warning("No characteristics found. Approximating on total given rate")
                        look = rate
                        smell = rate
                        taste = rate
                        feel = rate
                        overall = rate
                        i += 1

                if i == 3:
                    if muted.findAll('a', 'username') is not None:
                        for user in muted.findAll('a', 'username'):
                            reviewer = user.get_text()

                            # Code to extract link and points of each reviewer
                            reviewerPage = user.get('href')
                            reviewerProfileLink = 'http://www.beeradvocate.com'+reviewerPage+'?card=1'
                            # Connection: try-except
                            netControl = True
                            while netControl:
                                try:
                                    html = requests.get(reviewerProfileLink, timeout=5).text
                                    netControl = False
                                except requests.RequestException:
                                    time.sleep(4)
                                    logging.error("Connection error in reviewer point page, retrying...")

                            soup = BeautifulSoup(html, 'lxml')
                            for points in soup.findAll('a', 'concealed OverlayTrigger'):
                                reviewerScore = points.get_text()
                i += 1

            review = OrderedDict()

            review['rate'] = rate
            review['rDev'] = rDev
            review['look'] = look
            review['smell'] = smell
            review['taste'] = taste
            review['feel'] = feel
            review['overall'] = overall
            review['reviewer'] = reviewer
            review['reviewerScore'] = reviewerScore
            # review['text'] = text

            reviews.append(review)
            logging.info("Reviews of this file have been successfully read.")

        old = b

    beer['reviews'] = reviews
    beers.append(beer)

    logging.info("Building JSON dataset...")
    output = open("data/"+INPUT+".json", 'w')
    output.write(json.dumps(beers, indent=4))
    output.close()

    logging.info("JSON dataset has been successfully built.")

elif INPUT == "top-states":                     # top-states
    beers = []
    old = "1"
    old_s = "ak"
    beer = OrderedDict()  # OrderedDict keeps insertion order
    reviews = []
    directory = INPUT+"/"
    if not os.path.exists(directory):
        logging.error(directory+" input folder does not exists.")
        print directory+" input folder does not exists. Execute downloader first."
        exit(1)
    htmls = sorted(os.listdir(directory))

    for html in htmls:
        if html[0] == '.':
            continue

        logging.info("Reading html file: "+str(html))
        s = html.split("-")[0]
        b = html.split("-")[1]
        r = html.split("-")[2]

        if b != old:
            beer['reviews'] = reviews
            beers.append(beer)
            beer = OrderedDict()
            reviews = []

            if s != old_s:
                logging.info("Building JSON dataset...")
                output = open("data/top-states-"+old_s+".json", 'w')
                output.write(json.dumps(beers, indent=4))
                output.close()
                logging.info("JSON dataset for this state has been successfully built.")
                beers = []

        soup = BeautifulSoup(open(directory+html), "lxml")

        if int(r.split('.')[0]) == 0:
            position = b
            name = soup.find('title').string.split("|")[0].strip()
            brewer = soup.find('title').string.split("|")[1].strip()
            ba_score = soup.find('span', 'BAscore_big ba-score').string.strip()
            num_rev = soup.find('span', 'ba-reviews').string.strip()
            hads = soup.find('span', 'ba-ratings').string.strip()
            avg = soup.find('span', 'ba-ravg').string.strip()
            pDev = soup.find('span', 'ba-pdev').string.strip()

            for link in soup.select("td a"):

                url = link['href']
                if "/place/directory" in url:
                    if link.string.strip() == "United States":
                        continue
                    state = link.string.strip()

                if "/beer/style" in url:
                    style = link.string.strip()
                    abv = link.nextSibling.replace("|", "").strip()

            beer['position'] = position
            beer['name'] = name
            beer['brewer'] = brewer
            beer['ba_score'] = ba_score
            beer['num_rev'] = num_rev
            beer['hads'] = hads
            beer['avg'] = avg
            beer['pDev'] = pDev
            beer['state'] = state
            beer['style'] = style
            beer['abv'] = abv

        for block in soup.find_all(id='rating_fullview_content_2'):

            rate = block.find('span', 'BAscore_norm').get_text().strip()

            try:
                rDev = block.find('span', attrs={'style':'color:#006600;'}).get_text().strip()
            except Exception:
                try:
                    rDev = block.find('span', attrs={'style':'color:#990000;'}).get_text().strip()
                except Exception:
                    rDev = block.find('span', 'rAvg_norm').get_text().strip()
            # text = block.get_text()
            # text = sistemaTesto(text)

            i = 1
            for muted in block.find_all('span', 'muted'):

                if i == 1:
                    if 'look' in muted.get_text():
                        ratings = muted.get_text().encode('utf-8').split("|")
                        look = ratings[0].split(":")[1].strip()
                        smell = ratings[1].split(":")[1].strip()
                        taste = ratings[2].split(":")[1].strip()
                        feel = ratings[3].split(":")[1].strip()
                        overall = ratings[4].split(":")[1].strip()
                    else:
                        logging.warning("No characteristics found. Approximating on total given rate")
                        look = rate
                        smell = rate
                        taste = rate
                        feel = rate
                        overall = rate
                        i += 1

                if i == 3:
                    if muted.findAll('a', 'username') is not None:
                        for user in muted.findAll('a', 'username'):
                            reviewer = user.get_text()
                i += 1

            review = OrderedDict()

            review['rate'] = rate
            review['rDev'] = rDev
            review['look'] = look
            review['smell'] = smell
            review['taste'] = taste
            review['feel'] = feel
            review['overall'] = overall
            review['reviewer'] = reviewer
            # review['text'] = text

            reviews.append(review)

        old = b
        old_s = s

    beer['reviews'] = reviews
    beers.append(beer)
    output = open("data/top-states-"+old_s+".json", 'w')
    output.write(json.dumps(beers, indent=4))
    output.close()

else:
    logging.error("Please, insert a valid dataset: 'top-250','top-us' or 'top-states'")
    print "Please, insert a valid dataset: 'top-250','top-us' or 'top-states'"
    exit(1)

# def sistemaTesto(text):
#    try:
#         descr = text
#         descr = descr.split("|")[4].split("overall: ")[1]
#         if descr[1] == '.':
#             if descr[3].isdigit():
#                 return descr[4:]
#             else:
#                 return descr[3:]
#         else:
#             return descr[1:]
#     except:
#         log.write("WARNING: a description does not respect standards, could contain invalid characters\n")
#         return text
