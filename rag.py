from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os


from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel



load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "NIPS-2017-attention-is-all-you-need-Paper.pdf")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "index.html")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
rag_chain = None
rag_error = None

class QueryRequest(BaseModel):
    question: str


template="""Answer the question based on the following context:
{context}
Question:{question}
Answer:"""
prompt=ChatPromptTemplate.from_template(template)

def format_docs(docs):
     return "\n\n".join(doc.page_content for doc in docs)

def build_rag_chain():
    print("loading pdf")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print("splitting text")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    print("creating embeddings")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("storing embeddings in chromadb")
    vectorstore = Chroma.from_documents(texts, embeddings)
    retriver = vectorstore.as_retriever(search_kwargs={"k": 3})

    print("initializing llm")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=512,
        api_key=api_key
    )

    return (
        {"context": retriver | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

def get_rag_chain():
    global rag_chain
    global rag_error

    if rag_chain is not None:
        return rag_chain

    try:
        rag_chain = build_rag_chain()
        rag_error = None
        return rag_chain
    except Exception as exc:
        rag_error = str(exc)
        raise HTTPException(
            status_code=500,
            detail=(
                "RAG initialization failed. Confirm internet access for the first Hugging Face "
                f"model download and verify GROQ_API_KEY is set. Original error: {exc}"
            ),
        ) from exc

def ask_question(query: str):
    chain = get_rag_chain()
    return chain.invoke(query)

@app.get("/", response_class=HTMLResponse)
def home():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

@app.get("/health")
def health():
    return {
        "status": "ok",
        "rag_ready": rag_chain is not None,
        "last_error": rag_error,
    }

@app.post("/ask")
def ask(req: QueryRequest):
    answer = ask_question(req.question)
    return {"answer": answer}


