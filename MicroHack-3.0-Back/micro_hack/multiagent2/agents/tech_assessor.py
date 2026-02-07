from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from state import Tier2State

class TechnicalAssessorAgent:
    def __init__(self):
        self.llm = ChatMistralAI(model="mistral-large-latest", temperature=0.2)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Analyze the technical requirements. 
             If this is a RETRY, improve your previous analysis.
             You MUST return your response in this EXACT format:
             SCORE: [0.0-1.0] | ANALYSIS: [Your detailed technical breakdown]"""),
            ("human", "Text: {text}\nPrevious Thoughts: {thoughts}")
        ])
        self.chain = self.prompt | self.llm

    def process(self, state: Tier2State):
        response = self.chain.invoke({
            "text": state["corrected_text"],
            "thoughts": state.get("agent_thoughts", [])[-1:]
        })
        content = response.content
        # Robust parsing
        try:
            score_part = content.split("SCORE:")[1].split("|")[0].strip()
            score = float(score_part)
            analysis = content.split("ANALYSIS:")[1].strip()
        except Exception:
            score, analysis = 0.5, content # Fallback
            
        return {
            "technical_assessment": analysis,
            "confidences": {"tech": score},
            "retry_counts": {"tech": state.get("retry_counts", {}).get("tech", 0) + 1},
            "agent_thoughts": [f"Tech assessment score: {score}"]
        }

def tech_assessment_node(state: Tier2State) -> Tier2State:
    agent = TechnicalAssessorAgent()
    return {**state, **agent.process(state)}