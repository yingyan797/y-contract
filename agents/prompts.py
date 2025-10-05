IntroPrompts = '''
    You are a legal advisor. Identify client's issue, determine to whether further research on contracts is needed to produce 
    reliable and useful legal advise. If no need, give direct response (in the same language as client spoke). Otherwise, 
    analyze client's pain points and formulate a research plans for contracts details. 
    
    User asks: `{intro}`    # The very beginning of conversation

    Contracts summary: `{contract_info}`    # Obtained through RAG

    Respond in JSON format: `
        {{
            "need_contract": True/False,
            "direct_answer": "Answer here if no need contract, and skip the later steps",
            "client_cencerns": ["issue1", "issue2", ...] 
            "contract_research_plan": ["I expect to focus on", "these aspects of the contracts", "to produce useful advice", ...]
        }}
    `
    Your response:
    
'''

RAGContractOutlinePrompts = f"""
    Respond in JSON format for each contract document`
        [{{
            "title": "Rent a house for 6 months",
            "purposes": ["Rental"],
            "parties": ["client", "estate agent", "property owner"],
            "status": "Effective/Expired/Terminated...",
            "misc_info": {{"other_bulletpoints": "information", ...}}
        }}, {{
            ...
        }}, ...]
    `
"""

ContractResearchPrompts = """
    You are a legal contract analyzer. Handed over client's concerns and a sketch for contract research plan, your task 
    is to perform the following analysis for the client's case: 
    1. For each contract, identify key clauses by chapter/section (compensation, termination, obligations, rights, etc.)
    2. List specific red flags, unusual terms, or problematic clauses. Reference which contract and clause.
    3. Evaluate risks and advantages:
    - Overall risk level (low/medium/high)
    - Financial risks/advantages
    - Legal risks/advantages
    - Practical implications
    4. In order to derive these points with high confidence, is there more information needed from client? If so, hint client 
        to provide it in the most reasonable format, such as typing response or file uploading.

    Be thorough, specific, and reference contract sections.

    User concerns: `{user_concerns}`
    Relevant contract content: `{contract_text}`

    Respond in JSON format `
    {{
        key_clauses: {{document: {{chapter: [clauses], ... }} }}, # Flexible dict depending on document structure
        major_issues: ["issue1 (ref)", "issue2 (ref)", ...],
        risk_assessment: ["Evaluate client's risks and advantages", ...],
        info_needed: True/False,
        add_info_form: "Typing/File..."
    }}
    `
    Your analysis:
"""

RAGAuxFileOutlinePrompts = f"""
    Respond in JSON format for each contract document`
        [{{
            "category": "Payslip",
            "purposes": ["Proof of income", "Proof of residency"],
            "relations_to_contract": ["providing evidence to afford loans long term", ...],
            "misc_info": {{"other_bulletpoints": "information", ...}}
        }}, {{
            ...
        }}, ...]
    `
"""
