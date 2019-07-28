"""For B and C of every community, generates count, in-degree and out-degree stats"""

import os
import re
import sys
import json
import igraph
import networkx as nx

def B_C_degree_stats(tweet_id, cluster, graph):
  graph_nodes = set(range(0, len(graph.vs)))

  with open(tweet_id + '/B_C_degree_stats_l1_' + tweet_id + '.txt', 'w') as f:
    for cl in cluster:
      d = dict()
      print('for cl: ', cl)

      d['cl'] = cl
      cluster_nodes = set(cluster[cl])
      # boundary_edges_out = list(my_edge_boundary(graph, graph_nodes.difference(cluster_nodes), cluster_nodes))
      boundary_edges_in = list(my_edge_boundary(graph, cluster_nodes, graph_nodes.difference(cluster_nodes)))
      boundary_nodes = set([int(i[0]) for i in boundary_edges_in])
      # in_neighbor_nodes = set([str(i[1]) for i in boundary_edges_in])
      # out_neighbor_nodes = set([str(i[0]) for i in boundary_edges_out])
      core_nodes = (cluster_nodes.difference(boundary_nodes))
      # d_H_list = [i[1] for i in H.degree()]
      # plot(np.asarray(d_H_list), tweet_id, cl, 'Degree dist.')
      d['nodes_count'] = len(cluster_nodes)
      d['boundary_count'] = len(boundary_nodes)
      d['core_count'] = len(core_nodes)

      ''' in-degree..'''
      in_d_boundary_nodes = graph.degree(vertices = list(boundary_nodes), mode = 'in')
      in_d_boundary_nodes_list = [i for i in in_d_boundary_nodes]
      fq_in_d_boundary_nodes = {i: in_d_boundary_nodes_list.count(i) for i in set(in_d_boundary_nodes_list)}
      # plot(np.asarray(in_d_boundary_nodes_list), tweet_id, cl, 'in-d of b-nodes')
      print('fq_in_d_boundary_nodes: ', fq_in_d_boundary_nodes)
      d['B_in_d'] = fq_in_d_boundary_nodes

      in_d_core_nodes = graph.degree(vertices = list(core_nodes), mode = 'in')
      in_d_core_nodes_list = [i for i in in_d_core_nodes]
      fq_in_d_core_nodes = {i: in_d_core_nodes_list.count(i) for i in set(in_d_core_nodes_list)}
      # plot(np.asarray(in_d_core_nodes_list), tweet_id, cl, 'in-d of c-nodes')
      print('fq_in_d_core_nodes: ', fq_in_d_core_nodes)
      d['C_in_d'] = fq_in_d_core_nodes

      ''' out-degree..'''
      out_d_boundary_nodes = graph.degree(vertices = list(boundary_nodes), mode = 'out')
      out_d_boundary_nodes_list = [i for i in out_d_boundary_nodes]
      fq_out_d_boundary_nodes = {i: out_d_boundary_nodes_list.count(i) for i in set(out_d_boundary_nodes_list)}
      # plot(np.asarray(out_d_boundary_nodes_list), tweet_id, cl, 'out-d of b-nodes')
      print('fq_out_d_boundary_nodes: ', fq_out_d_boundary_nodes)
      d['B_out_d'] = fq_out_d_boundary_nodes

      out_d_core_nodes = graph.degree(vertices = list(core_nodes), mode = 'out')
      out_d_core_nodes_list = [i for i in out_d_core_nodes]
      fq_out_d_core_nodes = {i: out_d_core_nodes_list.count(i) for i in set(out_d_core_nodes_list)}
      # plot(np.asarray(out_d_core_nodes_list), tweet_id, cl, 'out-d of c-nodes')
      print('fq_out_d_core_nodes: ', fq_out_d_core_nodes)
      d['C_out_d'] = fq_out_d_core_nodes

      dict_str = json.dumps(d)
      f.write(dict_str + '\n')

def my_edge_boundary(G, nbunch1, nbunch2):
  nset2 = set(nbunch2)
  num_nodes = len(G.vs)
  return [(n1,n2) for n1 in nbunch1 if n1 < num_nodes for n2 in G.neighbors(n1, mode = 'out') if n2 in nset2]