from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from state import Tier2State

class FeasibilityExpertAgent:
    def __init__(self):
        self.llm = ChatMistralAI(model="mistral-large-latest", temperature=0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Review the Tech and Market data. Provide a final feasibility score (0.0 to 1.0). Return ONLY the number."),
            ("human", "Tech: {tech}\nMarket: {market}")
        ])
        self.chain = self.prompt | self.llm

    def process(self, state: Tier2State):
        response = self.chain.invoke({
            "tech": state["technical_assessment"],
            "market": state["market_analysis"]
        })
        try:
            score = float(response.content.strip())
        except:
            score = 0.5
        return {
            "feasibility_score": score,
            "retry_counts": {"feasibility": state.get("retry_counts", {}).get("feasibility", 0) + 1}
        }

def feasibility_node(state: Tier2State) -> Tier2State:
    agent = FeasibilityExpertAgent()
    return {**state, **agent.process(state)}