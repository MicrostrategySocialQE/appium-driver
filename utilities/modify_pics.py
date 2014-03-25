"""
Run this script after modifying the data.json file.
Regenerate the *m.png files according to new data.json.
"""

import json
from utilities import picture
import os

if __name__ == "__main__":
    os.chdir(os.getcwd() + "/..")
    data_path = "views/"

    f = open(data_path + "data.json", 'r')
    data = f.read()
    f.close()

    data = json.loads(data)

    for view in data:
        ids = data[view]['elements'].keys()
        element_nodes = data[view]['elements'].values()
        picture.mark_nodes(data_path + view + '.png', element_nodes, ids)

