"""Agent 1: Text Improvement Agent"""
import os
from typing import Dict
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from state import GraphState


class TextImproveAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.llm = ChatMistralAI(
            model="mistral-large-latest",
            temperature=0.3,
            api_key=self.api_key
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a text improvement expert. Your task is to:
1. Fix grammar and spelling errors
2. Improve clarity and readability
3. Maintain the original meaning and technical terms
4. Keep the text concise and professional

Return ONLY the corrected text, nothing else."""),
            ("human", "{text}")
        ])
        
        self.chain = self.prompt | self.llm
    
    def process(self, state: GraphState) -> Dict:
        """Process the state and improve the signal text"""
        try:
            signal_text = state.get("signal_text", "")
            
            if not signal_text or len(signal_text.strip()) == 0:
                return {
                    "corrected_text": signal_text,
                    "processing_errors": ["Empty signal text provided"]
                }
            
            # Invoke the LLM
            response = self.chain.invoke({"text": signal_text})
            corrected_text = response.content.strip()
            
            return {
                "corrected_text": corrected_text,
                "signal_text": corrected_text  # Update the main text
            }
            
        except Exception as e:
            return {
                "corrected_text": state.get("signal_text", ""),
                "processing_errors": [f"TextImproveAgent error: {str(e)}"]
            }


def text_improve_node(state: GraphState) -> GraphState:
    """Node function for LangGraph"""
    agent = TextImproveAgent()
    result = agent.process(state)
    return {**state, **result}