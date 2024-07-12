from get_embedding_function import get_embedding_function
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.vectorstores.chroma import Chroma

CHROMA_PATH = "chroma"

def get_response(user_query, chat_history):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(user_query, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    template = """
    "You are an assistant for MCQ generation from given context and the question user provides.
    Use the following pieces of retrieved context to generate the questions. 
    the questions should be like USMLE questions, and should test medical students based the context given" \n\n
    "the format of questions is: \n
    [question tilte] \n\n
    a) option a \n\n
    b) option b \n\n
    c) option c \n\n
    d) option d \n\n
    answer: c \n
    reason for this answer: [reason for this answer]"

    "the question of user is: {question}"\n
    "generate five questions with this format and below given context.tell each option in a new line"
    "\n\n"
    "{context}"
    """

    prompt = ChatPromptTemplate.from_template(template)

    #llm = ChatOpenAI()
    llm = ChatGroq(model="llama3-70b-8192")
        
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "history": chat_history,
        "context": context_text,
        "question": user_query,
    })