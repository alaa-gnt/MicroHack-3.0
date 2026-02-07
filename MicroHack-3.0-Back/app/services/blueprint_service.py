import os
import json
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

from app.models.opportunity import Opportunity
from app.models.feasibility import FeasibilityStudy
from app.models.blueprint import VentureBlueprint
from app.schemas.blueprint import VentureBlueprintCreate

class BlueprintService:
    def __init__(self, db: Session):
        self.db = db
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.llm = ChatMistralAI(
            model="mistral-large-latest",
            temperature=0.2,
            api_key=self.api_key
        )

    def get_blueprint(self, opportunity_id: str) -> Optional[VentureBlueprint]:
        return self.db.query(VentureBlueprint).filter(VentureBlueprint.opportunity_id == opportunity_id).first()

    def generate_blueprint(self, opportunity_id: str) -> VentureBlueprint:
        # 1. Fetch data
        opp = self.db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
        feas = self.db.query(FeasibilityStudy).filter(FeasibilityStudy.opportunity_id == opportunity_id).first()
        
        if not opp:
            raise ValueError("Opportunity not found")
        
        # 2. Check if already exists
        blueprint = self.get_blueprint(opportunity_id)
        if blueprint:
            return blueprint

        # 3. Prepare Prompt for Generation
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Senior Venture Architect. your task is to generate a comprehensive "Autonomous Venture Blueprint" for a given innovation opportunity.
            
            Return your response in EXACTLY this JSON format:
            {{
                "system_architecture": "string (Optimized tech stack and high-level architecture)",
                "data_schema": "string (SQL/NoSQL models and data structures)",
                "security_protocols": "string (ISO-compliant security and maritime data protocols)",
                "kpi_metrics": "string (Key metrics to track project impact)",
                "v0_prompt": "string (A detailed prompt for v0.dev or Claude Artifacts to generate the UI)",
                "github_manifest": {{
                    "package_json": "string",
                    "readme_md": "string",
                    "env_example": "string"
                }},
                "mermaid_flow": "string (A detailed Mermaid.js graph TD script. Use subgraphs for Frontend, Backend, Database, and External Services. Use cylinders for databases, diamonds for decision points. Add 'classDef' styles for different node types to make it look professional and colorful.)"
            }}
            """),
            ("human", """Opportunity: {title}
            Domain: {domain}
            Corrected Text: {text}
            Expert Assessment: {assessment}
            Required Stack: {stack}
            """)
        ])

        chain = prompt | self.llm
        
        response = chain.invoke({
            "title": opp.signal.title if opp.signal else "Innovation Project",
            "domain": opp.primary_domain,
            "text": opp.corrected_text or (opp.signal.full_content if opp.signal else ""),
            "assessment": feas.technical_assessment if feas else "General innovation",
            "stack": feas.required_technology_stack if feas else "Standard web stack"
        })

        try:
            # Clean response if LLM added backticks
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            data = json.loads(content)
            
            blueprint = VentureBlueprint(
                opportunity_id=opportunity_id,
                system_architecture=data.get("system_architecture"),
                data_schema=data.get("data_schema"),
                security_protocols=data.get("security_protocols"),
                kpi_metrics=data.get("kpi_metrics"),
                v0_prompt=data.get("v0_prompt"),
                github_manifest=data.get("github_manifest"),
                mermaid_flow=data.get("mermaid_flow")
            )
            
            self.db.add(blueprint)
            self.db.commit()
            self.db.refresh(blueprint)
            return blueprint
            
        except Exception as e:
            print(f"❌ Blueprint Generation Error: {e}")
            raise RuntimeError(f"Failed to generate blueprint: {str(e)}")
