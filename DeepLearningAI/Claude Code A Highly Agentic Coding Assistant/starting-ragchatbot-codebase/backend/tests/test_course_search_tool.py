import pytest
from unittest.mock import Mock, patch
from search_tools import CourseSearchTool, ToolManager
from simple_vector_store import SearchResults


class TestCourseSearchTool:
    """Test the CourseSearchTool functionality"""
    
    def test_get_tool_definition(self):
        """Test that tool definition is correctly formatted"""
        mock_store = Mock()
        tool = CourseSearchTool(mock_store)
        
        definition = tool.get_tool_definition()
        
        assert definition["name"] == "search_course_content"
        assert "description" in definition
        assert "input_schema" in definition
        assert definition["input_schema"]["required"] == ["query"]
        assert "query" in definition["input_schema"]["properties"]
        assert "course_name" in definition["input_schema"]["properties"]
        assert "lesson_number" in definition["input_schema"]["properties"]

    def test_execute_successful_search(self, sample_search_results):
        """Test successful search execution"""
        mock_store = Mock()
        mock_store.search.return_value = sample_search_results
        mock_store.get_lesson_link.return_value = "https://example.com/lesson1"
        
        tool = CourseSearchTool(mock_store)
        result = tool.execute("test query")
        
        # Verify search was called correctly
        mock_store.search.assert_called_once_with(
            query="test query",
            course_name=None,
            lesson_number=None
        )
        
        # Verify result format
        assert isinstance(result, str)
        assert "Model Context Protocol (MCP) Course" in result
        assert "Python Programming Fundamentals" in result
        assert len(tool.last_sources) == 2

    def test_execute_with_course_filter(self, sample_search_results):
        """Test search with course name filter"""
        mock_store = Mock()
        mock_store.search.return_value = sample_search_results
        mock_store.get_lesson_link.return_value = None
        
        tool = CourseSearchTool(mock_store)
        result = tool.execute("test query", course_name="MCP")
        
        mock_store.search.assert_called_once_with(
            query="test query",
            course_name="MCP",
            lesson_number=None
        )
        assert isinstance(result, str)

    def test_execute_with_lesson_filter(self, sample_search_results):
        """Test search with lesson number filter"""
        mock_store = Mock()
        mock_store.search.return_value = sample_search_results
        mock_store.get_lesson_link.return_value = "https://example.com/lesson1"
        
        tool = CourseSearchTool(mock_store)
        result = tool.execute("test query", lesson_number=1)
        
        mock_store.search.assert_called_once_with(
            query="test query",
            course_name=None,
            lesson_number=1
        )
        assert isinstance(result, str)

    def test_execute_empty_results(self, empty_search_results):
        """Test handling of empty search results"""
        mock_store = Mock()
        mock_store.search.return_value = empty_search_results
        
        tool = CourseSearchTool(mock_store)
        result = tool.execute("non-existent query")
        
        assert "No relevant content found" in result
        assert len(tool.last_sources) == 0

    def test_execute_empty_results_with_filters(self, empty_search_results):
        """Test empty results with filters applied"""
        mock_store = Mock()
        mock_store.search.return_value = empty_search_results
        
        tool = CourseSearchTool(mock_store)
        result = tool.execute("test query", course_name="NonExistent", lesson_number=99)
        
        assert "No relevant content found" in result
        assert "in course 'NonExistent'" in result
        assert "in lesson 99" in result

    def test_execute_search_error(self, error_search_results):
        """Test handling of search errors"""
        mock_store = Mock()
        mock_store.search.return_value = error_search_results
        
        tool = CourseSearchTool(mock_store)
        result = tool.execute("error query")
        
        assert "Search failed due to test error" in result
        assert len(tool.last_sources) == 0

    def test_format_results_with_lesson_links(self):
        """Test result formatting with lesson links"""
        mock_store = Mock()
        mock_store.get_lesson_link.return_value = "https://example.com/lesson1"
        
        tool = CourseSearchTool(mock_store)
        
        # Create sample results
        results = SearchResults(
            documents=["Test content about MCP"],
            metadata=[{
                "course_title": "MCP Course",
                "lesson_number": 1,
                "chunk_index": 0
            }],
            distances=[0.1]
        )
        
        formatted = tool._format_results(results)
        
        assert "[MCP Course - Lesson 1]" in formatted
        assert "Test content about MCP" in formatted
        assert len(tool.last_sources) == 1
        assert tool.last_sources[0]["text"] == "MCP Course - Lesson 1"
        assert tool.last_sources[0]["link"] == "https://example.com/lesson1"

    def test_format_results_without_lesson_links(self):
        """Test result formatting without lesson links"""
        mock_store = Mock()
        mock_store.get_lesson_link.return_value = None
        
        tool = CourseSearchTool(mock_store)
        
        results = SearchResults(
            documents=["Test content"],
            metadata=[{
                "course_title": "Test Course",
                "lesson_number": None,
                "chunk_index": 0
            }],
            distances=[0.1]
        )
        
        formatted = tool._format_results(results)
        
        assert "[Test Course]" in formatted
        assert "Test content" in formatted
        assert tool.last_sources[0]["link"] is None

    def test_sources_reset_functionality(self, sample_search_results):
        """Test that sources are properly tracked and can be reset"""
        mock_store = Mock()
        mock_store.search.return_value = sample_search_results
        mock_store.get_lesson_link.return_value = None
        
        tool = CourseSearchTool(mock_store)
        
        # Execute search to populate sources
        tool.execute("test query")
        assert len(tool.last_sources) > 0
        
        # Reset sources
        tool.last_sources = []
        assert len(tool.last_sources) == 0


class TestToolManager:
    """Test the ToolManager functionality"""
    
    def test_register_tool(self):
        """Test tool registration"""
        manager = ToolManager()
        mock_store = Mock()
        tool = CourseSearchTool(mock_store)
        
        manager.register_tool(tool)
        
        assert "search_course_content" in manager.tools
        assert manager.tools["search_course_content"] == tool

    def test_get_tool_definitions(self):
        """Test getting all tool definitions"""
        manager = ToolManager()
        mock_store = Mock()
        tool = CourseSearchTool(mock_store)
        
        manager.register_tool(tool)
        definitions = manager.get_tool_definitions()
        
        assert len(definitions) == 1
        assert definitions[0]["name"] == "search_course_content"

    def test_execute_tool(self, sample_search_results):
        """Test tool execution through manager"""
        manager = ToolManager()
        mock_store = Mock()
        mock_store.search.return_value = sample_search_results
        mock_store.get_lesson_link.return_value = None
        
        tool = CourseSearchTool(mock_store)
        manager.register_tool(tool)
        
        result = manager.execute_tool("search_course_content", query="test")
        
        assert isinstance(result, str)
        mock_store.search.assert_called_once()

    def test_execute_nonexistent_tool(self):
        """Test executing a tool that doesn't exist"""
        manager = ToolManager()
        
        result = manager.execute_tool("nonexistent_tool", query="test")
        
        assert "Tool 'nonexistent_tool' not found" in result

    def test_get_last_sources(self, sample_search_results):
        """Test getting sources from last search"""
        manager = ToolManager()
        mock_store = Mock()
        mock_store.search.return_value = sample_search_results
        mock_store.get_lesson_link.return_value = None
        
        tool = CourseSearchTool(mock_store)
        manager.register_tool(tool)
        
        # Execute to populate sources
        manager.execute_tool("search_course_content", query="test")
        sources = manager.get_last_sources()
        
        assert len(sources) > 0

    def test_reset_sources(self, sample_search_results):
        """Test resetting sources across all tools"""
        manager = ToolManager()
        mock_store = Mock()
        mock_store.search.return_value = sample_search_results
        mock_store.get_lesson_link.return_value = None
        
        tool = CourseSearchTool(mock_store)
        manager.register_tool(tool)
        
        # Execute to populate sources
        manager.execute_tool("search_course_content", query="test")
        assert len(manager.get_last_sources()) > 0
        
        # Reset sources
        manager.reset_sources()
        assert len(manager.get_last_sources()) == 0