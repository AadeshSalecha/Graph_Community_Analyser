import pickle
import os
import csv
import igraph
import concatenator
import igraph_TSM_implementation
import igraph_louvain_implementation

global_dir = './Test/'
tweetIDs = [('1127551496260702208', 'FALSE'), ('1132905364599578625', 'TRUE'), ('1126744497230991361', 'FALSE'), ('1119881405259898880', 'TRUE'), ('1129639755619164160', 'FALSE'), ('1118128339904913408', 'TRUE'), ('1119878414796820480', 'TRUE'), ('1133759873114615808', 'FALSE'), ('1130789245457555456', 'FALSE'), ('1129034548937932800', 'FALSE')] 
id_dict = None
igraph_G = None
TSM_scores = None
louvain = None

def main():
  global id_dict
  global igraph_G
  global TSM_scores

  make_directory(global_dir + '/Concatenated')

  #############################
  # Combine all graphs into one
  #############################

  all_tweet_networks = [f for f in os.listdir(global_dir) if (not os.path.isfile(global_dir + '/' + f))]
  filter_out = ['All_Followers', 'All_Friends', '__pycache__', 'sample', 'Concatenated']
  all_tweet_networks = list(filter(lambda x : all([w not in x for w in filter_out]), all_tweet_networks))

  concatenator.combine_networks(cur_dir = global_dir, all_tweet_networks = all_tweet_networks)
  #############################

  # Make ID Dict, Edges
  id_dict, edges = compute_id_dict_and_edges()

  # Make IGraph
  igraph_G = igraph.Graph(edges, directed = True)

  # Run TSM
  TSM_scores = compute_TSM_scores(graph = igraph_G)

  print('No. of nodes = ', len(id_dict))
  print('No. of edges = ', len(edges))
  
  # Run louvain
  if(not os.path.isfile(global_dir + '/Concantenated/louvain')):
    undirected_igraph_G = igraph.Graph(edges, directed = False)
    louvain = igraph_louvain_implementation.louvain(cur_dir = global_dir, graph = undirected_igraph_G)

  # for each tweet run rest of files
  for tweet_id, truth_val in tweetIDs:
    process_tweetID(tweet_id)

def compute_TSM_scores(graph):
  if(os.path.isfile(global_dir + 'Concatenated/TSM_scores')):
    TSM_scores = pickle.load(open(global_dir + '/Concatenated/TSM_scores', 'rb'))
  
  else:
    TSM_scores = igraph_TSM_implementation.TSM(cur_dir = global_dir, graph = graph, vertices = range(0, len(graph.vs)))

  return TSM_scores

def compute_id_dict_and_edges():
  id_dict = {}
  edges = []
  
  if(os.path.isfile(global_dir + '/Concatenated/id_dict') and os.path.isfile(global_dir + '/Concatenated/edges')):
    id_dict = pickle.load(open(global_dir + '/Concatenated/id_dict', 'rb'))
    edges = pickle.load(open(global_dir + '/Concatenated/edges', 'rb'))
  
  else:
    count = 0
    for folder in [global_dir + '/All_Followers', global_dir + '/All_Friends']:
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
              
              edges.append((id_dict[row[0]], id_dict[row[1]]))

    pickle.dump(id_dict, open(global_dir + '/Concatenated/id_dict', 'wb'))
    pickle.dump(edges, open(global_dir + '/Concatenated/edges', 'wb'))

  return id_dict, edges

def process_tweetID(tweet_id):
  # Consider only those spreaders whose network could be extracted. (i.e. excluding 'protected' twitter users)
  l_spreaders = []
  retweet_file = ''.join(['retweets_', tweet_id, '.txt'])
  with open(global_dir + '/' + tweet_id + '/' + retweet_file) as infile:
    for line in infile:
      l_spl = re.split(r'[,]', line.rstrip())
      if l_spl[2] in id_dict:
        l_spreaders.append(id_dict[l_spl[2]])

  igraph_louvain_implementation.NBC(cur_dir = global_dir, tweet_id = tweet_id, cluster = louvain, graph = igraph_G, l_spreaders = l_spreaders)
  subgraph_stats.B_C_degree_stats(tweet_id = tweet_id, cluster = louvain, graph = igraph_G)
  # spreader_role.sp_role(tweet_id, l_spreader)
  # bel_ranks.spread_edge_bel(tweet_id, id_dict, G, l_spreaders)

def make_directory(dirname):
  if not os.path.exists(dirname):
    os.makedirs(dirname)

if __name__ == '__main__':
  # main()