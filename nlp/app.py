from flask import Flask
from flask import request
import json
from highlight_from_db import highlight_for_user
from models.sif import SIF
import logging, sys, traceback
app = Flask(__name__)

model = None

@app.route('/highlight', methods=['POST'])
def highlight():
    user_id = request.get_json().get('user_id', '')
    article_id = request.get_json().get('article_id', '')
    app.logger.info(request.get_json())
    highlighted =  highlight_for_user(model, user_id, article_id, app.logger)
    return json.dumps(highlighted)
    


if __name__ == '__main__':
    model = SIF(mode='para')
    app.run(debug=True, host='0.0.0.0', port=5001)
