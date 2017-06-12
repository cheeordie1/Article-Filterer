# This file is for testing whether means of partitioning data in models/preprocess are working right

# import models.preprocess as preprocess
from models.sif import SIF
import newspaper

model = SIF(1, 1000, mode= 'sentence')
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
	if cmd=="add":
		article = scrape(url)
		print("adding article {}".format(article.title))
		corpus.add(article.text)
		model.load_corpus(corpus)

	elif cmd=="read":
		article = scrape(url)
		print("reading article {}".format(article.title))
		paras, sims = model.highlight(new_article)
		print(paras)
	else:
		print("please enter cmd 'read' or 'add'")
# print(cmd, url)
# print('Hello', person)

