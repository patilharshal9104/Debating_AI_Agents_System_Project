"""
debate_agent.py - Debate agent logic with lawyer-style critique
"""

from typing import List, Tuple
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import Tool
from web_loader import validate_reference

class DebateAgent:
    def __init__(self, name: str, llm_call_func):
        self.name = name
        self.llm_call = llm_call_func
        self.memory = InMemoryChatMessageHistory()
        self.tools = self._init_tools()
    
    def _init_tools(self) -> List[Tool]:
        """Initialize agent tools."""
        return [
            Tool(
                name="reference_checker",
                func=self._check_reference,
                description="Verify a reference URL and get its content snippet"
            ),
            Tool(
                name="debate_history",
                func=self._get_history,
                description="Review past arguments in this debate"
            )
        ]
    
    async def formulate_response(self, prompt: str, stage: str) -> Tuple[str, List[str]]:
        """Formulate a response based on debate stage."""
        print(f"[DEBUG] {self.name} formulating {stage} response")
        full_prompt = f"""
        Debate Context:
        {self._get_history()}
        
        Stage: {stage}
        Task: {prompt}
        
        Provide your response with references in JSON format:
        {{
            {"\"answer\": \"...\"" if stage in ["initial_suggestion", "refinement"] else "\"critique\": \"...\"" if stage == "critique" else "\"final_answer\": \"...\""},
            "references": ["https://url1", "https://url2"]
        }}
        """
        return await self.llm_call(full_prompt)
    
    async def critique_opponent(self, opponent_answer: str, question: str, evidence: str) -> Tuple[str, List[str]]:
        """Critique the opponent's suggestion for flaws."""
        print(f"[DEBUG] {self.name} critiquing opponent")
        critique_prompt = f"""
        As a lawyer-style debate agent for {self.name}, analyze the following opponent suggestion for flaws (e.g., factual inaccuracies, weak evidence, missing points) regarding: {question}
        
        Opponent's suggestion: {opponent_answer}
        Supporting evidence: {evidence}
        
        Provide a concise critique (max 300 words) identifying specific weaknesses and suggest improvements. End with a JSON block:
        {{
            "critique": "...",
            "references": ["https://url1", "https://url2"]
        }}
        """
        return await self.llm_call(critique_prompt)
    
    def _check_reference(self, url: str) -> str:
        """Check a reference URL."""
        is_valid, snippet = validate_reference(url)
        return f"Reference {'VALID' if is_valid else 'INVALID'}: {url}\nSnippet: {snippet[:500]}"
    
    def _get_history(self) -> str:
        """Get debate history."""
        if not self.memory.messages:
            return "No history available"
        return "\n".join([f"{msg.__class__.__name__}: {msg.content}" for msg in self.memory.messages])
    
    def add_to_memory(self, message: str, is_user: bool = False, max_history: int = 10):
        """Add a message to memory."""
        if is_user:
            self.memory.add_message(HumanMessage(content=message))
        else:
            self.memory.add_message(AIMessage(content=message))
        if len(self.memory.messages) > max_history:
            self.memory.messages = self.memory.messages[-max_history:]