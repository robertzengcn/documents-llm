from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.documents.base import Document
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from .invoice import InvoiceJson
# from .system_message import json_structure,system_message
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.llms import Ollama
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
    # llm  = ChatOpenAI(
    #     temperature=temperature,
    #     model_name=model_name,
    #     api_key=openai_api_key,
    #     base_url=base_url,
    # )
    llm =Ollama(model="mistral")
    
    #split pdf doc to vector
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    
    # structured_llm = llm.with_structured_output(InvoiceJson, method="json_mode")
    # system_prompt = system_message.format(json_structure=json_structure)

    # prompt_template = """Extra information from following document.
    # Only include information that is part of the document. 
    # Do not include your own opinion or analysis.\n{format_instructions}\n
    
    # Document:
    # "{document}"
    # """
    # prompt = PromptTemplate.from_template(prompt_template,
    #                                        partial_variables={"format_instructions": parser.get_format_instructions()},                                    
    #                                       )
    # few_shot_structured_llm = prompt
    # print(few_shot_structured_llm)
    # llm_chain = LLMChain(llm=llm, prompt=few_shot_structured_llm)

    # stuff_chain = StuffDocumentsChain(
    #     llm_chain=llm_chain, document_variable_name="document"
    # )
    # structured_llm = llm.with_structured_output(InvoiceJson, method="json_mode")
    # system_prompt = system_message.format(json_structure=json_structure)
    # prompt = ChatPromptTemplate.from_messages(
    #     [("system", system_prompt), ("human", "{input}")]
    # )
    # print(docs[0].page_content)
    
    # few_shot_structured_llm = prompt | structured_llm
   
    # few_shot_structured_llm = prompt | structured_llm
    # input_prompt = f"raw_texts: {docs[0].page_content}"
    # print(few_shot_structured_llm)
    # result = few_shot_structured_llm.invoke({"input": input_prompt})
   
    # return
    # print(result)
    # result = stuff_chain.invoke(docs)
    # return result["output_text"]
    system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, just say '' "
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
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    billtoemail = rag_chain.invoke({"input": "What was email address of billing to?"})
    
    return billtoemail
