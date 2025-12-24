import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
load_dotenv()

class ChatPDFSystem:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = PineconeVectorStore.from_existing_index(
            index_name=os.getenv("PINECONE_INDEX_NAME"),
            embedding=self.embeddings
        )
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        
        # Memory buffer for keeping conversation history
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # The Chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            memory=self.memory,
            return_source_documents=True
        )

    def ask(self, query):
        result = self.qa_chain.invoke({"question": query})
        
        answer = result["answer"]
        source_docs = result["source_documents"]
        
        # Extract Citations
        citations = []
        for doc in source_docs:
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', 'Unknown')
            citations.append(f"{os.path.basename(source)} (Page {page})")
        
        return {
            "answer": answer,
            "citations": list(set(citations))
        }