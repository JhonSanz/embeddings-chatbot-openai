from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory


class LLMDocProccessor:
    def __init__(self) -> None:
        self.vectorstore = None
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        self.ready = False
        self.start()

    def get_conversation_chain(self):
        # message_history = DynamoDBChatMessageHistory(
        #     table_name="chatbot_memory_test", session_id="1"
        # )
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            # chat_memory=message_history,
            return_messages=True
        )
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm, retriever=self.vectorstore.as_retriever(), memory=memory
        )
        return conversation_chain

    def load_knowledge(self) -> bool:
        try:
            embeddings = OpenAIEmbeddings()
            # SHOULD I LOAD IT FROM S3? ;)
            vectorstore = FAISS.load_local("faiss_index", embeddings)
            self.vectorstore = vectorstore
            return True
        except:
            return False

    def start(self) -> bool:
        self.ready = self.load_knowledge()
