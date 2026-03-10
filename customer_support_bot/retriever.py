from langchain_huggingface import HuggingFaceEmbeddings
import os
import re 
import time
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from sentence_transformers import CrossEncoder

load_dotenv(override=True)
time.sleep(1)


def clean_text(text: str):
    
    # remove emails
    text = re.sub(r'\S+@\S+', '', text)

    # remove phone numbers
    text = re.sub(r'\+\d[\d\s]+', '', text)

    # remove copyright
    text = re.sub(r'©.*', '', text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def clean_pdf_text(text: str):

    # remove emails
    text = re.sub(r'\S+@\S+', '', text)

    # remove phone numbers
    text = re.sub(r'\+\d[\d\s]+', '', text)

    # remove copyright
    text = re.sub(r'©.*', '', text)

    # remove common navigation words
    noise_words = [
        "Follow Us",
        "Careers",
        "Blog",
        "Terms",
        "Privacy Policy",
        "Applications & Services",
        "Our Products",
        "Industries",
        "Resources",
        "Case Studies"
    ]

    for word in noise_words:
        text = text.replace(word, "")

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# function to clean noisy PDF text
def clean_text(text: str):

    text = re.sub(r'\S+@\S+', '', text)  # remove emails
    text = re.sub(r'\+\d[\d\s]+', '', text)  # remove phone numbers
    text = re.sub(r'©.*', '', text)  # remove copyright
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces

    return text.strip()
def compress_context(docs, query):
    
    keywords = query.lower().split()
    
    relevant_lines = []
    
    for doc in docs:
        lines = doc.page_content.split("\n")
        
        for line in lines:
            if any(word in line.lower() for word in keywords):
                relevant_lines.append(line.strip())
    
    return "\n".join(relevant_lines)

# function to build context from vector DB
def build_context(vector_db: FAISS, query: str, top_k: int):

    # Step 1: Retrieve more docs than needed
    base_retriever = vector_db.as_retriever(search_kwargs={"k": 5})
    hits = base_retriever.invoke(query)

    print("Initial retrieved docs:", len(hits))

    # Step 2: Prepare query-doc pairs for reranking
    pairs = [[query, hit.page_content] for hit in hits]

    # Step 3: Get relevance scores
    scores = reranker.predict(pairs)

    # Step 4: Combine scores with docs
    scored_docs = list(zip(hits, scores))

    # Step 5: Sort by score
    ranked_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)

    # Step 6: Select top_k best documents
    top_docs = [doc for doc, score in ranked_docs[:top_k]]

    # print("Top docs after reranking:", top_docs)

    # 🔵 Step 7: CLEAN TEXT HERE
    cleaned_chunks = [clean_pdf_text(doc.page_content) for doc in top_docs]

    # Step 8: Build context
    res = compress_context(top_docs, query)

    return f"""
Use ONLY the information inside the context to answer the question.

<context>
{res}
</context>

Question:
{query}
"""

# loading the vector DB
BASE_DIR = Path(__file__).resolve().parent

vector_db_dir = BASE_DIR / "data" / "semantic-search" / "index" /"faiss"
print(f"Loading vector DB from {vector_db_dir}")
# initialize embeddings model
embeddings_model = HuggingFaceEmbeddings(
    model_name = os.getenv("HF_EMBEDDINGS_MODEL"),
    encode_kwargs = {"normalize_embeddings": True},
    model_kwargs = {"token": os.getenv("HUGGING_FACE_TOKEN")},
)

print("Embeddings model initialized successfully.embeddings_model:", embeddings_model)
# load vector DB from local directory
vector_db = FAISS.load_local(
    folder_path = vector_db_dir,
    embeddings = embeddings_model,
    allow_dangerous_deserialization = True,
)
print("Vector DB loaded successfully.vector_db:", vector_db)


reranker = CrossEncoder("BAAI/bge-reranker-base")


def rerank(query, docs, top_n=4):
    
    pairs = [[query, doc.page_content] for doc in docs]
    
    scores = reranker.predict(pairs)
    
    scored_docs = list(zip(docs, scores))
    
    ranked_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)
    
    return [doc for doc, score in ranked_docs[:top_n]]