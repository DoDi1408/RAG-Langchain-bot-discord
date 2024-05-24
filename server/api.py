import json
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from indexer import superIndexingFunction
from ragChain import createRagChain

app = Flask(__name__)
CORS(app, support_credentials=True)

vectorstore = superIndexingFunction()
rag_chain = createRagChain(vectorstore)

@app.route('/prompt', methods=['POST'])
@cross_origin(origin='*',supports_credentials=True)
def create_prompt():
    user_prompt = json.loads(request.data)
    print(user_prompt)
    if 'message' not in user_prompt:
        return jsonify({ 'error': 'missing message' }), 400

    output = ""
    for chunk in rag_chain.stream(user_prompt['message']):
        output += chunk

    return jsonify({'output': output}), 200

if __name__ == '__main__':
   app.run(port=5000)