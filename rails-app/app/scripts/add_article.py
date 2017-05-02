from newspaper import Article
import sys
import json

url = sys.argv[1]
a = Article(url)
a.download()
a.parse()
retval = {}
