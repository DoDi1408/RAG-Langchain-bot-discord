from indexer import superIndexingFunction
from ragChain import createRagChain

vectorstore = superIndexingFunction()
rag_chain = createRagChain(vectorstore)

def get_response(user_input: str) -> str:
    output = ""
    for chunk in rag_chain.stream(user_input):
        output += chunk
    return output