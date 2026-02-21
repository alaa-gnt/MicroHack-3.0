"""Test setup and environment verification"""
import os
import sys


def test_environment():
    """Test that the environment is properly set up"""
    
    print("Testing environment setup...")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    assert sys.version_info >= (3, 8), "Python 3.8 or higher required"
    
    # Check for API key
    api_key = os.getenv("MISTRAL_API_KEY")
    if api_key:
        print("✅ MISTRAL_API_KEY found in environment")
    else:
        print("⚠️  MISTRAL_API_KEY not found. Please set it before running agents.")
        print("   export MISTRAL_API_KEY='your-api-key-here'")
    
    # Check imports
    try:
        import langgraph
        print(f"✅ LangGraph installed")
    except ImportError:
        print("❌ LangGraph not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        import langchain
        version = getattr(langchain, '__version__', 'installed')
        print(f"✅ LangChain version: {version}")
    except ImportError:
        print("❌ LangChain not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        import langchain_core
        print(f"✅ LangChain Core available")
    except ImportError:
        print("❌ LangChain Core not installed. Run: pip install -r requirements.txt")
        return False
    
    try:
        from langchain_mistralai import ChatMistralAI
        from langchain_core.prompts import ChatPromptTemplate
        print("✅ LangChain MistralAI integration available")
    except ImportError as e:
        print(f"❌ LangChain MistralAI not installed: {e}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    try:
        import datasets
        print(f"✅ Datasets library available")
    except ImportError:
        print("❌ Datasets not installed. Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ Environment setup complete!")
    return True


if __name__ == "__main__":
    success = test_environment()
    sys.exit(0 if success else 1)