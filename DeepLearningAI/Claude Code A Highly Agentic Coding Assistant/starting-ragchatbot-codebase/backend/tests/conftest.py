import pytest
import os
import tempfile
import shutil
from unittest.mock import Mock, MagicMock
from typing import Dict, List, Any

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simple_vector_store import SimpleVectorStore, SearchResults
from search_tools import CourseSearchTool, CourseOutlineTool, ToolManager
from ai_generator import AIGenerator
from rag_system import RAGSystem
from config import Config
from models import Course, Lesson, CourseChunk


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing"""
    config = Mock(spec=Config)
    config.ANTHROPIC_API_KEY = "test-key"
    config.ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
    config.CHUNK_SIZE = 800
    config.CHUNK_OVERLAP = 100
    config.MAX_RESULTS = 5
    config.MAX_HISTORY = 2
    config.CHROMA_PATH = "./test_chroma_db"
    return config


@pytest.fixture
def temp_vector_store():
    """Create a temporary vector store for testing"""
    temp_dir = tempfile.mkdtemp()
    store = SimpleVectorStore(persist_path=temp_dir, max_results=5)
    yield store
    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_courses():
    """Create sample course data for testing"""
    courses = []
    
    # Course 1
    lessons1 = [
        Lesson(lesson_number=1, title="Introduction to MCP", lesson_link="https://example.com/lesson1"),
        Lesson(lesson_number=2, title="Building Connectors", lesson_link="https://example.com/lesson2"),
    ]
    course1 = Course(
        title="Model Context Protocol (MCP) Course",
        instructor="John Doe",
        course_link="https://example.com/course1",
        lessons=lessons1
    )
    courses.append(course1)
    
    # Course 2  
    lessons2 = [
        Lesson(lesson_number=1, title="Python Basics", lesson_link="https://example.com/py1"),
        Lesson(lesson_number=2, title="Advanced Python", lesson_link="https://example.com/py2"),
    ]
    course2 = Course(
        title="Python Programming Fundamentals",
        instructor="Jane Smith", 
        course_link="https://example.com/course2",
        lessons=lessons2
    )
    courses.append(course2)
    
    return courses


@pytest.fixture
def sample_course_chunks():
    """Create sample course chunks for testing"""
    chunks = []
    
    # MCP Course chunks
    chunks.extend([
        CourseChunk(
            course_title="Model Context Protocol (MCP) Course",
            lesson_number=1,
            chunk_index=0,
            content="Model Context Protocol (MCP) is a revolutionary way to connect AI systems. It provides standardized interfaces for communication between different AI models and external tools."
        ),
        CourseChunk(
            course_title="Model Context Protocol (MCP) Course", 
            lesson_number=1,
            chunk_index=1,
            content="MCP enables seamless integration between Claude and various data sources, APIs, and tools. This allows for more powerful and flexible AI applications."
        ),
        CourseChunk(
            course_title="Model Context Protocol (MCP) Course",
            lesson_number=2, 
            chunk_index=0,
            content="Building MCP connectors requires understanding the protocol specification. Connectors act as bridges between AI models and external systems."
        ),
    ])
    
    # Python Course chunks
    chunks.extend([
        CourseChunk(
            course_title="Python Programming Fundamentals",
            lesson_number=1,
            chunk_index=0,
            content="Python is a high-level programming language known for its simplicity and readability. It's widely used in web development, data science, and AI."
        ),
        CourseChunk(
            course_title="Python Programming Fundamentals",
            lesson_number=2,
            chunk_index=0,
            content="Advanced Python concepts include decorators, context managers, and metaclasses. These features enable more sophisticated programming patterns."
        ),
    ])
    
    return chunks


@pytest.fixture
def populated_vector_store(temp_vector_store, sample_courses, sample_course_chunks):
    """Create a vector store populated with sample data"""
    # Add course metadata
    for course in sample_courses:
        temp_vector_store.add_course_metadata(course)
    
    # Add course content
    temp_vector_store.add_course_content(sample_course_chunks)
    
    return temp_vector_store


@pytest.fixture
def mock_anthropic_client():
    """Create a mock Anthropic client for testing"""
    mock_client = Mock()
    
    # Mock successful response
    mock_response = Mock()
    mock_response.content = [Mock()]
    mock_response.content[0].text = "This is a test response"
    mock_response.stop_reason = "end_turn"
    
    mock_client.messages.create.return_value = mock_response
    
    return mock_client


@pytest.fixture
def mock_anthropic_client_with_tools():
    """Create a mock Anthropic client that simulates tool usage"""
    mock_client = Mock()
    
    # Mock tool use response
    mock_tool_response = Mock()
    mock_tool_content = Mock()
    mock_tool_content.type = "tool_use"
    mock_tool_content.name = "search_course_content"
    mock_tool_content.input = {"query": "test query"}
    mock_tool_content.id = "tool_123"
    
    mock_tool_response.content = [mock_tool_content]
    mock_tool_response.stop_reason = "tool_use"
    
    # Mock final response after tool use
    mock_final_response = Mock()
    mock_final_response.content = [Mock()]
    mock_final_response.content[0].text = "Based on the search results, here's the answer..."
    mock_final_response.stop_reason = "end_turn"
    
    mock_client.messages.create.side_effect = [mock_tool_response, mock_final_response]
    
    return mock_client


@pytest.fixture
def sample_search_results():
    """Create sample search results for testing"""
    return SearchResults(
        documents=[
            "MCP is a revolutionary protocol for AI communication",
            "Python is a versatile programming language"
        ],
        metadata=[
            {
                "course_title": "Model Context Protocol (MCP) Course",
                "lesson_number": 1,
                "chunk_index": 0
            },
            {
                "course_title": "Python Programming Fundamentals", 
                "lesson_number": 1,
                "chunk_index": 0
            }
        ],
        distances=[0.1, 0.2]
    )


@pytest.fixture
def empty_search_results():
    """Create empty search results for testing"""
    return SearchResults(
        documents=[],
        metadata=[],
        distances=[]
    )


@pytest.fixture
def error_search_results():
    """Create error search results for testing"""
    return SearchResults.empty("Search failed due to test error")