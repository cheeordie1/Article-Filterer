from sklearn.neighbors import NearestNeighbors
import numpy as np


# Splits the new document into relevant sections
def getSections(doc):
	return doc.split("\n")


"""
hasCloseNeighbors(data,knowledge,dist,threshold)

params:
	data: representation of potentially new block of information
	knowledge: a model of what we already know, consisting of 'knowns'
	represented the same way 'data' is
	dist: distance metric for comparing 'data' to existing 'knowns'
	threshold: the min distance below which we consider 'data' 
	to be the same as a 'known'
return:
	Boolean representing whether the 'data' is sufficiently
	close to any knowns to be considered redundant information

"""

def hasCloseNeighbors(data,knowledge,dist,threshold):
	for known in knowledge:
		if dist(data,known) < threshold:
			return True
	return false


"""
Returns and array of (string,boolean) 

params:
	doc: document to be highlighted by section
	preprocess: function that represents section the same way 'knowledge' is represented
	isNew: function that determines whether a section contains new information
	knowledge: current model of user knowledge
return:
	zipped array of (string,boolean) with each element representing a 
	section of text and whether that section contains new information
"""
def highlightDocument(doc,preprocess,isNew,knowledge):
	sections = getSections(doc)
	newInfo = []
	for section in sections:
		data = preprocess(section)
		if(isNew(data,knowledge)):
			newInfo.append(True)
		else:
			newInfo.append(False)
	return zip(sections,newInfo)

