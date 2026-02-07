import os
import json
import re
from typing import Dict
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from state import GraphState

class ImpactScoringAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.llm = ChatMistralAI(model="mistral-large-latest", temperature=0.3, api_key=self.api_key)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an impact assessment expert. Evaluate the potential IMPACT (0.0 to 1.0).
{retry_instruction}
Respond ONLY with a JSON object: {{"impact": float, "confidence": float, "reasoning": "string"}}"""),
            ("human", "Signal: {text}\nDomain: {domain}")
        ])

    def _extract_json(self, text: str) -> Dict:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(match.group()) if match else json.loads(text)

    def process(self, state: GraphState) -> Dict:
        retries = state.get("retry_count", 0)
        retry_instruction = ""
        if retries > 0:
            retry_instruction = "THOUGHT: Previous assessment had low confidence. Be more analytical about global scale and disruption."

        try:
            response = (self.prompt | self.llm).invoke({
                "retry_instruction": retry_instruction,
                "text": state.get("corrected_text") or state.get("signal_text", ""),
                "domain": state.get("domain", "Other")
            })
            result = self._extract_json(response.content)
            conf = float(result.get("confidence", 0.0))
            
            return {
                "impact": float(result.get("impact", 0.5)),
                "impact_confidence": conf,
                "retry_count": 1 if conf < 0.8 else 0 # Signal retry if low confidence
            }
        except Exception:
            return {"impact_confidence": 0.0, "retry_count": 1}

def impact_scoring_node(state: GraphState) -> GraphState:
    agent = ImpactScoringAgent()
    result = agent.process(state)
    return {**state, **result}