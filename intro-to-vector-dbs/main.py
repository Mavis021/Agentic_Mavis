import os 
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from langchain_core.runnables import RunnablePassthrough


load_dotenv()


def format_docs(docs):
    return "\n\n".join([docs.page_content for docs in docs])


if __name__ == '__main__':
    print("Retrieving ...")

    embeddings = OpenAIEmbeddings()
    llm= ChatOpenAI()

    query = "What are vectordatabases?"
    # chain = PromptTemplate.from_template(template=query) | llm

    vectorstore = PineconeVectorStore(

        index_name=os.environ['INDEX_NAME'],
        embedding=embeddings,
    )


    # Using LangChain Hub to pull a pre-defined prompt for retrieval-qa

    # retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    # combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    # retrieval_chain = create_retrieval_chain(
    #     retriever=vectorstore.as_retriever(),
    #     combine_docs_chain=combine_docs_chain
    # )

    # result = retrieval_chain.invoke(input={"input": query})

    # print(f"Result: {result}")



    template = """
       Use the following pieces of context to answer the question at the end. 
       If you don't know the answer, just say that you don't know, don't try to make up an answer.
       Use three sentences maximum and keep the answer as concise as possible.
       Always say "Thanks for the question!" at the beginning of your answer.

       {context}

       Question:{question}

       Helpful Answer:     
    """

    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"context": vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
    )

    restult = rag_chain.invoke(query)
    print(f"Result: {restult}")