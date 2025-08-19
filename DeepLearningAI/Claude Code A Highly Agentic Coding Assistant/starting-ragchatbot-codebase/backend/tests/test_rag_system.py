import pytest
import tempfile
import shutil
import os
from unittest.mock import Mock, patch, MagicMock
from rag_system import RAGSystem
from models import Course, Lesson, CourseChunk


class TestRAGSystem:
    """Test the RAGSystem integration functionality"""
    
    @pytest.fixture
    def mock_rag_system(self, mock_config):
        """Create a RAG system with mocked dependencies"""
        with patch('rag_system.DocumentProcessor'), \
             patch('rag_system.SimpleVectorStore'), \
             patch('rag_system.AIGenerator'), \
             patch('rag_system.SessionManager'), \
             patch('rag_system.ToolManager'), \
             patch('rag_system.CourseSearchTool'), \
             patch('rag_system.CourseOutlineTool'):
            
            rag_system = RAGSystem(mock_config)
            return rag_system

    def test_initialization(self, mock_rag_system, mock_config):
        """Test RAG system initialization"""
        assert mock_rag_system.config == mock_config
        assert hasattr(mock_rag_system, 'document_processor')
        assert hasattr(mock_rag_system, 'vector_store')
        assert hasattr(mock_rag_system, 'ai_generator')
        assert hasattr(mock_rag_system, 'session_manager')
        assert hasattr(mock_rag_system, 'tool_manager')
        assert hasattr(mock_rag_system, 'search_tool')
        assert hasattr(mock_rag_system, 'outline_tool')

    def test_add_course_document_success(self, mock_rag_system):
        """Test successful course document addition"""
        # Mock document processor
        mock_course = Mock(spec=Course)
        mock_course.title = "Test Course"
        mock_chunks = [Mock(spec=CourseChunk), Mock(spec=CourseChunk)]
        
        mock_rag_system.document_processor.process_course_document.return_value = (mock_course, mock_chunks)
        
        course, chunk_count = mock_rag_system.add_course_document("/fake/path.pdf")
        
        assert course == mock_course
        assert chunk_count == 2
        
        # Verify vector store calls
        mock_rag_system.vector_store.add_course_metadata.assert_called_once_with(mock_course)
        mock_rag_system.vector_store.add_course_content.assert_called_once_with(mock_chunks)

    def test_add_course_document_failure(self, mock_rag_system):
        """Test course document addition failure"""
        mock_rag_system.document_processor.process_course_document.side_effect = Exception("Processing failed")
        
        course, chunk_count = mock_rag_system.add_course_document("/fake/path.pdf")
        
        assert course is None
        assert chunk_count == 0

    @patch('rag_system.os.path.exists')
    @patch('rag_system.os.listdir')
    def test_add_course_folder_success(self, mock_listdir, mock_exists, mock_rag_system):
        """Test successful course folder addition"""
        mock_exists.return_value = True
        mock_listdir.return_value = ["course1.pdf", "course2.pdf", "ignored.txt"]
        
        # Mock existing courses
        mock_rag_system.vector_store.get_existing_course_titles.return_value = set()
        
        # Mock document processing
        mock_course1 = Mock(spec=Course)
        mock_course1.title = "Course 1"
        mock_chunks1 = [Mock(), Mock()]
        
        mock_course2 = Mock(spec=Course)
        mock_course2.title = "Course 2"
        mock_chunks2 = [Mock()]
        
        mock_rag_system.document_processor.process_course_document.side_effect = [
            (mock_course1, mock_chunks1),
            (mock_course2, mock_chunks2)
        ]
        
        courses, chunks = mock_rag_system.add_course_folder("/fake/folder")
        
        assert courses == 2
        assert chunks == 3

    @patch('rag_system.os.path.exists')
    def test_add_course_folder_nonexistent(self, mock_exists, mock_rag_system):
        """Test course folder addition with nonexistent folder"""
        mock_exists.return_value = False
        
        courses, chunks = mock_rag_system.add_course_folder("/fake/folder")
        
        assert courses == 0
        assert chunks == 0

    def test_query_without_session(self, mock_rag_system):
        """Test query processing without session ID"""
        mock_rag_system.ai_generator.generate_response.return_value = "Test response"
        mock_rag_system.tool_manager.get_last_sources.return_value = []
        
        response, sources = mock_rag_system.query("What is MCP?")
        
        assert response == "Test response"
        assert sources == []
        
        # Verify AI generator was called with correct parameters
        mock_rag_system.ai_generator.generate_response.assert_called_once()
        call_args = mock_rag_system.ai_generator.generate_response.call_args
        
        assert "What is MCP?" in call_args[1]["query"]
        assert call_args[1]["conversation_history"] is None
        assert call_args[1]["tools"] is not None
        assert call_args[1]["tool_manager"] is not None

    def test_query_with_session(self, mock_rag_system):
        """Test query processing with session ID"""
        session_id = "test-session-123"
        mock_rag_system.session_manager.get_conversation_history.return_value = "Previous conversation"
        mock_rag_system.ai_generator.generate_response.return_value = "Test response with context"
        mock_rag_system.tool_manager.get_last_sources.return_value = [{"text": "Source 1"}]
        
        response, sources = mock_rag_system.query("Follow-up question", session_id=session_id)
        
        assert response == "Test response with context"
        assert len(sources) == 1
        
        # Verify session manager calls
        mock_rag_system.session_manager.get_conversation_history.assert_called_once_with(session_id)
        mock_rag_system.session_manager.add_exchange.assert_called_once_with(
            session_id, "Follow-up question", "Test response with context"
        )
        
        # Verify AI generator was called with conversation history
        call_args = mock_rag_system.ai_generator.generate_response.call_args
        assert call_args[1]["conversation_history"] == "Previous conversation"

    def test_query_with_sources(self, mock_rag_system):
        """Test query processing that returns sources"""
        mock_sources = [
            {"text": "MCP Course - Lesson 1", "link": "https://example.com/lesson1"},
            {"text": "Python Course - Lesson 2", "link": None}
        ]
        
        mock_rag_system.ai_generator.generate_response.return_value = "Answer based on course content"
        mock_rag_system.tool_manager.get_last_sources.return_value = mock_sources
        
        response, sources = mock_rag_system.query("Explain MCP")
        
        assert response == "Answer based on course content"
        assert sources == mock_sources
        
        # Verify sources were reset after retrieval
        mock_rag_system.tool_manager.reset_sources.assert_called_once()

    def test_get_course_analytics(self, mock_rag_system):
        """Test course analytics retrieval"""
        mock_rag_system.vector_store.get_course_count.return_value = 5
        mock_rag_system.vector_store.get_existing_course_titles.return_value = [
            "Course 1", "Course 2", "Course 3", "Course 4", "Course 5"
        ]
        
        analytics = mock_rag_system.get_course_analytics()
        
        assert analytics["total_courses"] == 5
        assert len(analytics["course_titles"]) == 5
        assert "Course 1" in analytics["course_titles"]

    def test_tool_registration(self, mock_rag_system):
        """Test that tools are properly registered"""
        # Verify tools were registered
        mock_rag_system.tool_manager.register_tool.assert_any_call(mock_rag_system.search_tool)
        mock_rag_system.tool_manager.register_tool.assert_any_call(mock_rag_system.outline_tool)


class TestRAGSystemRealIntegration:
    """Integration tests with real components (no mocking)"""
    
    @pytest.fixture
    def real_rag_system(self):
        """Create a real RAG system with temporary storage"""
        temp_dir = tempfile.mkdtemp()
        
        # Create real config
        config = Mock()
        config.ANTHROPIC_API_KEY = "test-key"
        config.ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
        config.CHUNK_SIZE = 800
        config.CHUNK_OVERLAP = 100
        config.MAX_RESULTS = 5
        config.MAX_HISTORY = 2
        config.CHROMA_PATH = temp_dir
        
        with patch('rag_system.AIGenerator') as mock_ai_gen:
            # Mock AI generator to avoid real API calls
            mock_ai_gen.return_value.generate_response.return_value = "Mocked AI response"
            
            rag_system = RAGSystem(config)
            yield rag_system
        
        # Cleanup
        shutil.rmtree(temp_dir)

    def test_real_document_processing_flow(self, real_rag_system, sample_courses, sample_course_chunks):
        """Test real document processing without mocking core components"""
        # Add course metadata and content directly
        for course in sample_courses:
            real_rag_system.vector_store.add_course_metadata(course)
        
        real_rag_system.vector_store.add_course_content(sample_course_chunks)
        
        # Verify data was added
        assert real_rag_system.vector_store.get_course_count() == 2
        assert len(real_rag_system.vector_store.get_existing_course_titles()) == 2
        
        # Test search functionality
        results = real_rag_system.vector_store.search("MCP protocol")
        assert not results.is_empty()

    def test_real_tool_execution(self, real_rag_system, sample_courses, sample_course_chunks):
        """Test real tool execution without mocking tools"""
        # Setup data
        for course in sample_courses:
            real_rag_system.vector_store.add_course_metadata(course)
        
        real_rag_system.vector_store.add_course_content(sample_course_chunks)
        
        # Test search tool execution
        result = real_rag_system.search_tool.execute("MCP protocol")
        assert isinstance(result, str)
        assert "Model Context Protocol" in result
        
        # Test outline tool execution
        result = real_rag_system.outline_tool.execute("MCP")
        assert isinstance(result, str)
        assert "Model Context Protocol (MCP) Course" in result

    def test_real_query_processing_flow(self, real_rag_system, sample_courses, sample_course_chunks):
        """Test real query processing flow (with mocked AI generator)"""
        # Setup data
        for course in sample_courses:
            real_rag_system.vector_store.add_course_metadata(course)
        
        real_rag_system.vector_store.add_course_content(sample_course_chunks)
        
        # Mock AI generator to simulate tool usage
        with patch.object(real_rag_system.ai_generator, 'generate_response') as mock_gen:
            mock_gen.return_value = "AI response about MCP"
            
            response, sources = real_rag_system.query("What is MCP?")
            
            assert response == "AI response about MCP"
            
            # Verify AI generator was called with proper parameters
            mock_gen.assert_called_once()
            call_args = mock_gen.call_args
            
            assert call_args[1]["tools"] is not None
            assert call_args[1]["tool_manager"] is not None
            assert len(call_args[1]["tools"]) == 2  # Search and outline tools

    def test_empty_vector_store_handling(self, real_rag_system):
        """Test handling of queries when vector store is empty"""
        # Don't add any data
        
        # Test search tool with empty store
        result = real_rag_system.search_tool.execute("any query")
        assert "No data available for search" in result
        
        # Test outline tool with empty store
        result = real_rag_system.outline_tool.execute("any course")
        assert "No courses found" in result

    def test_course_filtering_functionality(self, real_rag_system, sample_courses, sample_course_chunks):
        """Test course and lesson filtering in real system"""
        # Setup data
        for course in sample_courses:
            real_rag_system.vector_store.add_course_metadata(course)
        
        real_rag_system.vector_store.add_course_content(sample_course_chunks)
        
        # Test course filtering
        result = real_rag_system.search_tool.execute("programming", course_name="Python")
        assert "Python Programming Fundamentals" in result
        assert "Model Context Protocol" not in result
        
        # Test lesson filtering
        result = real_rag_system.search_tool.execute("basics", lesson_number=1)
        # Should only get lesson 1 content
        assert "lesson 1" in result.lower() or "lesson_number" in str(real_rag_system.search_tool.last_sources)