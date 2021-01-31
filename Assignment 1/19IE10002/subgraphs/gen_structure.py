#computation

import snap
import os
import sys

Rnd = snap.TRnd(42)	#seed = 42
Rnd.Randomize()

filename = sys.argv[1]    # filename would be facebook.elist or amazon.elist

G = snap.LoadEdgeList(snap.PUNGraph, filename,0,1) # 3rd and 4th parameters are column indices of source and destination nodes

n =  G.GetNodes()
print("Number of nodes:",n)

m = G.GetEdges()
print("Number of edges:",m)

print("Number of nodes with degree=7:",snap.CntDegNodes(G,7))

max_ID = snap.GetMxDegNId(G)    #gives us the ID of one random node with maximum degree
it = G.GetNI(max_ID)            #iterator to that node
max = it.GetDeg()               #finding the maximum degree

print("Node id(s) with highest degree:", end = " ")
for itr in G.Nodes():
    if(itr.GetDeg() == max):    #if the degree of a node is the maximum degree, then print it
        print(itr.GetId(), end=" ")
print("\b")

os.mkdir("plots")	#creating a folder "plots" inside "subgraphs"
os.chdir("plots")	#now we're inside "plots"

snap.PlotInDegDistr(G, "deg_dist_" + filename, "Degree Distribution") #for an undirected graph, indegree = outdegree = degree for all nodes

d1 = snap.GetBfsFullDiam(G, 10)
d2 = snap.GetBfsFullDiam(G, 100)
d3 = snap.GetBfsFullDiam(G, 1000)

print("Approximate full diameter by sampling 10 nodes:", d1)
print("Approximate full diameter by sampling 100 nodes:", d2)
print("Approximate full diameter by sampling 1000 nodes:", d3)

dm = (d1+d2+d3)/3   #dm is the mean of the diameters

dvar = ( (d1 - dm) ** 2 + (d2 - dm) ** 2 + (d3 - dm) ** 2 )/3	#dvar is the variance of the diameters
print("Approximate full diameter (mean and variance):", round(dm,4),",",round(dvar,4))

ed1 = snap.GetBfsEffDiam(G, 10)
ed2 = snap.GetBfsEffDiam(G, 100)
ed3 = snap.GetBfsEffDiam(G, 1000)

print("Approximate effective diameter by sampling 10 nodes:", round(ed1,4))
print("Approximate effective diameter by sampling 100 nodes:", round(ed2,4))
print("Approximate effective diameter by sampling 1000 nodes:", round(ed3,4))

edm = (ed1+ed2+ed3)/3   #edm is the mean of effective diameters

edvar = ( (ed1 - edm) ** 2 + (ed2 - edm) ** 2 + (ed3 - edm) ** 2 )/3    #edvar is the variance of effective diameters
print("Approximate effective diameter (mean and variance):", round(edm,4),",",round(edvar,4))

snap.PlotShortPathDistr(G, "shortest_path_"+filename, "Shortest path length distribution")

G_Scc = snap.GetMxScc(G)        #for an undirected graph, strong and weak connected component mean the same thing
n_Scc = G_Scc.GetNodes()

print("Fraction of nodes in largest connected component:", round( (n_Scc/n),4))

Bridge_vector = snap.TIntPrV()  #vector of bridge edges
snap.GetEdgeBridges(G, Bridge_vector)
print("Number of edge bridges:",len(Bridge_vector))

Art_points_vector = snap.TIntV()    #vector of articulation points
snap.GetArtPoints(G, Art_points_vector)
print("Number of articulation points:",len(Art_points_vector))

snap.PlotSccDistr(G,"connected_component_" + filename, "Distribution of size of connected component")

C_avg = snap.GetClustCf(G)
print("Average Clustering coefficient:",round(C_avg,4))

print("Number of triads:", snap.GetTriads(G))

rnode = G.GetRndNId(Rnd)    #random node ID
print("Clustering coefficient of random node",rnode,":",round(snap.GetNodeClustCf(G,rnode),4))

rnode = G.GetRndNId(Rnd)    #random node ID again chosen
print("Number of triads random node",rnode," participates:",snap.GetNodeTriads(G,rnode))

print("Number of edges that participate in at least one triad:",snap.GetTriadEdges(G))

snap.PlotClustCf(G,"clustering_coefficient_" + filename, "Distribution of clustering coefficient")







