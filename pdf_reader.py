from typing import List
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI

class LLMDocProccessor:
    def __init__(self, pdf: List[str]) -> None:
        self.knowledge_base = None
        self.pdf = pdf

        self.run()

    def reader(self):
        with open(self.pdf[0], "rb") as pdf:
            pdf_reader = PdfReader(pdf)
            text = ""
            # recorrer las paginas del pdf
            for page in pdf_reader.pages:
                text += page.extract_text()

            # split into chunks
            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=20,
                length_function=len
            )
            chunks = text_splitter.split_text(text)
            print(chunks, len(chunks))
            return chunks

    def create_embeddings(self, chunks):
        embeddings = OpenAIEmbeddings()
        """
        utilizamos FAISS para buscar la similaridad entre los
        embeddings y nuestros chunks y asi generar la base
        de conocimientos
        """
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        # knowledge_base.save_local("faiss_index")
        self.knowledge_base = knowledge_base

    def generate_answer(self, question):
        """
        aqui completamos el diagrama, tomando la prengunta
        del usuario y realizando la búsqueda semantica en
        la base de conocimiento
        """
        docs = self.knowledge_base.similarity_search(question)
        # llm = OpenAI()

        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

        """
        Y luego utilizamos el LLM para generar la respuesta
        que le vamos a presentar al usuario, basados en los
        docs previamente encontrados
        """
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=question, )
            print(cb)
            print(response)
        return response

    def run(self):
        # TODO preload embeddings
        # TODO preload faiss:  with open("faiss_index", "rb")
        chunks = self.reader()
        self.create_embeddings(chunks)
