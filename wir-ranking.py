__author__ = "ioemilio"

import sys
import math
import pprint as pp

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

if len(argv) == 0:
    argv.append("overall")


ref = 'top-250'      # set top-250 as default
if argv[0] in reference:
    if argv[0] == 'us':
        ref = 'top-'+argv[0]
    else:
        ref = "top-"+argv[0]
    if len(argv) == 1:
        argv.append("overall")

argv = [arg.lower() for arg in argv if arg in fields]


beers = []

try:
    with open("data/vectors/"+ref+"-vectorialized.tsv", "r") as input_file:
        for line in input_file:
            splitted_line = line.split("\t")
            beer = {}
            beer["name"] = splitted_line[0]
            norm = 0.0
            for arg in argv:
                norm += float(splitted_line[fields[arg]])**2
            beer["norm"] = math.sqrt(norm)
            beers.append(beer)
except:
    print "Vectorized default dataset (top-250) is missing. Execute on another dataset (us or of an American state) or re-execute the wir-avg.py program."
    exit(1)

# print beers
beers = sorted(beers, key=lambda entry: entry["norm"], reverse=True)
print("Ranking of beers on " + ref + " according to features: "+str(argv))

if "/" in ref:
    ref = ref.split("/")[1]

output_file = open("Ranking_output.txt", 'w')
output_file.write("Ranking on "+ref+" according to features: "+str(argv)+"\n")
for b in beers:
    output_file.write(str(b)+"\n")

output_file.close()
pp.pprint(beers)
print "Ranking has been saved in Ranking_output.txt file."

