import os
import json
import re
from typing import Dict
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from state import GraphState

class TriAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.llm = ChatMistralAI(model="mistral-large-latest", temperature=0.3, api_key=self.api_key)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Evaluate Technology Readiness (0-10). {thought}\nReturn ONLY JSON: {{\"tri\": float, \"confidence\": float}}"),
            ("human", "Text: {text}\nImpact: {impact}\nUrgency: {urgency}")
        ])

    def _extract_json(self, text: str) -> Dict:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(match.group()) if match else json.loads(text)

    def process(self, state: GraphState) -> Dict:
        retries = state.get("retry_count", 0)
        thought = "Analyze feasibility."
        if retries > 0:
            thought = "THOUGHT: My last score was uncertain. I need to weigh the impact vs urgency more strictly."

        try:
            response = (self.prompt | self.llm).invoke({
                "thought": thought,
                "text": state.get("corrected_text") or state.get("signal_text", ""),
                "impact": state.get("impact", 0.5),
                "urgency": state.get("urgency", 0.5)
            })
            result = self._extract_json(response.content)
            conf = float(result.get("confidence", 0.0))
            
            return {
                "tri": float(result.get("tri", 5.0)),
                "tri_confidence": conf,
                "retry_count": 1 if conf < 0.7 else 0
            }
        except:
            return {"tri_confidence": 0.0, "retry_count": 1}

def tri_node(state: GraphState) -> GraphState:
    agent = TriAgent()
    result = agent.process(state)
    return {**state, **result}