try:
    import langchain
    import langchain_community
    import langchain_openai
    import langchain_pinecone
    import fastapi
    print("✅ SUCCESS: All libraries are installed correctly!")
except ImportError as e:
    print(f"❌ ERROR: Missing library -> {e}")