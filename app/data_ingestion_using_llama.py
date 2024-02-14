from pathlib import Path
import os
import pypdf
import pgvector
import asyncpg
from sqlalchemy import make_url
from llama_index import SimpleDirectoryReader, LLMPredictor, StorageContext
from llama_index.indices import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
import openai
from dotenv import load_dotenv
load_dotenv()
import psycopg2
# Configure prompt parameters and initialise helper
max_input_size = 4096
num_output = 256
max_chunk_overlap = 20

host = 'localhost'
port = '5432'
username = 'postgres'
password = 'chatbot'
database_schema = 'postgres'
mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"
directory_path = "C:/Users/Khushbu/dev/LLMDetectText/data"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# def parsing_pdf_to_vector():


documents = SimpleDirectoryReader(directory_path).load_data()


connection_string = "postgresql://postgres:root@localhost:5432"
db_name = "postgres"
conn = psycopg2.connect(connection_string)
conn.autocommit = True
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector");



url = make_url(connection_string)
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    table_name="doc_vector",
    embed_dim=1536,  # openai embedding dimension
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
