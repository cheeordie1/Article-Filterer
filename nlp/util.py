# util.py

from sklearn.neighbors import NearestNeighbors
import numpy as np

def getkNearestNeighbors(y,X,dist,k=1):
	nbrs = {}
	for x in X:
		d = dist(x,y)
		if len(nbrs) < k:
			nbrs[x] = d
		else:
			furthestNearNeighbor = max(nbrs, key=nbrs.get)
		 	if d < nbrs[furthestNearNeighbor]:
				del nbrs[furthestNearNeighbor]
				nbrs[x] = d
	return nbrs
