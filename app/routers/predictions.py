from fastapi import APIRouter, HTTPException
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from pydantic import BaseModel

from app import constants
from app.config import settings

router = APIRouter()

persist_directory = settings.chroma_vectorstore_dir
embedding = OpenAIEmbeddings()

# Now we can load the persisted database from disk, and use it as normal.
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

qa = RetrievalQA.from_llm(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens=2000),
    retriever=vectordb.as_retriever(),
    return_source_documents=True,
)


class PredictionRequest(BaseModel):
    question: str = ""


@router.post("/prediction", responses={400: {"description": "Invalid request"}})
async def prediction(data: PredictionRequest):
    question: str = data.question

    if not question:
        raise HTTPException(status_code=400, detail=f"Empty question")

    # question = "Co víš o předškolním vzdělání a jeho legislativě?"
    # question = "Popiš druhy kariérních systémů."
    # question = "Když vydělávám 100 000 Kč hrubého měsíčně jakožto programátor, vyplatí se víc osvč nebo hpp nebo sro?"
    # question = "Je protiprávní postavit plot bez upozornění souseda, který ale na chalupě nebydlí? Jaká může být pokuta?"
    # question = "Do kdy můžu odstoupit od smlouvy bez udání důvodu?"
    query = f"Užitečně a podrobně (zajímají mě především konkrétní paragrafy) odpověz v českém jazyce maximálně 500 slovy na otázku: '{question}'"
    result = qa({"query": query})

    return result
