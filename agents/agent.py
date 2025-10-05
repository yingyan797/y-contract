from typing import TypedDict, List, Optional, Annotated
import operator, os, dotenv, json
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models.base import init_chat_model
from agents.prompts import IntroPrompts, ContractOutlinePrompts, ContractResearchPrompts

class AIModel:
    def __init__(self, is_simulation) -> None:
        self.is_simulation = is_simulation
        self.invoke_count = 0
        os.environ["GOOGLE_API_KEY"] = dotenv.get_key(".env","gemini_api")
        self.model = init_chat_model(
            model="gemini-2.5-flash-lite",
            model_provider="google_genai"
        )

    def invoke(self, prompt):
        if self.is_simulation:
            return "Simulation answer"
        response = self.model.invoke(prompt).content
        self.invoke_count += 1
        return response

# class ContractInfo(TypedDict):
#     title: str
#     purposes: List[str]  # "employment" or "rental"
#     parties: List[str]
#     status: Optional[str]   # "Valid", "Unsigned", "Expired"
#     misc_info: dict

#     text: str
#     embeddings: Optional[str]

# class AuxFileInfo(TypedDict):
#     category: Optional[str]   # Bank statement, email, proof 
#     purposes: List[str]   # Bank statement, email, proof 
#     relation_to_contract: List[str] # Supplimentary, evidence, rule against
#     misc_info: dict

#     text: str
#     embeddings: Optional[str]

# Define the state structure
class AdvisoryState(TypedDict):
    """State for the contract advisory workflow"""
    # Flow control
    accept_client_response: bool = False
    ai_response: Optional[str]

    # Core information
    all_contracts: List[str]
    added_contracts: List[str]
    contracts_info: List[dict]

    client_intro: str
    client_needs: List[str]
    
    # Analysis results
    contract_assessment: str  # Advantage and risk levels for different aspects
    
    # Information gathering
    supplementary_materials: List[dict]  # Additional docs/context
    
    # Advice generation
    advice_steps: List[str] # Progressive ai advice
    final_advice: Optional[str]  # Comprehensive final advice based on each step


class AdvisoryWorkflow:
    def __init__(self) -> None:
        self.model = AIModel(False)

    def reception(self, state: AdvisoryState) -> AdvisoryState:
        intro = state.get("client_intro")
        state["client_needs"] = intro
        response = ""
        if state.get("added_contracts"):
            state = self._contract_overview(state)
            prompt = IntroPrompts.format(
                intro=intro,
                contracts_info=state["contracts_info"] 
            )
            response = self.model.invoke(prompt)

        else:
            prompt = """
                You are a general legal consultant. Client asks you for help with their circumstances. Provide direct response, and
                suggest whether they need to provide contract documents or other supplimentary documents to better proceed.

                Your response:
            """
            state["accept_client_response"] = True
            response = self.model.invoke(prompt)
        state["ai_response"] = response
        return state

    def _contract_overview(self, state: AdvisoryState) -> AdvisoryState:
        issues = state.get("client_needs")
        added_contracts = state.get("added_contracts")
        if state.get("added_contracts"):
            prompt = ContractOutlinePrompts.format(
                client_needs=issues,
                added_contracts=json.dumps(added_contracts)
            )
            response = self.model.invoke(prompt)
            state["all_contracts"].extend(added_contracts)
            state["contracts_info"].extend(json.loads(response))
            state["added_contracts"] = []
        return state

    def contract_research(self, state:AdvisoryState) -> AdvisoryState:
        prompt = ContractResearchPrompts.format(
            contracts_info=state.get("contracts_info"),
            client_needs=state.get("client_needs")
        )
        return state


