import re
import sys
import csv

# tweet_id = sys.argv[1]
tweet_id = '1117996079436451841'

s = set()
network_file = ''.join(['network_l1_', tweet_id, '.txt'])
with open(tweet_id + '/' + network_file) as infile:
    for line in infile:
        l_spl = re.split(r'[,]', line.rstrip())
        if len(l_spl) == 2:
            s.add(l_spl[0])
            s.add(l_spl[1])


ids_file = ''.join(['ids_l1_', tweet_id, '.txt'])
i = 0
with open(tweet_id + '/' + ids_file, 'w') as f:
    writer = csv.writer(f)
    for user in s:
        writer.writerow([user, i])
        i += 1


