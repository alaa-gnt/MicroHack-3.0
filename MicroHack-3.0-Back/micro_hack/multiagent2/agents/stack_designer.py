from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from state import Tier2State

class StackDesignerAgent:
    def __init__(self):
        self.llm = ChatMistralAI(model="mistral-small-latest", temperature=0.1)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Suggest a tech stack. If retrying, simplify for an MVP.
             Format: SCORE: [0.0-1.0] | STACK: [comma-separated list]"""),
            ("human", "Project: {text}\nAssessment: {assessment}\nPrevious Thoughts: {thoughts}")
        ])
        self.chain = self.prompt | self.llm

    def process(self, state: Tier2State):
        response = self.chain.invoke({
            "text": state["corrected_text"],
            "assessment": state.get("technical_assessment", ""),
            "thoughts": state.get("agent_thoughts", [])[-1:]
        })
        content = response.content
        try:
            score = float(content.split("SCORE:")[1].split("|")[0].strip())
            stack_str = content.split("STACK:")[1].strip()
            tech_list = [t.strip() for t in stack_str.split(",")]
        except:
            score, tech_list = 0.5, ["Check logs"]

        return {
            "tech_stack": tech_list,
            "confidences": {"stack": score},
            "retry_counts": {"stack": state.get("retry_counts", {}).get("stack", 0) + 1},
            "agent_thoughts": [f"Stack design score: {score}"]
        }

def tech_stack_node(state: Tier2State) -> Tier2State:
    agent = StackDesignerAgent()
    return {**state, **agent.process(state)}