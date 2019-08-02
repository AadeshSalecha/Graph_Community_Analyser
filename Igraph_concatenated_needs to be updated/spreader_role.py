"""For every spreader check for which communities its is a C, B or N."""
import json
import os
import re
import sys
from collections import defaultdict

def sp_role(tweet_id, l_spreaders):
  with open(cur_dir + '/Concatenated/spreader_role.txt', 'w') as f:
    for spreader in l_spreaders:
      D = defaultdict(list)
      D['spreader'] = spreader
      with open(cur_dir + '/Concatenated/com_NBC_file.txt') as infile:
        for line in infile:
          d = json.loads(line)
          d_keys = ['core', 'neighbor', 'boundary']
          for key in d_keys:
            value = d[key]
            if spreader in value:
              D[key].append(d['cl'])
      dict_str = json.dumps(D)
      print(D)
      f.write(dict_str + '\n')