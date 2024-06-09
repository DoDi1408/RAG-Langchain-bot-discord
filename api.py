import json
from logging.config import dictConfig
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from indexer import superIndexingFunction
from ragChain import createRagChain

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
CORS(app, support_credentials=True)

vectorstore = superIndexingFunction()
rag_chain = createRagChain(vectorstore)

@app.route('/prompt', methods=['POST'])
@cross_origin(origin='*',supports_credentials=True)
def create_prompt():
    app.logger.info('received a /prompt')
    user_prompt = json.loads(request.data)
    app.logger.info(user_prompt)
    if 'message' not in user_prompt:
        return jsonify({ 'error': 'missing message' }), 400

    output = ""
    for chunk in rag_chain.stream(user_prompt['message']):
        output += chunk

    return jsonify({'output': output}), 200

if __name__ == "__main__":
    from waitress import serve
    PORT = 5134
    serve(app, host="0.0.0.0", port=PORT)