"""Generate TS for network"""

import copy
import networkx as nx
import re
import math
import csv
import sys

inv = 0.359
iter_count = 20
normChoice = 0

def TSM(tweet_id, G):
  def calcScores(vs, s, n, other_sc, flag):
    s = 0
    if flag == 'ti':
      for vertex in vs:
        s += inver(other_sc.get(vertex))*G[n][vertex]['weight']
    elif flag == 'tw':
      for vertex in vs:
        s += inver(other_sc.get(vertex))*G[vertex][n]['weight']
    return s

  def inver(a):
    return 1/float(1+a**inv)

  def normalize(userScores, choice):
    score_list = userScores.values()
    min_val = min(score_list)
    max_val = max(score_list)
    if choice == 0:  # min-max
      for user in userScores:
        userScores[user] = (userScores[user] - min_val)/float(max_val - min_val)


    elif choice == 1: # sum-of-squares
      norm_den = sum(i**2 for i in score_list)
      norm_den = math.sqrt(norm_den)
      for user in userScores:
        userScores[user] = userScores[user]/float(norm_den)

    return userScores

  vertices = G.nodes()
  print('n(nodes): ', len(vertices))
  print('n(edges): ', len(G.edges()))

  hti = {}
  htw = {}

  for node in vertices:
    hti[node] = 1 #/float(len(vertices))
    htw[node] = 1 #/float(len(vertices))
  
  i = 0
  while i < iter_count:
    print('iteration count: ', i+1)

    prev_hti = copy.deepcopy(hti); prev_htw = copy.deepcopy(htw)

    for node in vertices:
      """Calculate Scores for Trustingness"""
      # vsti = g.neighbors(node, mode=OUT)
      vsti = [ind[1] for ind in G.out_edges(node)]
      sc = calcScores(vsti, 0, node, prev_htw, 'ti')
      hti[node] = sc

    for node in vertices:
      """Calculate Scores for Trustworthiness"""
      # vstw = g.neighbors(node, mode=IN)
      vstw = [ind[0] for ind in G.in_edges(node)]
      sc = calcScores(vstw, 0, node, prev_hti, 'tw')
      htw[node] = sc

    # Changed normalization to be inside loop
    hti = normalize(hti, normChoice)
    htw = normalize(htw, normChoice)
    i += 1

  TS_file = ''.join([tweet_id, '/New_TSM_networkx_network_l1_', tweet_id, '.txt'])
  with open(TS_file, 'w') as f:
    writer = csv.writer(f)
    for i in vertices:
      writer.writerow([i, hti[i], htw[i]])

if __name__ == '__main__':
  G = nx.DiGraph()
  G.add_edge(1, 3, weight = 1)
  G.add_edge(4, 1, weight = 1)
  G.add_edge(2, 3, weight = 1)
  G.add_edge(3, 5, weight = 1)
  G.add_edge(2, 5, weight = 1)
  
  TSM('sample', G)

  # G = nx.DiGraph()
  # with open('soc-Epinions1_ip.txt') as inptr:
  #   for line in inptr:
  #     a, b = int(line.split()[0]), int(line.split()[1])
  #     G.add_edge(a, b, weight = 1)

  # TSM('test', G)