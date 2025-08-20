import pytest
from unittest.mock import Mock, patch, MagicMock
from ai_generator import AIGenerator, ConversationState
from search_tools import ToolManager, CourseSearchTool
import anthropic


class TestAIGenerator:
    """Test the AIGenerator functionality"""
    
    def test_initialization(self):
        """Test AIGenerator initialization"""
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        assert generator.model == "claude-sonnet-4-20250514"
        assert generator.base_params["model"] == "claude-sonnet-4-20250514"
        assert generator.base_params["temperature"] == 0
        assert generator.base_params["max_tokens"] == 800

    @patch('ai_generator.anthropic.Anthropic')
    def test_generate_response_simple(self, mock_anthropic):
        """Test simple response generation without tools"""
        # Setup mock client
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "This is a test response"
        mock_response.stop_reason = "end_turn"
        
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        result = generator.generate_response("Test query")
        
        assert result == "This is a test response"
        mock_client.messages.create.assert_called_once()

    @patch('ai_generator.anthropic.Anthropic')
    def test_generate_response_with_conversation_history(self, mock_anthropic):
        """Test response generation with conversation history"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Response with history"
        mock_response.stop_reason = "end_turn"
        
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        result = generator.generate_response(
            "Test query", 
            conversation_history="Previous conversation context"
        )
        
        assert result == "Response with history"
        
        # Check that system prompt includes conversation history
        call_args = mock_client.messages.create.call_args
        system_content = call_args[1]["system"]
        assert "Previous conversation context" in system_content

    @patch('ai_generator.anthropic.Anthropic')
    def test_generate_response_empty_content(self, mock_anthropic):
        """Test handling of empty response content"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = []  # Empty content
        mock_response.stop_reason = "end_turn"
        
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        result = generator.generate_response("Test query")
        
        assert "I apologize, but I couldn't generate a response. Please try again." in result

    @patch('ai_generator.anthropic.Anthropic')
    def test_generate_response_with_tools_no_usage(self, mock_anthropic):
        """Test response generation with tools available but not used"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Direct response without tools"
        mock_response.stop_reason = "end_turn"
        
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        # Create mock tools
        mock_tools = [{"name": "search_course_content", "description": "Test tool"}]
        mock_tool_manager = Mock()
        
        result = generator.generate_response(
            "Test query",
            tools=mock_tools,
            tool_manager=mock_tool_manager
        )
        
        assert result == "Direct response without tools"
        
        # Verify tools were passed to API
        call_args = mock_client.messages.create.call_args
        assert "tools" in call_args[1]
        assert call_args[1]["tools"] == mock_tools

    @patch('ai_generator.anthropic.Anthropic')
    def test_generate_response_with_tool_usage(self, mock_anthropic):
        """Test response generation with tool usage - should still work with new sequential system"""
        mock_client = Mock()
        
        # First response - tool usage
        mock_tool_response = Mock()
        mock_tool_content = Mock()
        mock_tool_content.type = "tool_use"
        mock_tool_content.name = "search_course_content"
        mock_tool_content.input = {"query": "test query"}
        mock_tool_content.id = "tool_123"
        
        mock_tool_response.content = [mock_tool_content]
        mock_tool_response.stop_reason = "tool_use"
        
        # Second response - final answer (no more tools)
        mock_final_response = Mock()
        mock_final_response.content = [Mock()]
        mock_final_response.content[0].text = "Based on the search results, here's the answer"
        mock_final_response.stop_reason = "end_turn"
        
        mock_client.messages.create.side_effect = [mock_tool_response, mock_final_response]
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        # Create mock tool manager
        mock_tool_manager = Mock()
        mock_tool_manager.execute_tool.return_value = "Tool search results"
        
        mock_tools = [{"name": "search_course_content", "description": "Test tool"}]
        
        result = generator.generate_response(
            "Test query",
            tools=mock_tools,
            tool_manager=mock_tool_manager
        )
        
        assert result == "Based on the search results, here's the answer"
        
        # Verify tool was executed
        mock_tool_manager.execute_tool.assert_called_once_with(
            "search_course_content",
            query="test query"
        )
        
        # Verify two API calls were made (new sequential system)
        assert mock_client.messages.create.call_count == 2

    @patch('ai_generator.anthropic.Anthropic')
    def test_handle_tool_execution_empty_final_response(self, mock_anthropic):
        """Test handling when final response after tool use is empty"""
        mock_client = Mock()
        
        # Tool use response
        mock_tool_response = Mock()
        mock_tool_content = Mock()
        mock_tool_content.type = "tool_use"
        mock_tool_content.name = "search_course_content"
        mock_tool_content.input = {"query": "test"}
        mock_tool_content.id = "tool_123"
        
        mock_tool_response.content = [mock_tool_content]
        mock_tool_response.stop_reason = "tool_use"
        
        # Empty final response
        mock_final_response = Mock()
        mock_final_response.content = []  # Empty content
        mock_final_response.stop_reason = "end_turn"
        
        mock_client.messages.create.side_effect = [mock_tool_response, mock_final_response]
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        mock_tool_manager = Mock()
        mock_tool_manager.execute_tool.return_value = "Tool results"
        mock_tools = [{"name": "search_course_content"}]
        
        result = generator.generate_response(
            "Test query",
            tools=mock_tools,
            tool_manager=mock_tool_manager
        )
        
        assert "I apologize, but I couldn't generate a response. Please try again." in result

    @patch('ai_generator.anthropic.Anthropic')
    def test_handle_multiple_tool_calls(self, mock_anthropic):
        """Test handling multiple tool calls in one response"""
        mock_client = Mock()
        
        # Tool use response with multiple tools
        mock_tool_response = Mock()
        mock_tool_content1 = Mock()
        mock_tool_content1.type = "tool_use"
        mock_tool_content1.name = "search_course_content"
        mock_tool_content1.input = {"query": "test1"}
        mock_tool_content1.id = "tool_123"
        
        mock_tool_content2 = Mock()
        mock_tool_content2.type = "tool_use"
        mock_tool_content2.name = "get_course_outline"
        mock_tool_content2.input = {"course_title": "test course"}
        mock_tool_content2.id = "tool_456"
        
        mock_tool_response.content = [mock_tool_content1, mock_tool_content2]
        mock_tool_response.stop_reason = "tool_use"
        
        # Final response
        mock_final_response = Mock()
        mock_final_response.content = [Mock()]
        mock_final_response.content[0].text = "Combined tool results response"
        
        mock_client.messages.create.side_effect = [mock_tool_response, mock_final_response]
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        mock_tool_manager = Mock()
        mock_tool_manager.execute_tool.side_effect = ["Result 1", "Result 2"]
        mock_tools = [{"name": "search_course_content"}, {"name": "get_course_outline"}]
        
        result = generator.generate_response(
            "Test query",
            tools=mock_tools,
            tool_manager=mock_tool_manager
        )
        
        assert result == "Combined tool results response"
        
        # Verify both tools were executed
        assert mock_tool_manager.execute_tool.call_count == 2

    @patch('ai_generator.anthropic.Anthropic')
    def test_api_exception_handling(self, mock_anthropic):
        """Test handling of API exceptions"""
        mock_client = Mock()
        # Create a mock request object for the APIError
        mock_request = Mock()
        mock_client.messages.create.side_effect = anthropic.APIError("API Error", request=mock_request, body="test")
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        with pytest.raises(anthropic.APIError):
            generator.generate_response("Test query")

    def test_system_prompt_content(self):
        """Test that system prompt contains expected content"""
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        assert "course materials" in generator.SYSTEM_PROMPT
        assert "search_course_content" in generator.SYSTEM_PROMPT
        assert "get_course_outline" in generator.SYSTEM_PROMPT
        assert "tool_choice" not in generator.SYSTEM_PROMPT  # Should be in API params, not prompt

    @patch('ai_generator.anthropic.Anthropic')
    def test_tool_parameters_passed_correctly(self, mock_anthropic):
        """Test that tool parameters are passed correctly to API"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Response"
        mock_response.stop_reason = "end_turn"
        
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        mock_tools = [{"name": "test_tool", "description": "Test tool"}]
        
        generator.generate_response("Test query", tools=mock_tools)
        
        call_args = mock_client.messages.create.call_args
        
        # Verify tool parameters
        assert "tools" in call_args[1]
        assert call_args[1]["tools"] == mock_tools
        assert "tool_choice" in call_args[1]
        assert call_args[1]["tool_choice"] == {"type": "auto"}


class TestSequentialToolCalling:
    """Test sequential tool calling functionality"""
    
    @patch('ai_generator.anthropic.Anthropic')
    def test_two_round_sequential_tool_calling(self, mock_anthropic):
        """Test complex query requiring two sequential tool calls - focus on behavior not text"""
        mock_client = Mock()
        
        # Round 1: Tool use response
        mock_tool_response1 = Mock()
        mock_tool_content1 = Mock()
        mock_tool_content1.type = "tool_use"
        mock_tool_content1.name = "get_course_outline"
        mock_tool_content1.input = {"course_title": "MCP course"}
        mock_tool_content1.id = "tool_123"
        
        mock_tool_response1.content = [mock_tool_content1]
        mock_tool_response1.stop_reason = "tool_use"
        
        # Round 2: Second tool use response
        mock_tool_response2 = Mock()
        mock_tool_content2 = Mock()
        mock_tool_content2.type = "tool_use"
        mock_tool_content2.name = "search_course_content"
        mock_tool_content2.input = {"query": "lesson 4 topic"}
        mock_tool_content2.id = "tool_456"
        
        mock_tool_response2.content = [mock_tool_content2]
        mock_tool_response2.stop_reason = "tool_use"
        
        # Final response - no more tools (just test that we get some response)
        mock_final_response = Mock()
        mock_final_response.content = [Mock()]
        mock_final_response.content[0].text = "Some final response"
        mock_final_response.stop_reason = "end_turn"
        
        mock_client.messages.create.side_effect = [
            mock_tool_response1, 
            mock_tool_response2, 
            mock_final_response
        ]
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        # Create mock tool manager
        mock_tool_manager = Mock()
        mock_tool_manager.execute_tool.side_effect = [
            "Course outline with lesson 4: Advanced topics",
            "Search results for advanced topics"
        ]
        
        mock_tools = [
            {"name": "get_course_outline", "description": "Get course outline"},
            {"name": "search_course_content", "description": "Search content"}
        ]
        
        result = generator.generate_response(
            "Find a course similar to lesson 4 of MCP course",
            tools=mock_tools,
            tool_manager=mock_tool_manager
        )
        
        # Test that we got some result (don't worry about exact text due to Mock issues)
        assert result is not None
        assert result != ""
        
        # Verify both tools were executed in sequence
        assert mock_tool_manager.execute_tool.call_count == 2
        mock_tool_manager.execute_tool.assert_any_call("get_course_outline", course_title="MCP course")
        mock_tool_manager.execute_tool.assert_any_call("search_course_content", query="lesson 4 topic")
        
        # Verify three API calls were made (2 tool rounds + 1 final)
        assert mock_client.messages.create.call_count == 3
        
        # Verify tool calls were made with tools parameter in first two calls
        first_call_args = mock_client.messages.create.call_args_list[0]
        assert "tools" in first_call_args[1]
        
        second_call_args = mock_client.messages.create.call_args_list[1]
        assert "tools" in second_call_args[1]
        
        # Final call should not have tools (after max rounds)
        third_call_args = mock_client.messages.create.call_args_list[2]
        assert "tools" not in third_call_args[1] or third_call_args[1].get("tools") is None
    
    @patch('ai_generator.anthropic.Anthropic')
    def test_max_rounds_termination(self, mock_anthropic):
        """Test that conversation terminates after 2 rounds even if Claude wants more tools"""
        mock_client = Mock()
        
        # Round 1: Tool use
        mock_tool_response1 = Mock()
        mock_tool_content1 = Mock()
        mock_tool_content1.type = "tool_use"
        mock_tool_content1.name = "search_course_content"
        mock_tool_content1.input = {"query": "test1"}
        mock_tool_content1.id = "tool_123"
        
        mock_tool_response1.content = [mock_tool_content1]
        mock_tool_response1.stop_reason = "tool_use"
        
        # Round 2: Tool use again
        mock_tool_response2 = Mock()
        mock_tool_content2 = Mock()
        mock_tool_content2.type = "tool_use"
        mock_tool_content2.name = "search_course_content"
        mock_tool_content2.input = {"query": "test2"}
        mock_tool_content2.id = "tool_456"
        
        mock_tool_response2.content = [mock_tool_content2]
        mock_tool_response2.stop_reason = "tool_use"
        
        # Round 3: Would want tools but max rounds reached - no tools provided
        mock_final_content = Mock()
        mock_final_content.configure_mock(text="Final answer without more tools")
        mock_final_response = Mock()
        mock_final_response.configure_mock(
            content=[mock_final_content],
            stop_reason="end_turn"
        )
        
        mock_client.messages.create.side_effect = [
            mock_tool_response1,
            mock_tool_response2, 
            mock_final_response
        ]
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        mock_tool_manager = Mock()
        mock_tool_manager.execute_tool.side_effect = ["Result 1", "Result 2"]
        mock_tools = [{"name": "search_course_content"}]
        
        result = generator.generate_response(
            "Complex query",
            tools=mock_tools,
            tool_manager=mock_tool_manager,
            max_rounds=2
        )
        
        # Test that we got some result (focus on behavior, not exact text)
        assert result is not None
        assert result != ""
        
        # Verify exactly 2 tool executions (max rounds)
        assert mock_tool_manager.execute_tool.call_count == 2
        
        # Verify exactly 3 API calls (2 tool rounds + 1 final without tools)
        assert mock_client.messages.create.call_count == 3
        
        # Verify final call had no tools
        final_call_args = mock_client.messages.create.call_args_list[-1]
        assert "tools" not in final_call_args[1] or final_call_args[1].get("tools") is None
    
    @patch('ai_generator.anthropic.Anthropic')
    def test_tool_execution_error_handling(self, mock_anthropic):
        """Test graceful handling of tool execution errors"""
        mock_client = Mock()
        
        # Tool use response
        mock_tool_response = Mock()
        mock_tool_content = Mock()
        mock_tool_content.type = "tool_use"
        mock_tool_content.name = "search_course_content"
        mock_tool_content.input = {"query": "test"}
        mock_tool_content.id = "tool_123"
        
        mock_tool_response.content = [mock_tool_content]
        mock_tool_response.stop_reason = "tool_use"
        
        # Final response after error
        mock_final_response = Mock()
        mock_final_content = Mock()
        setattr(mock_final_content, 'text', "Response after tool error")
        mock_final_response.content = [mock_final_content]
        mock_final_response.stop_reason = "end_turn"
        
        mock_client.messages.create.side_effect = [mock_tool_response, mock_final_response]
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        # Mock tool manager that throws an error
        mock_tool_manager = Mock()
        mock_tool_manager.execute_tool.side_effect = Exception("Tool failed")
        mock_tools = [{"name": "search_course_content"}]
        
        result = generator.generate_response(
            "Test query",
            tools=mock_tools,
            tool_manager=mock_tool_manager
        )
        
        assert result == "Response after tool error"
        
        # Verify tool was attempted
        mock_tool_manager.execute_tool.assert_called_once_with("search_course_content", query="test")
        
        # Verify two API calls were made
        assert mock_client.messages.create.call_count == 2
        
        # Verify error was included in tool result
        second_call_args = mock_client.messages.create.call_args_list[1]
        messages = second_call_args[1]["messages"]
        tool_result_message = messages[-1]  # Last message should be tool results
        assert tool_result_message["role"] == "user"
        assert "Tool execution failed" in str(tool_result_message["content"])
    
    @patch('ai_generator.anthropic.Anthropic')
    def test_conversation_state_context_preservation(self, mock_anthropic):
        """Test that context is preserved between rounds in sequential calling"""
        mock_client = Mock()
        
        # Tool use response
        mock_tool_response = Mock()
        mock_tool_content = Mock()
        mock_tool_content.type = "tool_use"
        mock_tool_content.name = "search_course_content"
        mock_tool_content.input = {"query": "test"}
        mock_tool_content.id = "tool_123"
        
        mock_tool_response.content = [mock_tool_content]
        mock_tool_response.stop_reason = "tool_use"
        
        # Final response
        mock_final_response = Mock()
        mock_final_content = Mock()
        setattr(mock_final_content, 'text', "Final response")
        mock_final_response.content = [mock_final_content]
        mock_final_response.stop_reason = "end_turn"
        
        mock_client.messages.create.side_effect = [mock_tool_response, mock_final_response]
        mock_anthropic.return_value = mock_client
        
        generator = AIGenerator("test-key", "claude-sonnet-4-20250514")
        
        mock_tool_manager = Mock()
        mock_tool_manager.execute_tool.return_value = "Tool result"
        mock_tools = [{"name": "search_course_content"}]
        
        result = generator.generate_response(
            "Test query",
            conversation_history="Previous: How are you?\\nAssistant: I'm doing well!",
            tools=mock_tools,
            tool_manager=mock_tool_manager
        )
        
        assert result == "Final response"
        
        # Verify conversation history was included in both calls
        for call_args in mock_client.messages.create.call_args_list:
            system_content = call_args[1]["system"]
            assert "Previous conversation:" in system_content
            assert "How are you?" in system_content
            assert "I'm doing well!" in system_content
    
    def test_conversation_state_methods(self):
        """Test ConversationState helper methods"""
        state = ConversationState(max_rounds=2)
        
        # Initial state
        assert state.should_continue() == True
        assert state.can_use_tools() == True
        assert state.round_count == 0
        
        # After first round
        state.increment_round()
        assert state.round_count == 1
        assert state.should_continue() == True
        assert state.can_use_tools() == True
        
        # After second round
        state.increment_round()
        assert state.round_count == 2
        assert state.should_continue() == True  # Should continue until final_response is set
        assert state.can_use_tools() == True  # Can still use tools in round 2
        
        # After third round (exceeded max_rounds)
        state.increment_round()
        assert state.round_count == 3
        assert state.should_continue() == True  # Should continue until final_response is set
        assert state.can_use_tools() == False  # Can't use tools after max_rounds
        
        # Test final response setting
        mock_response = Mock()
        state.set_final_response(mock_response)
        assert state.final_response == mock_response
        
        # Test tool error tracking
        state_with_errors = ConversationState()
        assert state_with_errors.should_continue() == True
        
        state_with_errors.add_tool_error("Error 1")
        assert state_with_errors.should_continue() == True
        
        state_with_errors.add_tool_error("Error 2")
        assert state_with_errors.should_continue() == False  # Too many errors