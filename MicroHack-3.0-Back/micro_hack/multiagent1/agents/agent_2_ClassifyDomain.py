"""Agent 2: Domain Classification Agent (ReAct Version)"""
import os
import json
import re
from typing import Dict
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from state import GraphState


class ClassifyDomainAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment")
            
        self.llm = ChatMistralAI(
            model="mistral-large-latest",
            temperature=0.2,
            api_key=self.api_key
        )
        
        self.domains = [
            "IoT", "Blockchain", "AI/ML", "Cybersecurity", 
            "Cloud Computing", "5G/Networking", "Quantum Computing",
            "Biotechnology", "Clean Energy", "FinTech", "HealthTech",
            "EdTech", "AgriTech", "Space Technology", "Robotics",
            "AR/VR", "Other"
        ]
        
        # We keep your favorite prompt, but add a slot for {retry_instruction}
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a domain classification expert. Classify the given text into ONE of these domains:
{domains}

{retry_instruction}

Respond with a JSON object containing:
- "domain": the classified domain (exactly as listed above)
- "confidence": a float between 0 and 1 indicating your confidence

Example response:
{{"domain": "AI/ML", "confidence": 0.95}}

Return ONLY the JSON object, nothing else."""),
            ("human", "Text to classify:\n{text}\n\nKeywords: {keywords}")
        ])
    
    def _extract_json(self, text: str) -> Dict:
        """Robustly extract JSON from LLM response"""
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(text)
        except Exception:
            raise ValueError(f"Could not parse JSON from: {text}")

    def process(self, state: GraphState) -> Dict:
        """Classify the domain of the signal with ReAct logic"""
        try:
            text = state.get("corrected_text") or state.get("signal_text", "")
            keywords = state.get("keyword", [])
            retries = state.get("retry_count", 0)
            
            # ReAct Logic: If we are retrying, give a specific 'Thought' instruction
            retry_instruction = ""
            if retries > 0:
                retry_instruction = """
THOUGHT: My previous classification had low confidence. 
ACTION: I must re-examine the specific technical keywords and context to ensure the domain is correct.
"""

            if not text:
                return {"domain": "Other", "domain_confidence": 0.0}
            
            # Invoke the LLM
            chain = self.prompt | self.llm
            response = chain.invoke({
                "text": text,
                "keywords": ", ".join(keywords) if keywords else "None",
                "domains": ", ".join(self.domains),
                "retry_instruction": retry_instruction
            })
            
            result = self._extract_json(response.content.strip())
            
            domain = result.get("domain", "Other")
            conf = float(result.get("confidence", 0.0))
            
            if domain not in self.domains:
                domain = "Other"
            
            # CRITICAL REACT CHANGE: 
            # If confidence is < 0.8, we return retry_count=1. 
            # Because we used operator.add in state.py, this adds 1 to the current total.
            return {
                "domain": domain,
                "domain_confidence": conf,
                "retry_count": 1 if conf < 0.8 else 0
            }
            
        except Exception as e:
            print(f"\n[ERROR] Agent 2 Failure: {str(e)}")
            return {
                "domain": "Other",
                "domain_confidence": 0.0,
                "retry_count": 1 # Try again if it crashes
            }


def classify_domain_node(state: GraphState) -> GraphState:
    agent = ClassifyDomainAgent()
    result = agent.process(state)
    return {**state, **result}