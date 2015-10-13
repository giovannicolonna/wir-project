__author__ = "ioemilio"

import sys
import math
import pprint as pp

LOGFILE = "top-us-ranking-log.txt"
log = open(LOGFILE, "w")

# [name, look, smell, taste, feel, overall, w_look, w_smell, w_taste, w_feel, w_overall]
fields = {}
fields["name"] = 0
fields["look"] = 1
fields["smell"] = 2
fields["taste"] = 3
fields["feel"] = 4
fields["overall"] = 5
fields["w_look"] = 6
fields["w_smell"] = 7
fields["w_taste"] = 8
fields["w_feel"] = 9
fields["w_overall"] = 10

argv = sys.argv[1:len(sys.argv)]
argv = [arg.lower() for arg in argv if arg in fields]

log.write("Considered features: "+str(argv)+"\n")
log.write("Ranking beers according to features...\n")
beers = []

with open("top-us-vectorialized.tsv", "r") as input_file:
    for line in input_file:
        splitted_line = line.split("\t")
        beer = {}
        beer["name"] = splitted_line[0]
        norm = 0.0
        for arg in argv:
            norm += float(splitted_line[fields[arg]])**2
        beer["norm"] = math.sqrt(norm)
        beers.append(beer)

#print beers
beers = sorted(beers, key=lambda entry:entry["norm"], reverse=True)

top10 = beers[0:10]
bottom10 = beers[len(beers)-10:len(beers)]
bottom10 = sorted(bottom10, key=lambda entry:entry["norm"])

log.write("\nTop 10 beers according features:\n")
for b in top10:
    log.write(str(b)+"\n")

log.write("\nBottom 10 beers according features:\n")
for b in bottom10:
    log.write(str(b)+"\n")

log.close()
