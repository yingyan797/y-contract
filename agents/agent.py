from typing import TypedDict, List, Optional, Annotated
import operator, os, dotenv
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models.base import init_chat_model

dotenv.load_dotenv()

class AIModel:
    def __init__(self, is_simulation=False) -> None:
        self.is_simulation = is_simulation
        # os.environ["GOOGLE_API_KEY"] = dotenv.get_key(".env","gemini_api")
        self.model = init_chat_model(
            model="gemini-2.5-flash-lite",
            model_provider="google_genai"
        )

    def invoke(self, messages):
        if self.is_simulation:
            return "Simulation answer"
        response = self.model.invoke(messages).content
        return response

class ContractInfo(TypedDict):
    title: str
    purposes: List[str]  # "employment" or "rental"
    parties: List[str]
    status: Optional[str]   # "Valid", "Unsigned", "Expired"
    misc_info: dict

    text: str
    embeddings: Optional[str]

class AuxFileInfo(TypedDict):
    category: Optional[str]   # Bank statement, email, proof 
    purposes: List[str]   # Bank statement, email, proof 
    relation_to_contract: List[str] # Supplimentary, evidence, rule against
    misc_info: dict

    text: str
    embeddings: Optional[str]

# Define the state structure
class AdvisoryState(TypedDict):
    """State for the contract advisory workflow"""
    # Core information
    contracts: List[ContractInfo]
    user_intro: str
    
    # Analysis results
    key_clauses: dict  # Key clauses organized by category {contract: [{chapter: sentence, ...}]}
    major_issues: List[str]  # Red flags or concerns
    risk_assessment: str  # Advantage and risk levels for different aspects
    
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


class AdvisoryWorkflow:
    def __init__(self) -> None:
        self.model = AIModel(False)

    def reception(self, state: AdvisoryState):
        intro = state.get("user_intro")
        self.model.invoke()

# Testing AI.
if __name__ == '__main__':
    print('hi')
    ai = AIModel()
    messages = [
        SystemMessage(content="You are a bossy grumpy AI"),
        HumanMessage(content="hi!"),
        AIMessage(content="mpfh."),
        HumanMessage(content="Umm. Hii? How r you doing? Isnt it lovely today?"),
        AIMessage("Eh."),
        HumanMessage("I mean look at it! So sunny and clean!")
    ]

    print(ai.invoke(messages))