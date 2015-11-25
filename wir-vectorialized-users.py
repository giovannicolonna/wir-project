__author__ = 'Federica'

import json
from collections import OrderedDict, defaultdict

with open("users.json") as data_file:
    input = json.load(data_file)
