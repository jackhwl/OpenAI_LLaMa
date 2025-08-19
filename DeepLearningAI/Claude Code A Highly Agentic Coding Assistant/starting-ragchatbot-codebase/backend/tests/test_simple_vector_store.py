import pytest
import tempfile
import shutil
import os
import numpy as np
from simple_vector_store import SimpleVectorStore, SearchResults
from models import Course, Lesson, CourseChunk


class TestSimpleVectorStore:
    """Test the SimpleVectorStore functionality"""
    
    def test_initialization(self):
        """Test vector store initialization"""
        temp_dir = tempfile.mkdtemp()
        try:
            store = SimpleVectorStore(persist_path=temp_dir, max_results=3)
            
            assert store.max_results == 3
            assert store.persist_path == temp_dir
            assert store.course_catalog == []
            assert store.course_content == []
            assert store.course_vectors is None
            assert store.vectorizer_fitted == False
        finally:
            shutil.rmtree(temp_dir)

    def test_add_course_metadata(self, temp_vector_store, sample_courses):
        """Test adding course metadata"""
        course = sample_courses[0]
        temp_vector_store.add_course_metadata(course)
        
        assert len(temp_vector_store.course_catalog) == 1
        catalog_entry = temp_vector_store.course_catalog[0]
        
        assert catalog_entry["title"] == course.title
        assert catalog_entry["instructor"] == course.instructor
        assert catalog_entry["course_link"] == course.course_link
        assert len(catalog_entry["lessons"]) == len(course.lessons)
        assert catalog_entry["lesson_count"] == len(course.lessons)

    def test_add_course_content(self, temp_vector_store, sample_course_chunks):
        """Test adding course content chunks"""
        temp_vector_store.add_course_content(sample_course_chunks)
        
        assert len(temp_vector_store.course_content) == len(sample_course_chunks)
        assert temp_vector_store.vectorizer_fitted == True
        assert temp_vector_store.course_vectors is not None
        
        # Verify content structure
        first_content = temp_vector_store.course_content[0]
        assert "document" in first_content
        assert "metadata" in first_content
        assert "course_title" in first_content["metadata"]
        assert "lesson_number" in first_content["metadata"]
        assert "chunk_index" in first_content["metadata"]

    def test_search_basic_functionality(self, populated_vector_store):
        """Test basic search functionality"""
        results = populated_vector_store.search("MCP protocol")
        
        assert not results.is_empty()
        assert len(results.documents) > 0
        assert len(results.metadata) == len(results.documents)
        assert len(results.distances) == len(results.documents)
        assert results.error is None

    def test_search_with_course_filter(self, populated_vector_store):
        """Test search with course name filter"""
        results = populated_vector_store.search("programming", course_name="Python")
        
        assert not results.is_empty()
        # All results should be from Python course
        for metadata in results.metadata:
            assert "Python" in metadata["course_title"]

    def test_search_with_lesson_filter(self, populated_vector_store):
        """Test search with lesson number filter"""
        results = populated_vector_store.search("Python", lesson_number=1)
        
        assert not results.is_empty()
        # All results should be from lesson 1
        for metadata in results.metadata:
            assert metadata["lesson_number"] == 1

    def test_search_with_both_filters(self, populated_vector_store):
        """Test search with both course and lesson filters"""
        results = populated_vector_store.search(
            "programming", 
            course_name="Python", 
            lesson_number=1
        )
        
        for metadata in results.metadata:
            assert "Python" in metadata["course_title"]
            assert metadata["lesson_number"] == 1

    def test_search_no_data(self, temp_vector_store):
        """Test search when no data is available"""
        results = temp_vector_store.search("any query")
        
        assert results.is_empty()
        assert results.error == "No data available for search"

    def test_search_no_matches(self, populated_vector_store):
        """Test search with very specific query that should have no matches"""
        results = populated_vector_store.search("xyzabcnotfound")
        
        # Should return empty results due to low similarity threshold
        assert results.is_empty() or len(results.documents) == 0

    def test_search_limit_parameter(self, populated_vector_store):
        """Test search with custom limit"""
        results = populated_vector_store.search("programming", limit=2)
        
        assert len(results.documents) <= 2

    def test_search_diversification(self, temp_vector_store):
        """Test that search results are diversified across lessons"""
        # Create multiple chunks from the same lesson
        chunks = []
        for i in range(10):
            chunks.append(CourseChunk(
                course_title="Test Course",
                lesson_number=1,
                chunk_index=i,
                content=f"Programming content chunk {i} about Python and coding"
            ))
        
        # Add one chunk from different lesson
        chunks.append(CourseChunk(
            course_title="Test Course",
            lesson_number=2,
            chunk_index=0,
            content="Different lesson about advanced programming concepts"
        ))
        
        temp_vector_store.add_course_content(chunks)
        results = temp_vector_store.search("programming", limit=5)
        
        # Should have results from both lessons
        lesson_numbers = [meta["lesson_number"] for meta in results.metadata]
        assert len(set(lesson_numbers)) > 1  # Multiple different lessons

    def test_get_existing_course_titles(self, populated_vector_store):
        """Test getting existing course titles"""
        titles = populated_vector_store.get_existing_course_titles()
        
        assert len(titles) == 2
        assert "Model Context Protocol (MCP) Course" in titles
        assert "Python Programming Fundamentals" in titles

    def test_get_course_count(self, populated_vector_store):
        """Test getting course count"""
        count = populated_vector_store.get_course_count()
        assert count == 2

    def test_get_all_courses_metadata(self, populated_vector_store):
        """Test getting all courses metadata"""
        metadata = populated_vector_store.get_all_courses_metadata()
        
        assert len(metadata) == 2
        assert all("title" in course for course in metadata)
        assert all("lessons" in course for course in metadata)

    def test_get_course_link(self, populated_vector_store):
        """Test getting course link"""
        link = populated_vector_store.get_course_link("Model Context Protocol (MCP) Course")
        assert link == "https://example.com/course1"
        
        # Test non-existent course
        link = populated_vector_store.get_course_link("Non-existent Course")
        assert link is None

    def test_get_lesson_link(self, populated_vector_store):
        """Test getting lesson link"""
        link = populated_vector_store.get_lesson_link("Model Context Protocol (MCP) Course", 1)
        assert link == "https://example.com/lesson1"
        
        # Test non-existent lesson
        link = populated_vector_store.get_lesson_link("Model Context Protocol (MCP) Course", 99)
        assert link is None

    def test_clear_all_data(self, populated_vector_store):
        """Test clearing all data"""
        # Verify data exists
        assert len(populated_vector_store.course_catalog) > 0
        assert len(populated_vector_store.course_content) > 0
        
        # Clear data
        populated_vector_store.clear_all_data()
        
        assert len(populated_vector_store.course_catalog) == 0
        assert len(populated_vector_store.course_content) == 0
        assert populated_vector_store.course_vectors is None
        assert populated_vector_store.vectorizer_fitted == False

    def test_persistence_save_and_load(self, sample_courses, sample_course_chunks):
        """Test data persistence (save and load)"""
        temp_dir = tempfile.mkdtemp()
        try:
            # Create store and add data
            store1 = SimpleVectorStore(persist_path=temp_dir)
            store1.add_course_metadata(sample_courses[0])
            store1.add_course_content(sample_course_chunks[:2])
            
            # Create new store with same path (should load data)
            store2 = SimpleVectorStore(persist_path=temp_dir)
            
            # Verify data was loaded
            assert len(store2.course_catalog) == 1
            assert len(store2.course_content) == 2
            assert store2.vectorizer_fitted == True
            assert store2.course_vectors is not None
            
            # Test search works on loaded data
            results = store2.search("MCP")
            assert not results.is_empty()
            
        finally:
            shutil.rmtree(temp_dir)

    def test_duplicate_course_handling(self, temp_vector_store, sample_courses):
        """Test handling of duplicate course additions"""
        course = sample_courses[0]
        
        # Add course twice
        temp_vector_store.add_course_metadata(course)
        temp_vector_store.add_course_metadata(course)
        
        # Should have only one course in catalog
        assert len(temp_vector_store.course_catalog) == 1

    def test_search_results_structure(self, populated_vector_store):
        """Test that search results have correct structure"""
        results = populated_vector_store.search("MCP")
        
        # Test SearchResults methods
        assert hasattr(results, 'documents')
        assert hasattr(results, 'metadata')
        assert hasattr(results, 'distances')
        assert hasattr(results, 'error')
        assert hasattr(results, 'is_empty')
        
        # Test data types
        assert isinstance(results.documents, list)
        assert isinstance(results.metadata, list)
        assert isinstance(results.distances, list)
        
        # Test that all lists have same length
        assert len(results.documents) == len(results.metadata)
        assert len(results.metadata) == len(results.distances)

    def test_empty_search_results_factory(self):
        """Test SearchResults.empty factory method"""
        empty_results = SearchResults.empty("Test error message")
        
        assert empty_results.is_empty()
        assert empty_results.error == "Test error message"
        assert len(empty_results.documents) == 0
        assert len(empty_results.metadata) == 0
        assert len(empty_results.distances) == 0

    def test_search_similarity_threshold(self, populated_vector_store):
        """Test that very low similarity results are filtered out"""
        # Search for something completely unrelated
        results = populated_vector_store.search("quantum physics nuclear fusion")
        
        # Should either be empty or have very few results
        # (depending on how the similarity threshold is set)
        if not results.is_empty():
            # All remaining results should have reasonable similarity
            for distance in results.distances:
                assert distance < 0.99  # Very high distance means very low similarity

    def test_add_empty_course_content(self, temp_vector_store):
        """Test adding empty course content"""
        temp_vector_store.add_course_content([])
        
        assert len(temp_vector_store.course_content) == 0
        assert temp_vector_store.vectorizer_fitted == False