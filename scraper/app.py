from flask import Flask
from flask import request
from newspaper import Article
import json
import logging, sys, traceback
app = Flask(__name__)

@app.route('/get_article', methods=['POST'])
def get_article():
    try:
        url = request.get_json().get('url', '')
        app.logger.info(request.get_json())
        a = Article(url)
        a.download()
        a.parse()
        retval = {}
        retval["text"] = a.text
        retval["title"] = a.title
        retval["authors"] = a.authors
        return json.dumps(retval)
    except Exception as e:
        app.logger.error(traceback.format_exception(None, e, e.__traceback__))
        retval = {}
        retval["error"] = "error"
        return json.dumps(retval)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
