"""
Usage: python3 highlight_from_db.py <user_id> <article_id>
Outputs: a JSON document specifying which paragraphs of the article should be
highlighted based on the user's article history
"""

import psycopg2
import sys
from models.tfidf_bog import TFIDF_BOG
import json

"""
highlight the article based on the user's history using some method
params:
    article: string containing article to be highlighted
    user_history: list of article strings
returns:
    list of entries for each paragraph in sequential order where each entry is in the format:
        {text: <text>, highlighted: True or False}
"""
def highlight_tfidf(new_article, user_history, logger):
    model = TFIDF_BOG()
    logger.info(user_history)
    model.load_corpus(user_history)
    paras, sims = model.highlight(new_article)
    paragraphs = []
    for i in range(len(paras)):
        entry = {}
        entry['text'] = paras[i]
        if sims[i] > 0.1:
            entry['highlighted'] = True
            logger.info("TRUE")
            logger.info(sims[i])
        else:
            entry['highlighted'] = False
            logger.info("FALSE")
            logger.info(sims[i])
        paragraphs.append(entry)
    return paragraphs


def highlight_for_user(user_id, article_id, logger):
    conn = psycopg2.connect("host=postgres dbname=article-filter_test user=pguser password=dbpass")
    cur = conn.cursor()
    cur.execute(('SELECT a.text FROM articles a INNER JOIN user_articles ua ' 
        'on  a.id=ua.article_id WHERE ua.user_id = %s AND a.id != %s'), 
        (user_id, article_id))
    user_history = []
    read_article = cur.fetchone()
    #logger.info(read_article)
    while read_article is not None:
        text = read_article[0]
        if text is not None:
            user_history.append(text)
        read_article = cur.fetchone()

    cur.execute('SELECT a.text From articles a WHERE a.id = %s', (article_id,))
    fetchall = cur.fetchall()
    #logger.info(fetchall)
    article = fetchall[0][0]
    #logger.info(article)

    result = highlight_tfidf(article, user_history, logger)
    #print(json.dumps(result))
    return result

