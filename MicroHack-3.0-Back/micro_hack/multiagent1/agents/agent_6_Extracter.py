"""Agent 6: Information Extraction Agent"""
import os
import json
import re
from typing import Dict
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from state import GraphState


class ExtractorAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.llm = ChatMistralAI(
            model="mistral-large-latest",
            temperature=0.2,
            api_key=self.api_key
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an information extraction expert. Extract the following entities:
1. COMPANIES: Names of organizations or startups
2. TECHNOLOGIES: Specific tools, frameworks, or protocols
3. LOCATION: Primary geographic location

Respond with a JSON object:
{{"companies": ["Company1"], "technologies": ["Tech1"], "location": "City, Country", "confidence": 0.85}}

Return ONLY the JSON object, nothing else."""),
            ("human", "Extract from:\nTitle: {title}\nText: {text}")
        ])
        
        self.chain = self.prompt | self.llm

    def _extract_json(self, text: str) -> Dict:
        """Robustly extract JSON even with markdown formatting"""
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(text)
        except Exception:
            raise ValueError(f"Failed to parse extraction JSON")

    def process(self, state: GraphState) -> Dict:
        """Extract companies, technologies, and location"""
        try:
            text = state.get("corrected_text") or state.get("signal_text", "")
            if not text:
                return {"companies": [], "technologies": [], "location": "Not specified", "extraction_confidence": 0.0}
            
            response = self.chain.invoke({
                "text": text,
                "title": state.get("title", ""),
                "source": state.get("source", ""),
                "url": state.get("url", "")
            })
            
            # Use the robust regex parser
            result = self._extract_json(response.content.strip())
            
            # Clean and validate lists
            companies = result.get("companies", [])
            techs = result.get("technologies", [])
            
            return {
                "companies": companies if isinstance(companies, list) else [],
                "technologies": techs if isinstance(techs, list) else [],
                "location": result.get("location", "Not specified"),
                "extraction_confidence": float(result.get("confidence", 0.5))
            }
            
        except Exception as e:
            print(f"DEBUG Error in Agent 6: {str(e)}")
            return {
                "companies": [],
                "technologies": [],
                "location": "Not specified",
                "extraction_confidence": 0.0,
                "processing_errors": [f"ExtractorAgent error: {str(e)}"]
            }


def extractor_node(state: GraphState) -> GraphState:
    """Node function for LangGraph"""
    agent = ExtractorAgent()
    result = agent.process(state)
    # Final merge into the global state
    return {**state, **result}