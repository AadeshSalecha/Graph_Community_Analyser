"""generates two files:
louvain_: Each line contains community members.
com_NBC_: Generates dictionary of Core, Boundary, Neighbor for each community"""

import re
import csv
import sys
import json
import pickle
import networkx as nx
import community as com
from collections import defaultdict


def louvain(graph, cur_dir = './'):
  print('Louvain clustering started')
  part = graph.community_multilevel()
  print('Louvain clustering ended')

  print('Node->Cluster to Cluster->Node conversion started')
  cluster = defaultdict(list)
  mem = part.membership
  for i in range(len(mem)):
    cluster[mem[i]].append(i)
  print('Node->Cluster to Cluster->Node conversion ended')

  pickle.dump(cluster, open(cur_dir + '/Concatenated/louvain', 'wb'))
  return cluster

def NBC(tweet_id, cluster, graph, l_spreaders, cur_dir = "./"):
  s_spreaders = set(l_spreaders)

  graph_nodes = set(range(0, len(graph.vs)))
  print('No. of clusters:', len(cluster.keys()))
  with open(cur_dir + "/" + tweet_id + '/com_NBC_l1_' + tweet_id + '.txt', 'w') as f:
    for cl in cluster:
      print('Running for cluster: ', cl)

      d = dict()
      d['cl'] = cl
      cluster_nodes = set(cluster[cl])
      infected_nodes = s_spreaders.intersection(cluster_nodes)
      # boundary_edges_out = list(my_edge_boundary(graph, graph_nodes.difference(cluster_nodes), cluster_nodes))
      boundary_edges_in = list(my_edge_boundary(graph, cluster_nodes, graph_nodes.difference(cluster_nodes)))
      boundary_nodes = set([str(i[0]) for i in boundary_edges_in])
      in_neighbor_nodes = set([str(i[1]) for i in boundary_edges_in])
      # out_neighbor_nodes = set([str(i[0]) for i in boundary_edges_out])
      core_nodes = (cluster_nodes.difference(boundary_nodes))
      d['core'] = list(core_nodes)
      d['inf_core'] = list(core_nodes.intersection(infected_nodes))
      d['boundary'] = list(boundary_nodes)
      d['inf_boundary'] = list(boundary_nodes.intersection(infected_nodes))
      d['neighbor'] = list(in_neighbor_nodes)
      d['inf_neighbor'] = list(in_neighbor_nodes.intersection(s_spreaders))
      dict_str = json.dumps(d)
      f.write(dict_str + '\n')

def my_edge_boundary(G, nbunch1, nbunch2):
  nset2 = set(nbunch2)
  num_nodes = len(G.vs)
  return [(n1,n2) for n1 in nbunch1 if n1 < num_nodes for n2 in G.neighbors(n1, mode = 'out') if n2 in nset2]