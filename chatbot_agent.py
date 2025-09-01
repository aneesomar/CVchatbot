from typing import Dict, Any, Optional
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Patch ChromaDB telemetry before importing config
try:
    import sys
    from unittest.mock import MagicMock
    sys.modules['posthog'] = MagicMock()
except:
    pass

import config
import requests

class PersonalChatbotAgent:
    def __init__(self, vector_store_retriever: Optional[Any] = None, personality_mode: str = None):
        # Use OpenAI ChatGPT
        if not config.OPENAI_API_KEY:
            # Try to get from Streamlit secrets as fallback
            try:
                import streamlit as st
                api_key = st.secrets.get("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY in environment variables or Streamlit secrets.")
            except ImportError:
                raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY environment variable.")
        else:
            api_key = config.OPENAI_API_KEY
        
        self.llm = ChatOpenAI(
            model_name=config.OPENAI_MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            openai_api_key=api_key
        )
        
        # Set personality mode
        self.personality_mode = personality_mode or config.DEFAULT_PERSONALITY_MODE
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        self.retriever = vector_store_retriever
        
        # Create the conversational chain if we have a retriever
        self.chain = self._create_chain()
    
    def is_openai_available(self) -> bool:
        """Check if OpenAI API is accessible"""
        try:
            # Simple test call to check API availability
            test_llm = ChatOpenAI(
                model_name=config.OPENAI_MODEL,
                openai_api_key=config.OPENAI_API_KEY,
                max_tokens=1
            )
            test_llm.invoke("test")
            return True
        except Exception as e:
            print(f"OpenAI API not available: {e}")
            return False
    
    def _create_chain(self):
        """Create or recreate the conversational chain with current personality mode"""
        if not self.retriever:
            return None
            
        personality_prompt = config.PERSONALITY_MODES[self.personality_mode]["prompt"]
        
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={
                "prompt": PromptTemplate(
                    input_variables=["context", "question"],
                    template=f"""{personality_prompt}

Context from Anees's documents:
{{context}}

Question: {{question}}

Instructions: Use the context above to answer as Anees Omar in {config.PERSONALITY_MODES[self.personality_mode]["name"]}. If the context contains relevant information, provide a complete answer using that information and do not add any disclaimers. Only if the context is empty or completely irrelevant should you mention not having the information.

Answer:"""
                )
            }
        )
    
    def set_personality_mode(self, mode: str):
        """Change the personality mode and recreate the chain"""
        if mode in config.PERSONALITY_MODES:
            self.personality_mode = mode
            self.chain = self._create_chain()
            return True
        return False
    
    def update_retriever(self, vector_store_retriever: Optional[Any]):
        """Update the retriever and recreate the chain"""
        self.retriever = vector_store_retriever
        self.chain = self._create_chain()
    
    def get_current_mode(self) -> Dict[str, str]:
        """Get information about the current personality mode"""
        if self.personality_mode in config.PERSONALITY_MODES:
            mode_info = config.PERSONALITY_MODES[self.personality_mode]
            return {
                "mode": self.personality_mode,
                "name": mode_info["name"],
                "description": mode_info["description"]
            }
        return None
    
    def ask(self, question: str) -> Dict[str, Any]:
        """Ask a question and get a response"""
        if not self.chain:
            # Fallback to direct chat without documents
            try:
                answer = self.chat_direct(question)
                return {
                    "answer": answer,
                    "source_documents": []
                }
            except Exception as e:
                return {
                    "answer": f"I encountered an error: {str(e)}",
                    "source_documents": []
                }
        
        try:
            response = self.chain({"question": question})
            return {
                "answer": response.get("answer", "I couldn't generate a response."),
                "source_documents": response.get("source_documents", [])
            }
        except Exception as e:
            return {
                "answer": f"I encountered an error: {str(e)}",
                "source_documents": []
            }
    
    def chat_direct(self, message: str) -> str:
        """Direct chat without document context (useful when no documents are loaded)"""
        try:
            personality_prompt = config.PERSONALITY_MODES[self.personality_mode]["prompt"]
            prompt = f"{personality_prompt}\n\nUser: {message}\n\nAssistant:"
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
