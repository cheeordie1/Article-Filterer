

# TODO: update this function to compare section to our current model and return true if there's significant overlap
def isRedundant(section):
	if "This section is redundant" in section:
		return True
	return False

# Returns an array of boolean values corresponding to whether each section is new information
def highlightNewSections(sections):
	result = []
	for section in sections:
		if isRedundant(section):
			result.append(False)
		else:
			result.append(True)
	return result

# Splits the new document into relevant sections
def getSections(doc):
	return doc.split("\n")

# Returns and array of (string,boolean) with each element representing a s
# ection of text and whether that section contains new information
def main(doc):
	sections = getSections(doc)
	highlighted = highlightNewSections(sections)
	return zip(sections,highlighted)

# Dummy data for demoing functionality
document = "This is a document for development purposes. It contains some redundant information."+"\nThis section is redundant"+"\nThis line contains new information"+"\nThis section is redundant"+"\nThis section is new"

print("We're going to process the following document with new information capitalized:")
print("\n")
print(document)
print("\n")
result = main(document)
for section, new in result:
	if new:
		print section.upper()
	else:
		print section


