from typing import TypedDict, List, Optional, Annotated
import operator, os, dotenv
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models.base import init_chat_model

class AIModel:
    def __init__(self, is_simulation) -> None:
        self.is_simulation = is_simulation
        os.environ["GOOGLE_API_KEY"] = dotenv.get_key(".env","gemini_api")
        self.model = init_chat_model(
            model="gemini-2.5-flash-lite",
            model_provider="google_genai"
        )

    def invoke(self, prompt):
        if self.is_simulation:
            return "Simulation answer"
        response = self.model.invoke(prompt).content
        return response

class ContractInfo(TypedDict):
    title: str
    purpose: Optional[str]  # "employment" or "rental"
    parties: List[str]
    status: Optional[str]   # "Valid", "Unsigned", "Expired"

    text: str
    embeddings: Optional[str]

class AuxFileInfo(TypedDict):
    category: Optional[str]   # Bank statement, email, proof 
    relation_to_contract: Optional[str] # Supplimentary, evidence, rule against
    
    text: str
    embeddings: Optional[str]

# Define the state structure
class ContractAdvisoryState(TypedDict):
    """State for the contract advisory workflow"""
    # Core contract information
    contracts: List[ContractInfo]
    
    # Analysis results
    extracted_clauses: dict  # Key clauses organized by category {contract: [{chapter: sentence, ...}]}
    identified_issues: List[str]  # Red flags or concerns
    risk_assessment: dict  # Advantage and risk levels for different aspects
    
    # Information gathering
    missing_info: List[str]  # What additional info is needed
    supplementary_materials: List[AuxFileInfo]  # Additional docs/context

    
    # Advice generation
    advice_steps: List[str] # Progressive ai advice
    user_attitude_steps: List[str] # Accepted, reluctant, confused, useless
    final_advice: Optional[str]  # Comprehensive final advice based on each step
    
    # Flow control
    conversation_complete: bool
    iteration_count: int
    next_action: str  # "analyze", "ask_questions", "provide_advice", "end"


