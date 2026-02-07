from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from state import Tier2State

class MarketAnalystAgent:
    def __init__(self):
        self.llm = ChatMistralAI(model="mistral-medium-latest", temperature=0.4)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Analyze target audience and revenue. 
             Format: SCORE: [0.0-1.0] | ANALYSIS: [text]"""),
            ("human", "{text}")
        ])
        self.chain = self.prompt | self.llm

    def process(self, state: Tier2State):
        response = self.chain.invoke({"text": state["corrected_text"]})
        content = response.content
        try:
            score = float(content.split("SCORE:")[1].split("|")[0].strip())
            analysis = content.split("ANALYSIS:")[1].strip()
        except:
            score, analysis = 0.6, content

        return {
            "market_analysis": analysis,
            "confidences": {"market": score},
            "retry_counts": {"market": state.get("retry_counts", {}).get("market", 0) + 1},
            "agent_thoughts": [f"Market analysis score: {score}"]
        }

def market_analysis_node(state: Tier2State) -> Tier2State:
    agent = MarketAnalystAgent()
    return {**state, **agent.process(state)}