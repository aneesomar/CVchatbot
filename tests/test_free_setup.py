#!/usr/bin/env python3
"""Test the free chatbot setup"""

def test_ollama():
    print("Testing Ollama connection...")
    try:
        import ollama
        response = ollama.chat(
            model='llama3.2:1b',
            messages=[{'role': 'user', 'content': 'Hello, can you introduce yourself?'}],
            stream=False
        )
        print("✅ Ollama is working!")
        print(f"Response: {response['message']['content']}")
        return True
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        return False

def test_free_embeddings():
    print("\nTesting free local embeddings...")
    try:
        from document_processor import LocalEmbeddings
        embeddings = LocalEmbeddings()
        
        # Test embedding some text
        texts = ["Hello world", "This is a test"]
        doc_embeddings = embeddings.embed_documents(texts)
        query_embedding = embeddings.embed_query("Hello")
        
        print("✅ Free embeddings working!")
        print(f"Document embeddings shape: {len(doc_embeddings)} x {len(doc_embeddings[0])}")
        print(f"Query embedding shape: {len(query_embedding)}")
        return True
    except Exception as e:
        print(f"❌ Free embeddings test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_free_chatbot_agent():
    print("\nTesting free chatbot agent...")
    try:
        from chatbot_agent import PersonalChatbotAgent
        
        agent = PersonalChatbotAgent()
        if agent.is_ollama_available():
            print("✅ Ollama is available for chatbot agent")
            
            # Test direct chat
            response = agent.chat_direct("Hello! Tell me about yourself.")
            print("✅ Direct chat working!")
            print(f"Response: {response[:100]}...")
            return True
        else:
            print("❌ Ollama not available")
            return False
            
    except Exception as e:
        print(f"❌ Free chatbot agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🆓 Testing Free Chatbot Setup\n")
    
    tests = [
        ("Ollama", test_ollama),
        ("Free Embeddings", test_free_embeddings),
        ("Free Chatbot Agent", test_free_chatbot_agent)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"{'='*50}")
        success = test_func()
        results.append((name, success))
        print()
    
    print("="*50)
    print("📊 FINAL RESULTS:")
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your free chatbot is ready to use!")
        print("Run: streamlit run app.py")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
