import snap
import os

filename = "facebook_combined.txt"

G = snap.LoadEdgeList(snap.PUNGraph,filename,0,1) #3rd and 4th parameters are column indices of source and destination nodes

#G is now the required undirected graph

n = G.GetNodes()
os.chdir("centralities")

#for closeness

cls_ib = snap.TIntFltH() # closeness centrality inbuilt (dict)
for itr in G.Nodes():
    cls_ib[itr.GetId()] = snap.GetClosenessCentr(G,itr.GetId())
    cls_ib[itr.GetId()] = round(cls_ib[itr.GetId()],6)

cls_ib.SortByDat(False)

cls = snap.TIntFltH() #closeness centrality dict

filename = "closeness.txt"
f = open(filename,"r")

for line in f:
    l = line.split()
    cls[int(l[0])] = float(l[1])
f.close()

nodes_ib = list()
for key in cls_ib:
    nodes_ib.append(key)
top_ib = nodes_ib[:100] #keys of top 100 nodes
top_ib_set = set(top_ib)

nodes = list()
for key in cls:
    nodes.append(key)
top = nodes[:100]   #keys of top 100 nodes
top_set = set(top)

top_intrsct = top_ib_set.intersection(top_set)

cls_overlap = len(top_intrsct)  #no of overlaps

print("overlaps for Closeness Centrality:",cls_overlap)

# for pagerank

pr_ib = snap.TIntFltH() # pagerank inbuilt (dict)

snap.GetPageRank(G,pr_ib,0.8)

for key in pr_ib:
    pr_ib[key] = round(pr_ib[key], 6)
    
pr_ib.SortByDat(False)

pr = snap.TIntFltH() #page rank

filename = "pagerank.txt"
f = open(filename,"r")

for line in f:
    l = line.split()
    pr[int(l[0])] = float(l[1])
f.close()

nodes_ib = list()
for key in pr_ib:
    nodes_ib.append(key)
top_ib = nodes_ib[:100] #keys of top 100 nodes
top_ib_set = set(top_ib)

nodes = list()
for key in pr:
    nodes.append(key)
top = nodes[:100]   #keys of top 100 nodes
top_set = set(top)

top_intrsct = top_ib_set.intersection(top_set)

pr_overlap = len(top_intrsct)  #no of overlaps

print("overlaps for PageRank Centrality:",pr_overlap)


