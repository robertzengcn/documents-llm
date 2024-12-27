#from langchain.chains.combine_documents.stuff import StuffDocumentsChain
#from langchain.chains.llm import LLMChain
from langchain_core.documents.base import Document
#from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from .invoice import InvoiceJson
# from .system_message import json_structure,system_message
from langchain_core.prompts import ChatPromptTemplate
#from langchain_chroma import Chroma
#from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import ChatOllama
# from .tool import get_embeddings
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from .productDict import ProductListJson
# import chromadb
# import json

# from langchain_core.output_parsers import JsonOutputParser


def extract_document(
    docs: list[Document],
    model_name: str,
    openai_api_key: str,
    base_url: str,
    temperature: float = 0.1,
) -> str:
    pass

    # parser = JsonOutputParser(pydantic_object=Order)
    # # Define LLM chain
    # chromadb.api.client.SharedSystemClient.clear_system_cache()
    llm  = ChatOllama(
        temperature=temperature,
        model=model_name,
        base_url="http://host.docker.internal:11434",
        api_key=openai_api_key,
    )
    
    # llm =ChatOllama(
    #     temperature=temperature,
    #     model=model_name,
    #     base_url=base_url,
    #     )
    embeddings = OllamaEmbeddings(
    model=model_name,
    base_url="http://host.docker.internal:11434",
    )
    print(model_name)
    
    #split pdf doc to vector
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(54)
    # default_ef = embedding_functions.DefaultEmbeddingFunction()
    vectorstore = FAISS.from_documents(splits,embeddings)
    retriever = vectorstore.as_retriever()
    print(55)
    
    system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, just say 'I don't know'. Only include information that is part of the document. Do not include your own opinion"
    "Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
    )
    print(76)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    print(79)
    billtoemailanswer = rag_chain.invoke({"input": "What is email address of billing to? please return email address only"})
    print(82)
    print(billtoemailanswer["answer"])
    billtoresp = rag_chain.invoke({"input": "What is the name of billing to in the document? only return name in your answer, not include address"})
    print(billtoresp["answer"])
    billtoaddresp = rag_chain.invoke({"input": "What is the billing to address? It is usually located before the state information, only return the address"})
    print(billtoaddresp["answer"])
    cityresp = rag_chain.invoke({"input": "What is city in the billing to information? only return city in your answer"})
    print(cityresp["answer"])
    billtostateresp = rag_chain.invoke({"input": "What is State number in the billing to address? only return state number in your answer"})
    print(billtostateresp["answer"])
    productresp = rag_chain.invoke({"input": "What are product information in the document? return product list information if you find multiple products"})
    print(productresp["answer"])
    paymentmethod = rag_chain.invoke({"input": "What is payment method in the document? only return payment method name in your answer"})
    print(paymentmethod["answer"])
    currencyres = rag_chain.invoke({"input": "What is currency in the document? only return currency short name like USD in your answer"})
    print(currencyres["answer"])
    # paymentterm = rag_chain.invoke({"input": "What is payment terms in the document?  only return the payment terms"})
    # print(paymentterm["answer"])
    print(102)
    
    # ask product info
    # projsonchain=llm.with_structured_output(ProductListJson)
    
    # json_system_prompt = (
    # "You are an assistant for question-answering tasks. "
    # "Use the following pieces of retrieved context to answer "
    # "the question.  Only include information that is part of the document. Do not include your own opinion"
    # "Use three sentences maximum and keep the "
    # "answer concise."
    # "\n\n"
    # "{context}"
    # )
    # jsonprompt = ChatPromptTemplate.from_messages(
    # [
    #     ("system", json_system_prompt),
    #     ("human", "{input}"),
    # ]
    # )
    # product_question_answer_chain = create_stuff_documents_chain(projsonchain, jsonprompt)
    # prorag_chain = create_retrieval_chain(retriever, product_question_answer_chain)
    
    # productresp=prorag_chain.invoke({"input": "What is product information in the document? Only include information that is part of the document. Do not include your own opinion or analysis"})
    # print(productresp)
    billing_info = {
        "email": billtoemailanswer["answer"],
        "name": billtoresp["answer"],
        "address": billtoaddresp["answer"],
        "city": cityresp["answer"],
        "state": billtostateresp["answer"],
        "product": productresp["answer"],
        "payment_method": paymentmethod["answer"],
        "currency": currencyres["answer"],
       
    }
    return billing_info
