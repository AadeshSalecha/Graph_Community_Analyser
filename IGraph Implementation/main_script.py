import re
import os
import csv
import igraph
import pickle
import bel_ranks
import concatenator
import spreader_role
import subgraph_stats
import igraph_TSM_implementation
import igraph_louvain_implementation

tweetID = 'temp2'
id_dict = None
igraph_G = None
TSM_scores = None
louvain = None

def main():
  global id_dict
  global igraph_G
  global TSM_scores

  # Make ID Dict, Edges
  id_dict, edges = compute_id_dict_and_edges()

  num_nodes = len(id_dict)

  # Make IGraph
  igraph_G = igraph.Graph(n = num_nodes, edges = edges, directed = True)

  print('No. of nodes = ', num_nodes)
  print('No. of edges = ', len(edges))

  # Run TSM
  # TSM_scores = compute_TSM_scores(graph = igraph_G)

  undirected_igraph_G = igraph.Graph(n = num_nodes, edges = edges, directed = False)

  # Consider only those spreaders whose network could be extracted. (i.e. excluding 'protected' twitter users)
  l_spreaders = compute_l_spreaders()

  # Run Louvain
  louvain = igraph_louvain_implementation.louvain(tweet_id = tweetID, graph = undirected_igraph_G)

  # Run NBC
  igraph_louvain_implementation.NBC(tweet_id = tweetID, cluster = louvain, graph = igraph_G, l_spreaders = l_spreaders)
  
  # Run graph stats  
  subgraph_stats.B_C_degree_stats(tweet_id = tweetID, cluster = louvain, graph = igraph_G)

  # Print Core, Boundary and Neighbor nodes
  spreader_role.sp_role(tweet_id = tweetID, l_spreaders = l_spreaders)

  # Print spreader, next_spreader stats
  # bel_ranks.spread_edge_bel(tweet_id = tweetID, TSM_scores = TSM_scores, id_dict = id_dict, G = igraph_G, l_spreaders = l_spreaders)

# Uses igraph_TSM to compute TSM scores
def compute_TSM_scores(graph):
  TSM_scores = igraph_TSM_implementation.TSM(tweet_id = tweetID, graph = graph, vertices = range(0, len(graph.vs)))
  return TSM_scores

def compute_l_spreaders():
  l_spreaders = []
  retweet_file = ''.join(['retweets_', tweetID, '.txt'])
  with open(tweetID + '/' + retweet_file, 'r') as infile:
    for line in infile:
      l_spl = re.split(r'[,]', line.rstrip())
      if l_spl[2] in id_dict:
        l_spreaders.append(id_dict[l_spl[2]])

  return l_spreaders

########################################### 
# 
# Does not need a networkx file
#
# Makes the id_dict structure by reading
# friends and follower scrapes for a tweet
#
########################################### 
def compute_id_dict_and_edges():
  id_dict = {}
  edges = set()
  
  count = 0
  for folder in [tweetID + '/Followers_l1_' + tweetID, tweetID + '/Friends_l1_' + tweetID]:
    cur_files = [f for f in os.listdir(folder) if os.path.isfile(folder + '/' + f)]

    for f in cur_files:
      with open(folder + '/' + f, mode='r') as inptr:
        reader = csv.reader(inptr)
        for row in reader:
          if(len(row) == 2):
            if(row[0] not in id_dict):
              id_dict[row[0]] = count
              count += 1
            if(row[1] not in id_dict):
              id_dict[row[1]] = count 
              count += 1
            
            edges.add((id_dict[row[0]], id_dict[row[1]]))

  return id_dict, list(edges)

def compute_id_dict_and_edges_from_ids_file():
  id_dict = dict()
  ids_file = ''.join(['ids_l1_', tweetID, '.txt'])
  edges = set()
  with open(tweetID + '/' + ids_file) as infile:
    for line in infile:
      l_spl = re.split(r'[,]', line.rstrip())
      id_dict[l_spl[0]] = int(l_spl[1])

  for folder in [tweetID + '/Followers_l1_' + tweetID, tweetID + '/Friends_l1_' + tweetID]:
    cur_files = [f for f in os.listdir(folder) if os.path.isfile(folder + '/' + f)]
    
    for f in cur_files:
      with open(folder + '/' + f, mode='r') as inptr:
        reader = csv.reader(inptr)
        for row in reader:
          if(len(row) == 2):
            edges.add((id_dict[row[0]], id_dict[row[1]]))

  return id_dict, list(edges)

def make_directory(dirname):
  if not os.path.exists(dirname):
    os.makedirs(dirname)

if __name__ == '__main__':
  main()