import anthropic
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class ConversationState:
    """Manages conversation state across multiple tool calling rounds"""
    messages: List[Dict[str, Any]] = field(default_factory=list)
    system: str = ""
    round_count: int = 0
    max_rounds: int = 2
    final_response: Optional[Any] = None
    tool_execution_errors: List[str] = field(default_factory=list)
    
    def should_continue(self) -> bool:
        """Check if we should continue with another round"""
        return (
            self.final_response is None and
            len(self.tool_execution_errors) < 2
        )
    
    def can_use_tools(self) -> bool:
        """Check if tools can still be used in current round"""
        return self.round_count <= self.max_rounds
    
    def add_message(self, role: str, content: Any):
        """Add a message to the conversation"""
        self.messages.append({"role": role, "content": content})
    
    def increment_round(self):
        """Increment the round counter"""
        self.round_count += 1
    
    def set_final_response(self, response: Any):
        """Set the final response and mark conversation complete"""
        self.final_response = response
    
    def add_tool_error(self, error: str):
        """Add a tool execution error"""
        self.tool_execution_errors.append(error)
    
    def get_final_response_text(self) -> str:
        """Extract and return the final response text"""
        if self.final_response and self.final_response.content and len(self.final_response.content) > 0:
            return self.final_response.content[0].text
        return "I apologize, but I couldn't generate a response. Please try again."

class AIGenerator:
    """Handles interactions with Anthropic's Claude API for generating responses"""
    
    # Static system prompt to avoid rebuilding on each call
    SYSTEM_PROMPT = """ You are an AI assistant specialized in course materials and educational content with access to comprehensive search tools for course information.

Tool Usage Guidelines:
- **Course outline queries**: Use `get_course_outline` for questions about course structure, lesson lists, or complete course overviews
- **Content search queries**: Use `search_course_content` for questions about specific course content or detailed educational materials
- **Sequential tool usage**: You can make up to 2 tool calls in separate rounds to handle complex queries
- **Multi-step reasoning**: Use tool results from earlier rounds to inform subsequent tool calls
- **Complex queries**: Break down multi-part questions into sequential searches
- Synthesize tool results into accurate, fact-based responses
- If tools yield no results, state this clearly without offering alternatives

Sequential Tool Usage Examples:
- "Find a course similar to lesson 4 of course X": First get outline of course X to identify lesson 4 topic, then search for courses with that topic
- "Compare topics between two courses": Get outlines for both courses, then search for specific content comparisons
- "Find advanced material on topic from basic course": First search basic course for topic introduction, then search for advanced materials

Response Protocol:
- **General knowledge questions**: Answer using existing knowledge without using tools
- **Course outline questions**: Use `get_course_outline` tool
- **Course content questions**: Use `search_course_content` tool
- **Complex queries**: Use multiple tool calls in sequence as needed
- **Tool result synthesis**: Integrate information from multiple tool calls into coherent responses
- **No meta-commentary**:
 - Provide direct answers only — no reasoning process, tool explanations, or question-type analysis
 - Do not mention "based on the search results" or "using the outline tool"

For outline responses, include:
- Course title and link
- Complete lesson list with numbers and titles
- Any available lesson links

All responses must be:
1. **Brief, Concise and focused** - Get to the point quickly
2. **Educational** - Maintain instructional value
3. **Clear** - Use accessible language
4. **Example-supported** - Include relevant examples when they aid understanding
Provide only the direct answer to what was asked.
"""
    
    def __init__(self, api_key: str, model: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        
        # Pre-build base API parameters
        self.base_params = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": 800
        }
    
    def generate_response(self, query: str,
                         conversation_history: Optional[str] = None,
                         tools: Optional[List] = None,
                         tool_manager=None,
                         max_rounds: int = 2) -> str:
        """
        Generate AI response with sequential tool calling capability.
        
        Args:
            query: The user's question or request
            conversation_history: Previous messages for context
            tools: Available tools the AI can use
            tool_manager: Manager to execute tools
            max_rounds: Maximum number of tool calling rounds (default 2)
            
        Returns:
            Generated response as string
        """
        
        # Build system content with conversation history
        system_content = self._build_system_content(conversation_history)
        
        # Initialize conversation state
        conversation_state = ConversationState(
            messages=[{"role": "user", "content": query}],
            system=system_content,
            max_rounds=max_rounds
        )
        
        # Sequential tool calling loop
        while conversation_state.should_continue():
            response = self._execute_round(conversation_state, tools, tool_manager)
            
            # Check termination conditions
            if self._should_terminate(response, conversation_state):
                break
        
        return conversation_state.get_final_response_text()
    
    def _build_system_content(self, conversation_history: Optional[str]) -> str:
        """Build system content with conversation history"""
        if conversation_history:
            return f"{self.SYSTEM_PROMPT}\n\nPrevious conversation:\n{conversation_history}"
        return self.SYSTEM_PROMPT
    
    def _execute_round(self, state: ConversationState, tools: Optional[List], tool_manager) -> Any:
        """Execute a single round of conversation with potential tool use"""
        
        state.increment_round()
        
        # Prepare API parameters for this round
        api_params = {
            **self.base_params,
            "messages": state.messages,
            "system": state.system
        }
        
        # Add tools only if we haven't exceeded max rounds
        if tools and state.can_use_tools():
            api_params["tools"] = tools
            api_params["tool_choice"] = {"type": "auto"}
        
        # Make API call
        response = self.client.messages.create(**api_params)
        
        # Handle response based on type
        if response.stop_reason == "tool_use" and tool_manager and state.can_use_tools():
            return self._handle_tool_round(response, state, tool_manager)
        else:
            # Final response - no more tool use
            state.set_final_response(response)
            return response
    
    def _handle_tool_round(self, response, state: ConversationState, tool_manager):
        """Handle a round that involves tool execution"""
        
        # Add Claude's response to conversation
        state.add_message("assistant", response.content)
        
        # Execute all tool calls
        tool_results = []
        for content_block in response.content:
            if content_block.type == "tool_use":
                try:
                    result = tool_manager.execute_tool(
                        content_block.name, 
                        **content_block.input
                    )
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": result
                    })
                except Exception as e:
                    # Handle tool execution errors gracefully
                    error_msg = f"Tool execution failed: {str(e)}"
                    state.add_tool_error(error_msg)
                    tool_results.append({
                        "type": "tool_result", 
                        "tool_use_id": content_block.id,
                        "content": error_msg
                    })
        
        # Add tool results to conversation
        if tool_results:
            state.add_message("user", tool_results)
        
        return response
    
    def _should_terminate(self, response, state: ConversationState) -> bool:
        """Determine if conversation should terminate"""
        
        # Terminate if no tool use in response (final answer received)
        if response.stop_reason != "tool_use":
            state.set_final_response(response)
            return True
        
        # Terminate if too many tool errors
        if len(state.tool_execution_errors) >= 2:
            fallback_response = self._generate_error_fallback(state)
            state.set_final_response(fallback_response)
            return True
        
        return False
    
    def _generate_error_fallback(self, state: ConversationState):
        """Generate fallback response when tool execution fails repeatedly"""
        
        # Make one final API call without tools
        fallback_params = {
            **self.base_params,
            "messages": state.messages + [{
                "role": "user", 
                "content": "Please provide an answer based on your existing knowledge, as the search tools are currently unavailable."
            }],
            "system": state.system
        }
        
        try:
            return self.client.messages.create(**fallback_params)
        except Exception:
            # Create a mock response if API call also fails
            class MockResponse:
                def __init__(self):
                    self.content = [MockContent()]
            
            class MockContent:
                def __init__(self):
                    self.text = "I apologize, but I'm unable to access the course information at this time. Please try again later."
            
            return MockResponse()
    
    def _handle_tool_execution(self, initial_response, base_params: Dict[str, Any], tool_manager):
        """
        DEPRECATED: Legacy method for single-round tool execution.
        New sequential tool calling uses _execute_round and _handle_tool_round instead.
        Kept for backward compatibility.
        
        Args:
            initial_response: The response containing tool use requests
            base_params: Base API parameters  
            tool_manager: Manager to execute tools
            
        Returns:
            Final response text after tool execution
        """
        # Start with existing messages
        messages = base_params["messages"].copy()
        
        # Add AI's tool use response
        messages.append({"role": "assistant", "content": initial_response.content})
        
        # Execute all tool calls and collect results
        tool_results = []
        for content_block in initial_response.content:
            if content_block.type == "tool_use":
                try:
                    tool_result = tool_manager.execute_tool(
                        content_block.name, 
                        **content_block.input
                    )
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": tool_result
                    })
                except Exception as e:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": f"Tool execution failed: {str(e)}"
                    })
        
        # Add tool results as single message
        if tool_results:
            messages.append({"role": "user", "content": tool_results})
        
        # Prepare final API call without tools
        final_params = {
            **self.base_params,
            "messages": messages,
            "system": base_params["system"]
        }
        
        # Get final response
        final_response = self.client.messages.create(**final_params)
        if final_response.content and len(final_response.content) > 0:
            return final_response.content[0].text
        else:
            return "I apologize, but I couldn't generate a response. Please try again."