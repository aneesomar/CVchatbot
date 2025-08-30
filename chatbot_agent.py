from typing import Dict, Any, Optional
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseRetriever
from langchain.llms.base import LLM

# Patch ChromaDB telemetry before importing config
try:
    import sys
    from unittest.mock import MagicMock
    sys.modules['posthog'] = MagicMock()
except:
    pass

import config
import ollama
import requests

class OllamaLLM(LLM):
    """Custom Ollama LLM wrapper for LangChain"""
    
    model_name: str = config.OLLAMA_MODEL
    base_url: str = config.OLLAMA_BASE_URL
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @property
    def _llm_type(self) -> str:
        return "ollama"
    
    def _call(self, prompt: str, stop: Optional[list] = None) -> str:
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}],
                stream=False
            )
            return response['message']['content']
        except Exception as e:
            return f"Error calling Ollama: {str(e)}"
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model_name": self.model_name, "base_url": self.base_url}

class PersonalChatbotAgent:
    def __init__(self, vector_store_retriever: Optional[BaseRetriever] = None, personality_mode: str = None):
        # Use free local Ollama model
        self.llm = OllamaLLM()
        
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
    
    def update_retriever(self, vector_store_retriever: Optional[BaseRetriever]):
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
            return self.llm._call(prompt)
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        
    def is_ollama_available(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            response = requests.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=5)
            models = response.json().get("models", [])
            return any(model.get("name") == config.OLLAMA_MODEL for model in models)
        except:
            return False
