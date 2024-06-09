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
        web_paths=(["https://discoelysium.fandom.com/wiki/Authority",
                   "https://discoelysium.fandom.com/wiki/Composure",
                   "https://discoelysium.fandom.com/wiki/Conceptualization",
                   "https://discoelysium.fandom.com/wiki/Drama",
                   "https://discoelysium.fandom.com/wiki/Electrochemistry",
                   "https://discoelysium.fandom.com/wiki/Empathy",
                   "https://discoelysium.fandom.com/wiki/Encyclopedia",
                   "https://discoelysium.fandom.com/wiki/Endurance",
                   "https://discoelysium.fandom.com/wiki/Esprit_de_Corps",
                   "https://discoelysium.fandom.com/wiki/Half_Light",
                   "https://discoelysium.fandom.com/wiki/Hand-Eye_Coordination",
                   "https://discoelysium.fandom.com/wiki/Inland_Empire",
                   "https://discoelysium.fandom.com/wiki/Interfacing",
                   "https://discoelysium.fandom.com/wiki/Logic",
                   "https://discoelysium.fandom.com/wiki/Pain_Threshold",
                   "https://discoelysium.fandom.com/wiki/Perception",
                   "https://discoelysium.fandom.com/wiki/Physical_Instrument",
                   "https://discoelysium.fandom.com/wiki/Reaction_Speed",
                   "https://discoelysium.fandom.com/wiki/Rhetoric",
                   "https://discoelysium.fandom.com/wiki/Savoir_Faire",
                   "https://discoelysium.fandom.com/wiki/Shivers",
                   "https://discoelysium.fandom.com/wiki/Suggestion",
                   "https://discoelysium.fandom.com/wiki/Visual_Calculus",
                   "https://discoelysium.fandom.com/wiki/Volition"]),)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    return vectorstore