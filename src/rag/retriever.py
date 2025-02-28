from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS

embed_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceBgeEmbeddings(model_name=embed_model_name)

retriever = FAISS.load_local(
    "./faiss_storage", embeddings, allow_dangerous_deserialization=True
)
