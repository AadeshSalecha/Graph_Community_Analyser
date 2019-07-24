'''For every spreader edge (source to target), generates rank of target followers node
based on believability for all followers of source'''

import networkx as nx
import json
import csv
import re
import sys
from collections import defaultdict

def spread_edge_bel(TSM_scores, tweet_id, id_dict, G, l_spreaders):
  G_fol_edges = []
  for i in range(0, len(l_spreaders)):
    for j in range(i + 1, len(l_spreaders)):
      source = l_spreaders[i]
      target = l_spreaders[j]
      if(G.get_eid(source, target, directed = True, error = False) != -1):
        G_fol_edges.append((target, source))
  G_fol = igraph.Graph(G_fol_edges, directed = True)

  spreader_with_no_paths = 0
  # with open(tweet_id + '/' +'demofile3.txt', 'a') as f:
  retweet_graph_ranks_file = ''.join(['spreaders_bel_stats_', tweet_id, '.txt'])
  with open(tweet_id + '/' + retweet_graph_ranks_file, 'w') as f:
    writer = csv.writer(f)
    for spreader in l_spreaders:
      d = dict()
      d['spreader'] = spreader
      print('Spreader:', spreader)
      in_edge_list = list(G.neighbors(spreader, mode = 'in'))
      d['follower_count'] = len(in_edge_list)
      in_edge_user_list = [[i, float(TSM_scores[i][0])] for i in in_edge_list]
      in_edge_sorted_list = sorted(in_edge_user_list, key=lambda x: x[1])
      # f.write('No. of followers for ' + spreader + ': ' + str(len(in_edge_sorted_user_list)) + '\n')
      inf_edge_list = list(G_fol.neighbors(spreader, mode = 'in'))
      d['next_spreaders_count'] = len(inf_edge_list)
      d['next_spreaders'] = [i for i in inf_edge_list]
      if len(inf_edge_list) > 0:
        inf_edge_user_list = [[i, float(TSM_scores[i][0])] for i in inf_edge_list]
        inf_edge_sorted_list = sorted(inf_edge_user_list, key=lambda x: x[1])
        print(in_edge_sorted_list.index(inf_edge_sorted_list[0]))
        spreader_bel_rank = [in_edge_sorted_list.index(i) for i in inf_edge_sorted_list]
        d['spreader_bel_rank'] = sorted(spreader_bel_rank)
      else:
        d['spreader_bel_rank'] = 'No next spreaders'
        print(spreader, 'has not inf spread paths from it')
        spreader_with_no_paths += 1
      d_dump = json.dumps(d)
      f.write(d_dump + '\n')

    print('No. of spreaders with no paths from them', spreader_with_no_paths)





