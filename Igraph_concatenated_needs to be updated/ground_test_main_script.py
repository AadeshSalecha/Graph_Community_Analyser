import igraph
import os
import sys
import csv
import re
import networkx as nx
# import generate_retweet_graph
# import subgraph_stats
# import spreader_role
# import second_level
# import bel_ranks
import igraph_louvain_implementation
import igraph_TSM_implementation

# tweet_id = sys.argv[1]
tweet_id = '1117996079436451841'
global_dir = './1117996079436451841/'

id_dict = {}
edges = set()

count = 0
id_dict = dict()
ids_file = ''.join(['ids_l1_', tweet_id, '.txt'])
with open(tweet_id + '/' + ids_file) as infile:
  for line in infile:
      l_spl = re.split(r'[,]', line.rstrip())
      id_dict[l_spl[0]] = int(l_spl[1])

network_file = ''.join(['network_l1_', tweet_id, '.txt'])
with open(tweet_id + '/' + network_file) as infile:
    for line in infile:
        l_spl = re.split(',', line.rstrip())
        if len(l_spl) == 2:
            try:
                edges.add((id_dict[l_spl[0]], id_dict[l_spl[1]]))
            except KeyError:
                continue

# Consider only those spreaders whose network could be extracted. (i.e. excluding 'protected' twitter users)
l_spreaders = []
retweet_file = ''.join(['retweets_', tweet_id, '.txt'])
with open(tweet_id + '/' + retweet_file) as infile:
    for line in infile:
        l_spl = re.split(r'[,]', line.rstrip())
        if l_spl[2] in id_dict:
            l_spreaders.append(id_dict[l_spl[2]])

# Make IGraph
print('No. of nodes = ', len(id_dict))
print('No. of edges = ', len(edges))

igraph_G = igraph.Graph(list(edges), directed = True)
TSM_scores = igraph_TSM_implementation.TSM(cur_dir = global_dir, graph = igraph_G, vertices = range(0, len(igraph_G.vs)), tweet_id = tweet_id)
undirected_igraph_G = igraph.Graph(list(edges), directed = False)
louvain = igraph_louvain_implementation.louvain(cur_dir = global_dir, graph = undirected_igraph_G, tweet_id = tweet_id)

# networkx_TSM.TSM(tweet_id, G)
# generate_retweet_graph.retweetGraph(tweet_id, id_dict, l_spreaders)
# louvain_communities.louvain_and_NBC(tweet_id, G, l_spreaders)
# subgraph_stats.B_C_degree_stats(tweet_id, G)
# spreader_role.sp_role(tweet_id, l_spreaders)
# second_level.second_level_gen(tweet_id, id_dict)
# bel_ranks.spread_edge_bel(tweet_id, id_dict, G, l_spreaders)
