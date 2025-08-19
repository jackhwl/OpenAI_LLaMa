import pytest
from unittest.mock import Mock, patch, MagicMock
from ai_generator import AIGenerator
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
        """Test response generation with tool usage"""
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
        
        # Second response - final answer
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
        
        # Verify two API calls were made
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
        mock_client.messages.create.side_effect = anthropic.APIError("API Error")
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