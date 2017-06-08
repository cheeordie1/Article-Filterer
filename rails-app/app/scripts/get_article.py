from newspaper import Article
import sys
import json

url = sys.argv[1]
try:
    a = Article(url)
    a.download()
    a.parse()
    retval = {}
    retval["text"] = a.text
    retval["title"] = a.title
    retval["authors"] = a.authors
    print(json.dumps(retval))
except:
    retval = {}
    retval["error"] = "error"
    print(json.dumps(retval))
