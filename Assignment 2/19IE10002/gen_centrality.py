import snap
import os

filename = "facebook_combined.txt"

G = snap.LoadEdgeList(snap.PUNGraph,filename,0,1) #3rd and 4th parameters are column indices of source and destination nodes

#G is now the required undirected graph

n = G.GetNodes()

cls = snap.TIntFltH() # closeness centrality dict containing (node id, closeness centrality) as a (key,value) pair

for itr1 in G.Nodes():
    cc = 0
    s = 0
    sp = snap.TIntH() # A hash table containing shortest paths from itr1.node to all other nodes
    a = snap.GetShortPath(G,itr1.GetId(),sp)
    for j in sp:
        s += sp[j]
    cc = (n-1)/s
    cc = round(cc,6)
    cls[itr1.GetId()] = cc


cls.SortByDat(False)        #sorting in descending order by value. parameter Asc == False

# now have to output cls in a text file

os.mkdir("centralities")
os.chdir("centralities")

filename = "closeness.txt"
f = open(filename,"w")
for key in cls:
    f.write(str(key) + " " + str(cls[key]) + "\n")
f.close()


pr = snap.TIntFltH()  # pagerank dict containing (node id, closeness centrality) as a (key,value) pair

n_pr = 0    #no of nodes with Id divisible by 4
for it in G.Nodes():
    if( (it.GetId() %4) == 0):
        n_pr += 1

#n_pr number of slots in the non uniform(biased) vector will have non zero input. others will have zero

a = 0.8 # damping factor

for itr in G.Nodes():   #initializing pageranks for all nodes
    pr[itr.GetId()] = 1

iteration_MAX = 128 # total number of iterations to be done. a number more than 100 and a power of 2 has been chosen.

for i in range(iteration_MAX):
    sum = 0
    for itr in G.Nodes():
        t = 0
        for Id in itr.GetOutEdges():
            itr2 = G.GetNI(Id)
            t += ( pr[Id]/itr2.GetOutDeg() )
        
        pr[itr.GetId()] = a * t
        
        if( (itr.GetId() % 4) == 0 ):
            pr[itr.GetId()] += (1-a) * (1/n_pr)
        
        sum += pr[itr.GetId()]
    
    for key in pr:          #normalization
        pr[key] = pr[key]/sum

for key in pr:          #normalization
    pr[key] = round(pr[key],6)

pr.SortByDat(False)

filename = "pagerank.txt"
f = open(filename,"w")
for key in pr:
    f.write(str(key) + " " + str(pr[key]) + "\n")
f.close()

