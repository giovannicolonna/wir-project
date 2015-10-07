__author__ = 'Federica'

import os
import json
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

log = open("parser-log-states.txt","w")

def sistemaTesto(text):
    try:
        descr = text
        descr = descr.split("|")[4].split("overall: ")[1]
        if descr[1] == '.':
            if descr[3].isdigit():
                return descr[4:]
            else:
                return descr[3:]
        else:
            return descr[1:]
    except:
        log.write("WARNING: a description does not respect standards, could contain invalid characters\n")
        return text

directory = "top-states/"
htmls = sorted(os.listdir(directory))

beers = []
old = "1"
old_s = "ak"
beer = OrderedDict()  # trasfrmandoli in OrderedDict si mantiene l'ordine di inserimento
reviews = []

for html in htmls:
    if html[0] == '.':
        continue
    print html
    log.write("Reading html file: "+str(html)+"\n")
    s = html.split("-")[0]
    b = html.split("-")[1]
    r = html.split("-")[2]

    if b != old:
        beer['reviews'] = reviews
        beers.append(beer)
        beer = OrderedDict()  # trasfrmandoli in OrderedDict si mantiene l'ordine di inserimento
        reviews = []
        if s != old_s:
            log.write("Building JSON dataset...\n")
            output = open("top-states-"+old_s+".json", 'w')
            output.write(json.dumps(beers, indent=4))
            output.close()
            log.write("JSON dataset has been successfully built.\n")
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
        log.write("\tReading reviews...\n")
        rate = block.find('span', 'BAscore_norm').get_text().strip()

        try:
            rDev = block.find('span', attrs={'style':'color:#006600;'}).get_text().strip()
        except Exception:
            try:
                rDev = block.find('span', attrs={'style':'color:#990000;'}).get_text().strip()
            except Exception:
                rDev = block.find('span', 'rAvg_norm').get_text().strip()

        #text = block.get_text()
        #text = sistemaTesto(text)
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
                    log.write("No characteristics found. Approximating on total given rate\n")
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
                        ##code for extracting link of reviewer (tested)

                        ##reviewerPage = user.get('href')
                        ##reviewerProfileLink = 'http://www.beeradvocate.com'+reviewerPage+'?card=1'
                        ##html = requests.get(reviewerProfileLink).text
                        ##soup = BeautifulSoup(html,'lxml')
                        ##for points in soup.findAll('a','concealed OverlayTrigger'):
                        ##    reviewerScore = points.get_text()


            i += 1

        review = OrderedDict()  # trasfrmandoli in OrderedDict si mantiene l'ordine di inserimento
        review['rate'] = rate
        review['rDev'] = rDev
        review['look'] = look
        review['smell'] = smell
        review['taste'] = taste
        review['feel'] = feel
        review['overall'] = overall
        #review['text'] = text
        review['reviewer'] = reviewer
        #review['reviewerScore'] = reviewerScore
        reviews.append(review)
        log.write("\tReviews of this file have been successfully read.\n")

    old = b
    old_s = s

log.close()

