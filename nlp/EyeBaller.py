# This file is for testing whether means of partitioning data in models/preprocess are working right

# import models.preprocess as preprocess
from models.sif import SIF
import sys
import newspaper
import traceback


model = SIF(mode= 'para')
paras, sims = [], []

def scrape(url):
	a = newspaper.Article(url)
	a.download()
	a.parse()
	# return a.text
	return {'title': a.title, 'text': a.text, 'url': url}


corpus = []

while(True):
	instruction = input("Enter [add/read] [url]:")
	instr = instruction.split(" ")
	cmd, url = instr[0:2]
	if not (cmd=="add" or cmd=="read"):
		print("please enter cmd 'read' or 'add'")
	try:
		article = scrape(url)
		# print(article['title'])
		if cmd=="add":
			print("adding article {}".format(article['title']))
			corpus.append(article['text'])
			model.load_corpus(corpus)
		elif cmd=="read":
			print("reading article {}".format(article['title']))
			paras, sims = model.highlight(article['text'])
			for i in range(min(len(paras), len(sims))):
				start, end = paras[i]
				text = article['text'][start:end-1]
				if sims[i]<0.6:
					text = text.upper()
				print(text)
			# toHighlight = []
	except:
		print("Unexpected error:", traceback.print_exc())
		

	
# print(cmd, url)
# print('Hello', person)

