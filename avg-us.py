__author__ = 'Federica'

import json
import re

INPUTFILE = "top-us" #si puo' scegliere tra top-us e top250


input_json = open(INPUTFILE+".json", 'r')
beers_json = input_json.read()
input_json.close()

# lista di birre. Ogni birra e' un dict con i vari campi, tra cui review che e' una lista
beers = json.loads(beers_json)

beers_dict = {} #not used
output_file = open(INPUTFILE+"-vectorialized.tsv",'w')

for beer in beers:
    tot_rev = len(beer['reviews'])
    beer_name = str(beer['name'].encode('utf-8'))
    avg_look = 0
    avg_smell = 0
    avg_taste = 0
    avg_feel = 0
    avg_overall = 0
    # weighted
    tot_weight = 0
    w_avg_look = 0
    w_avg_smell = 0
    w_avg_taste = 0
    w_avg_feel = 0
    w_avg_overall = 0

    for review in beer['reviews']:

        avg_look += float(review['look'])
        avg_smell += float(review['smell'])
        avg_taste += float(review['taste'])
        avg_feel += float(review['feel'])
        avg_overall += float(review['overall'])

        weight = review['reviewerScore']
        weight = float(re.sub(",", "", weight))
        tot_weight += weight

        w_avg_look += float(review['look']) * weight
        w_avg_smell += float(review['smell']) * weight
        w_avg_taste += float(review['taste']) * weight
        w_avg_feel += float(review['feel']) * weight
        w_avg_overall += float(review['overall']) * weight

    avg_look /= tot_rev
    avg_smell /= tot_rev
    avg_taste /= tot_rev
    avg_feel /= tot_rev
    avg_overall /= tot_rev

    w_avg_look /= tot_weight
    w_avg_smell /= tot_weight
    w_avg_taste /= tot_weight
    w_avg_feel /= tot_weight
    w_avg_overall /= tot_weight

    output_file.write(beer_name+'\t')

    output_file.write(str(avg_look)+'\t')
    output_file.write(str(avg_smell)+'\t')
    output_file.write(str(avg_taste)+'\t')
    output_file.write(str(avg_feel)+'\t')
    output_file.write(str(avg_overall)+'\t')

    # print on file weighted characteristics


    output_file.write(str(w_avg_look)+'\t')
    output_file.write(str(w_avg_smell)+'\t')
    output_file.write(str(w_avg_taste)+'\t')
    output_file.write(str(w_avg_feel)+'\t')
    output_file.write(str(w_avg_overall)+'\n')


output_file.close()

