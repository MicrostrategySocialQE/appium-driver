__author__ = 'Zhenyu'

import re
import json

if __name__ == "__main__":
    f = open("types.txt")
    pairs = re.findall(r"@\"([a-zA-Z.]+)\"", f.read())
    print pairs
    t = {}
    for i in range(0, len(pairs), 2):
        t[pairs[i]] = pairs[i+1]
    print json.dumps(t, indent=8)
