import matplotlib.pyplot as plot
import csv
networkx_TSM = "./Ground_truth/l1_community_ops-master/1117996079436451841/New_TSM_networkx_network_l1_1117996079436451841.txt"
igraph_TSM = "./Igraph_dev/1117996079436451841/New_TSM_networkx_network_l1_1117996079436451841.txt"

old = {}; new = {}
epsilon = 1e-3

with open(networkx_TSM) as netx:
  reader = csv.reader(netx)
  for row in reader:
    old[row[0]] = float(row[1]) # float(row[2]))

with open(igraph_TSM) as igraph:
  reader = csv.reader(igraph)
  for row in reader:
    new[row[0]] = float(row[1]) # float(row[2]))

old = sorted(list(set(old.values())))[10000:50000]
new = sorted(list(set(new.values())))[10000:50000]

for i in range(len(old)):
  if(abs(old[i] - new[i]) > epsilon):
    print(i, old[i], new[i])

plot.figure(0)
plot.plot(list(map(lambda x: x, old)), 'ro')

plot.figure(1)
plot.plot(list(map(lambda x: x, new)), 'bo')
plot.show()

# count = 0
# not_in = 0
# for key in old:
#   if key not in new:
#     print("Key not in new: ", key)
#     not_in += 1
#     # break
#   else:
#     if(abs(old[i][0] - new[i][0]) > epsilon):
#       print(key, old[key], new[key])
#       count += 1
#       # break

# print("Not equal # = ", count)
# print("Doesn't exist # = ", not_in)
