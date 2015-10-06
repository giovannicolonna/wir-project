__author__ = 'Federica'

import os
import json
from bs4 import BeautifulSoup

directory = "top250/"
htmls = os.listdir(directory)

beers = []
old = "1"
beer = {}
reviews = []

for html in htmls:
    print html
    b = html.split("-")[0]
    r = html.split("-")[1]

    if b != old:
        beer['reviews'] = reviews
        beers.append(beer)
        beer = {}
        reviews = []

    soup = BeautifulSoup(open(directory+html))

    if r[0] == 0:
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
                abv = link.nextSibling.encode('utf-8').replace("|", "").strip()

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
        text = block.get_text()

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

        review = {}
        review['rate'] = rate
        review['rDev'] = rDev
        review['look'] = look
        review['smell'] = smell
        review['taste'] = taste
        review['feel'] = feel
        review['overall'] = overall
        review['text'] = text
        review['reviewer'] = reviewer

        reviews.append(review)

    old = b

output = open("top250.json", 'w')
output.write(json.dumps(beers))
output.close()

