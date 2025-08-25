from typing import Dict, Any
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseRetriever
import config

class PersonalChatbotAgent:
    def __init__(self, vector_store_retriever: BaseRetriever):
        self.llm = ChatOpenAI(
            openai_api_key=config.OPENAI_API_KEY,
            model_name=config.OPENAI_MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        self.retriever = vector_store_retriever
        
        # Create the conversational chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
            verbose=True
        )
        
        # Customize the prompt to include personality
        self.chain.combine_docs_chain.llm_chain.prompt = PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template=f"""
{config.PERSONALITY_PROMPT}

Based on the following context from Anees's documents, answer the question as if you are Anees:

Context:
{{context}}

Chat History:
{{chat_history}}

Question: {{question}}

Answer as Anees would, using first person when appropriate and drawing from the specific information in the context. If the question can't be answered from the context, say so honestly but still try to be helpful.

Answer:"""
        )
    
    def ask(self, question: str) -> Dict[str, Any]:
        """Process a question and return the response with sources."""
        try:
            response = self.chain({"question": question})
            
            # Extract source information
            sources = []
            if 'source_documents' in response:
                for doc in response['source_documents']:
                    source_info = {
                        'filename': doc.metadata.get('filename', 'Unknown'),
                        'type': doc.metadata.get('type', 'Unknown'),
                        'content_preview': doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                    }
                    sources.append(source_info)
            
            return {
                'answer': response['answer'],
                'sources': sources,
                'success': True
            }
        
        except Exception as e:
            return {
                'answer': f"Sorry, I encountered an error while processing your question: {str(e)}",
                'sources': [],
                'success': False
            }
    
    def clear_memory(self):
        """Clear the conversation memory."""
        self.memory.clear()
    
    def get_conversation_history(self):
        """Get the current conversation history."""
        return self.memory.chat_memory.messages

# Predefined sample questions to help users get started
SAMPLE_QUESTIONS = [
    "What kind of engineer are you?",
    "What are your strongest skills?",
    "What projects are you most proud of?",
    "Tell me about your experience with Python",
    "What technologies do you work with?",
    "What's your educational background?",
    "What are your career goals?",
    "Can you describe a challenging project you worked on?",
    "What programming languages do you know?",
    "What's your approach to problem-solving?"
]
