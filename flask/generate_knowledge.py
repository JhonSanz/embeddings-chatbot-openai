from typing import List
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv


class LLMDocProccessor:
    def __init__(self, pdf: List[str]) -> None:
        self.vectorstore = None
        self.pdf = pdf
        self.run()

    def reader(self):
        with open(self.pdf[0], "rb") as pdf:
            pdf_reader = PdfReader(pdf)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            text_splitter = CharacterTextSplitter(
                separator="\n", chunk_size=500, chunk_overlap=20, length_function=len
            )
            chunks = text_splitter.split_text(text)
            print(len(chunks))
            return chunks

    def create_embeddings(self, chunks):
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_texts(chunks, embeddings)
        vectorstore.save_local(f"{self.pdf[0].split('.')[0]}_faiss_index")
        self.vectorstore = vectorstore

    def run(self):
        load_dotenv()
        chunks = self.reader()
        self.create_embeddings(chunks)


LLMDocProccessor(["renacuajo_paseador.pdf"])