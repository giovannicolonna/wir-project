__author__ = 'Federica'

import sys
import math
import pprint as pp

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

reference = ['us']
with open('states.tsv') as states:
    for line in states:
        reference.append(line.split('\t')[0])

argv = sys.argv[1:len(sys.argv)]

ref = 'top250'
if argv[0] in reference:
    if argv[0] == 'us':
        ref = 'top-'+argv[0]
    else:
        ref = "states-tsv/top-"+argv[0]

beer_name = argv[0]
# print beer_name

argv = [arg.lower() for arg in argv if arg in fields]
# argv.insert(0, beer_name)
# print argv


input_beers = []
with open(ref+"-vectorialized.tsv", "r") as input_file:
    for line in input_file:
        splitted_line = line.split("\t")
        if beer_name in splitted_line[0]:
            beer = {}
            beer["name"] = splitted_line[0]
            for arg in argv:
                beer[arg] = splitted_line[fields[arg]]
            input_beers.append(beer)

similar = {}
for beer in input_beers:
    distances = []
    with open(ref+"-vectorialized.tsv", "r") as input_file:
        for line in input_file:
            splitted_line = line.split("\t")
            if splitted_line[0] == beer["name"]:
                continue
            name = splitted_line[0]
            dist = 0.0
            for arg in beer:
                if arg != "name":
                    dist += (float(beer[arg]) - float(splitted_line[fields[arg]]))**2
            dist = math.sqrt(dist)
            distances.append((name, dist))
    similar[beer["name"]] = distances


print


for beer in similar:
    # ordinare similar[beer] (lista di tuple (nomebirra, distanza beer-nomebirra))
    ordered_distances = sorted(similar[beer], key=lambda k:k[1], reverse=True)
    top10 = ordered_distances[0:10]
    bottom10 = ordered_distances[len(ordered_distances)-10:len(ordered_distances)]
    bottom10 = sorted(bottom10, key=lambda k: k[1])

    print "Top10 and Bottom10 of "+beer
    print "Top10: \n", top10
    print "Bottom10: \n", bottom10
    print

