__author__ = 'Federica'

import sys
import math

# [name, look, smell, taste, feel, overall] FOR TOP-STATES
# [w_look, w_smell, w_taste, w_feel, w_overall] FOR TOP-US and TOP250

fields = {}
fields["name"] = 0
fields["look"] = 1
fields["smell"] = 2
fields["taste"] = 3
fields["feel"] = 4
fields["overall"] = 5

# loading states abbreviations in reference list
reference = ['us']
with open('states.tsv') as states:
    for line in states:
        reference.append(line.split('\t')[0])

# excluding python script
argv = sys.argv[1:len(sys.argv)]

# setting top-250 as default reference for ranking
# if you want a different reference for ranking pass parameter 'us' or 'state initials' (i.e. 'wy')
ref = "top-250"
flag = False
try:
    if argv[0] in reference:
        if argv[0] == 'us':
            ref = "top-"+argv[0]
        else:
            ref = "states-tsv/top-"+argv[0]
        flag = True
except IndexError:
    print("Insert a beer name and characteristics")
    exit(1)

if flag:
    try:
        beer_name = argv[1].lower()
    except IndexError:
        print("Insert a beer name and characteristics")
        exit(1)
else:
    beer_name = argv[0].lower()

# if no characteristic has been inserted, overall is taken as default
if flag:
    if len(argv) == 2:
        argv.append("overall")
else:
    if len(argv) == 1:
        argv.append("overall")

argv = [arg.lower() for arg in argv if arg in fields]

input_beers = []
try:
    with open("data/vectors/"+ref+"-vectorialized.tsv", 'r') as input_file:
        for line in input_file:
            splitted_line = line.split("\t")
            if beer_name in splitted_line[0].lower():
                beer = {}
                beer["name"] = splitted_line[0]
                for arg in argv:
                    beer[arg] = splitted_line[fields[arg]]
                input_beers.append(beer)
except IOError:
    print "Default dataset (top-250) is missing. Specify another dataset, or re-execute the wir-avg.py on top-250."
    exit(1)

similar = {}
for beer in input_beers:
    distances = []
    with open("data/vectors/"+ref+"-vectorialized.tsv", "r") as input_file:
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

output_file = open(beer_name+"_output.txt", 'w')
for beer in similar:
    # order similar[beer] (tuple list (input_beer, distance beer-input_beer))
    ordered_distances = sorted(similar[beer], key=lambda k: k[1], reverse=True)
    top10 = ordered_distances[0:10]
    bottom10 = ordered_distances[len(ordered_distances)-10:len(ordered_distances)]
    bottom10 = sorted(bottom10, key=lambda k: k[1])

    output_file.write("Top10 and Bottom10 beers similar to "+str(beer)+" according to: "+str(argv)+"\n\n")
    print ("Top10 and Bottom10 of "+str(beer)+" according to: "+str(argv))
    output_file.write("Top10:\n")
    for b in top10:
        output_file.write("\t"+str(b)+"\n")
    print "Top10: \n", top10
    output_file.write("Bottom10:\n")
    for b in bottom10:
        output_file.write("\t"+str(b)+"\n")
    output_file.write("\n")
    print "Bottom10: \n", bottom10
    print
    print "Rankings have been saved in: "+beer_name+"_output.txt file."
    print "If there are multiple results, don't worry, we computed rankings for all of them."
output_file.close()
