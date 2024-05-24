from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

import os

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def superIndexingFunction():
    # Load, chunk and index the contents of the blog.
    loader = WebBaseLoader(
        web_paths=(["https://www.espn.com.mx/futbol/mexico/nota/_/id/13697968/cruz-azul-vs-america-final-de-ida-en-vivo-clausura-2024",
                   "https://mexico.as.com/futbol/futbol-mexicano/cruz-azul-vs-america-en-vivo-liga-mx-final-de-ida-del-clausura-2024-hoy-en-directo-n/",
                   "https://www.mediotiempo.com/futbol/liga-mx/resumen-partido-cruz-azul-vs-america-ida-clausura-2024",
                   "https://vamoscruzazul.bolavip.com/noticias/cruz-azul-vs-america-en-vivo-sigue-el-juego-por-la-ida-de-la-final-del-clausura-2024"]
                   ),
    )
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    return vectorstore