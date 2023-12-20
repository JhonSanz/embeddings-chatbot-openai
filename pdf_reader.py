from typing import List
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory


class LLMDocProccessor:
    def __init__(self, pdf: List[str]) -> None:
        self.vectorstore = None
        self.pdf = pdf
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
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
                separator="\n", chunk_size=1000, chunk_overlap=20, length_function=len
            )
            chunks = text_splitter.split_text(text)
            return chunks

    def create_embeddings(self, chunks):
        """
        Los embeddings de openAI tienen costo, pero son muy baratos.
        El proceso de embedding requiere cómputo y en este
        paso openAI lo hace por nosotros.

        Existen alternativas gratuitas e incluso de mejor performance,
        pero estas deben correrse localmente con recursos
        informáticos como GPU (los cuales no tengo ahora xd)

        https://huggingface.co/spaces/mteb/leaderboard
        """
        embeddings = OpenAIEmbeddings()
        """
        utilizamos FAISS para buscar la similaridad entre los
        embeddings y nuestros chunks y asi generar la base
        de conocimientos.

        En este paso existen alternativas cloud para guardar
        la base de conocimientos similar a una base de datos.
        Tales como Pinecone, Chroma etc.
        """
        vectorstore = FAISS.from_texts(chunks, embeddings)
        # UPLOAD TO S3
        vectorstore.save_local("faiss_index")
        self.vectorstore = vectorstore

    def get_conversation_chain(self):
        message_history = DynamoDBChatMessageHistory(
            table_name="chatbot_memory_test", session_id="1"
        )
        memory = ConversationBufferMemory(
            memory_key="chat_history", chat_memory=message_history, return_messages=True
        )
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm, retriever=self.vectorstore.as_retriever(), memory=memory
        )
        return conversation_chain

    def generate_answer(self, question):
        """
        LAMBDA FUNCTION

        aqui completamos el diagrama, tomando la prengunta
        del usuario y realizando la búsqueda semantica en
        la base de conocimiento
        """
        docs = self.vectorstore.similarity_search(question)

        """
        Y luego utilizamos el LLM para generar la respuesta
        que le vamos a presentar al usuario, basados en los
        docs previamente encontrados
        """
        chain = load_qa_chain(self.llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(
                input_documents=docs,
                question=question,
            )
            print(cb)
            print(response)
        return response

    def load_knowledge(self):
        try:
            embeddings = OpenAIEmbeddings()
            # LOAD FROM S3
            vectorstore = FAISS.load_local("faiss_index", embeddings)
            self.vectorstore = vectorstore
            return True
        except:
            return False

    def run(self):
        loaded_embeddings = self.load_knowledge()
        if not loaded_embeddings:
            chunks = self.reader()
            self.create_embeddings(chunks)
