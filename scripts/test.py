from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI


def main():
    # Specify the persist_directory where the embeddings on disk is stored
    persist_directory = './data/chromadb'
    embedding = OpenAIEmbeddings()

    # Now we can load the persisted database from disk, and use it as normal.
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    qa = RetrievalQA.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens=1000),
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
    )

    # question = "Co víš o předškolním vzdělání a jeho legislativě?"
    # question = "Popiš druhy kariérních systémů."
    # question = "Když vydělávám 100 000 Kč hrubého měsíčně jakožto programátor, vyplatí se víc osvč nebo hpp nebo sro?"
    question = "Je protiprávní postavit plot bez upozornění souseda, který ale na chalupě nebydlí? Jaká může být pokuta?"
    query = f"Užitečně a podrobně (zajímají mě především konkrétní paragrafy) odpověz v českém jazyce maximálně 200 slovy na otázku: '{question}'"
    result = qa({"query": query})
    print(result)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
