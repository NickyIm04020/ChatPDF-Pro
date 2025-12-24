import sys
print(f"Python Executable: {sys.executable}")

try:
    import langchain
    print(f"✅ LangChain found: {langchain.__version__}")
    
    from langchain.chains import ConversationalRetrievalChain
    print("✅ ConversationalRetrievalChain found! You are ready.")
    
except ImportError as e:
    print(f"❌ ERROR: {e}")