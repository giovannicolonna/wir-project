import json
from collections import OrderedDict

csv_in = "groups/in_5.csv"
json_out = csv_in[:-4]+".json"

group = []
with open(csv_in, "r") as file_in:
    for line in file_in:
        user = OrderedDict()
        line = line.split(",")
        user["rate"] = line[0].strip()
        user["look"] = line[1].strip()
        user["smell"] = line[2].strip()
        user["taste"] = line[3].strip()
        user["feel"] = line[4].strip()
        user["overall"] = line[5].strip()
        group.append(user)

with open(json_out, "w") as output:
    output.write(json.dumps(group, indent=4))