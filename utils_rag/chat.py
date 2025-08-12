from utils_rag.extract import extractor
from utils_rag.secret import groq_key
from llama_index.core import Settings
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


Settings.llm = Groq(
    api_key=groq_key,
    model="openai/gpt-oss-20b",
    temperature=0.4,
    max_completion_tokens=8192,
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    cache_folder="./embed-model/",
    device="cpu",
    backend="onnx",
    model_kwargs={
        "provider": "CPUExecutionProvider",
    },
)

Settings.context_window = 16384


def process_data(files: list[bytes]):
    document_texts = [extractor(file.name, file.read()).strip() for file in files]

    documents = [Document(text=texts) for texts in document_texts]
    doc_nodes = SentenceSplitter(
        chunk_size=1024, chunk_overlap=100
    ).get_nodes_from_documents(documents)

    index = VectorStoreIndex(nodes=doc_nodes, use_async=True)

    return index


def chat_rag(query: str, index: VectorStoreIndex):
    engine = index.as_query_engine(similarity_top_k=5)
    response = engine.query(query)

    return response.response
    
