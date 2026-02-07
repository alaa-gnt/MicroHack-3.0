from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from state import Tier2State


class StrategistAgent:
    def __init__(self):
        self.llm = ChatMistralAI(model="mistral-large-latest", temperature=0.5)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Provide a final executive recommendation and the immediate next step for this project."),
            ("human", "Project: {text}\nFeasibility Score: {score}")
        ])
        self.chain = self.prompt | self.llm

    def process(self, state: Tier2State):
        response = self.chain.invoke({
            "text": state["corrected_text"],
            "score": state["feasibility_score"]
        })
        return {"final_recommendation": response.content.strip()}

def final_recommendation_node(state: Tier2State) -> Tier2State:
    agent = StrategistAgent()
    return {**state, **agent.process(state)}