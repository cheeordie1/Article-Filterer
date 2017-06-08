# highlightNewTest.py


# we want to 
# 	extract feature vector
# 	perform nearest neighbor search with distance function


alreadyRead = [
"The cat sat on the mat",
"Horton heard a who",
"I do not like green eggs and ham"
]

weights = np.array([1,1,1])



new1 = "The mat was sat on by the cat"
new2 = "A feline reclined on the carpet"
k = 2

knowledge = np.array([[-1, -1], [-2, -1], [3, 2]]) #replace with feature extraction on all read text




l = len(knowledge)

x = [3,3]
X = np.append(knowledge,[x],axis=0)
# print X[l-1]

# this will be O(n^2) but could be implemented in O(n)
nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(X)
distances, indices = nbrs.kneighbors(X)

xNbrIndices = indices[l][1:]
xNbrDistances = distances[l][1:]
xWeights = np.take(weights, xNbrIndices)

print x
print knowledge
print xNbrIndices
weightedSimilarity = xWeights/xNbrDistances
print np.sum(weightedSimilarity)

# Dummy data for demoing functionality
# document = "This is a document for development purposes. It contains some redundant information."+"\nThis section is redundant"+"\nThis line contains new information"+"\nThis section is redundant"+"\nThis section is new"

# print("We're going to process the following document with new information capitalized:")
# print("\n")
# print(document)
# print("\n")
# result = main(document)
# for section, new in result:
# 	if new:
# 		print section.upper()
# 	else:
# 		print section




