"""
Usage: python3 highlight.py <user_id> <article_id>
Outputs: a JSON document specifying which paragraphs of the article should be
highlighted based on the user's article history
"""

import psycopg2
import sys

"""
highlight the article based on the user's history using some method
params:
    article: string containing article to be highlighted
    user_history: list of article strings
"""
def highlight(article, user_history):
    # insert method here
    pass

user_id = sys.argv[1]
article_id = sys.argv[2]

conn = psycopg2.connect("host=localhost dbname=article-filter_test user=pguser password=dbpass")
cur = conn.cursor()
cur.execute(('SELECT a.text FROM articles a INNER JOIN user_articles ua ' 
    'on  a.id=ua.article_id WHERE ua.user_id = %s AND a.id != %s'), 
    (user_id, article_id))
user_history = []
read_article = cur.fetchone()
while read_article is not None:
    user_history.append(read_article[0])
    read_article = cur.fetchone()
    
cur.execute('SELECT a.text From articles a WHERE a.id = %s', article_id)
article = cur.fetchall()[0][0]

result = highlight(article, user_history)
print(result)

