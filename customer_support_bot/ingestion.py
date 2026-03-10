from pathlib import Path
import time
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import DistanceStrategy
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyMuPDFLoader

load_dotenv(override=True)
time.sleep(1)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=150,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

documents = []
for file in Path(DATA_DIR).glob("*.pdf"):
    loader = PyMuPDFLoader(str(file))
    documents.extend(loader.load_and_split(text_splitter))
print(len(documents))
print("these are the documents",documents)
for i, doc in enumerate(documents[:2]):
    print(f"\n--- Chunk {i} ---")
    print(doc.page_content[:300])

# create embeddings for all the chunks and store them in vector database
embeddings_model = HuggingFaceEmbeddings(
    model_name=os.getenv("HF_EMBEDDINGS_MODEL"),
    model_kwargs={"token": os.getenv("HUGGING_FACE_TOKEN")},
     encode_kwargs={
        "normalize_embeddings": True,
        # "show_progress_bar": True
    }
)

# create FAISS vector DB
vector_db = FAISS.from_documents(
    documents=documents,
    embedding=embeddings_model,
    distance_strategy=DistanceStrategy.COSINE,
)
VECTOR_DB_DIR = BASE_DIR / "data" / "semantic-search" / "index" / "faiss"
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
# save vector DB to local directory
vector_db.save_local(folder_path=VECTOR_DB_DIR)