import snap
import os


filename = "facebook_combined.txt"

G1 = snap.LoadEdgeList(snap.PUNGraph, filename, 0, 1)    #3rd and 4th parameters are column indices of source and destination nodes

for itr in G1.Nodes():
    if( (itr.GetId() % 5) == 0):
        G1.DelNode(itr.GetId())


filename = "com-amazon.ungraph.txt"

G2 = snap.LoadEdgeList(snap.PUNGraph,filename,0,1)

for it in G2.Nodes():
    if((it.GetId()%4)!=0):
        G2.DelNode(it.GetId())
        
os.mkdir("subgraphs")	#made a folder called "subgraphs"
os.chdir("subgraphs")	#now, inside "subgraphs"
        
snap.SaveEdgeList(G1,"facebook.elist")	#storing the required data set inside "subgraph"
snap.SaveEdgeList(G2,"amazon.elist")





