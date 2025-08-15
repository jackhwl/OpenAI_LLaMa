import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from models import Course, CourseChunk
import json
import os
import pickle

@dataclass
class SearchResults:
    """Container for search results with metadata"""
    documents: List[str]
    metadata: List[Dict[str, Any]]
    distances: List[float]
    error: Optional[str] = None
    
    @classmethod
    def empty(cls, error_msg: str) -> 'SearchResults':
        """Create empty results with error message"""
        return cls(documents=[], metadata=[], distances=[], error=error_msg)
    
    def is_empty(self) -> bool:
        """Check if results are empty"""
        return len(self.documents) == 0

class SimpleVectorStore:
    """Simple vector storage using TF-IDF and cosine similarity"""
    
    def __init__(self, persist_path: str = "./simple_vector_store", max_results: int = 5):
        self.max_results = max_results
        self.persist_path = persist_path
        
        # Initialize vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Storage for course catalog and content
        self.course_catalog = []  # List of course metadata
        self.course_content = []  # List of content chunks
        self.course_vectors = None  # TF-IDF vectors for content
        self.vectorizer_fitted = False
        
        # Try to load existing data
        self._load_data()
    
    def _save_data(self):
        """Save the vector store data to disk"""
        os.makedirs(self.persist_path, exist_ok=True)
        
        data = {
            'course_catalog': self.course_catalog,
            'course_content': self.course_content,
            'vectorizer_fitted': self.vectorizer_fitted
        }
        
        with open(os.path.join(self.persist_path, 'data.pkl'), 'wb') as f:
            pickle.dump(data, f)
        
        if self.vectorizer_fitted:
            with open(os.path.join(self.persist_path, 'vectorizer.pkl'), 'wb') as f:
                pickle.dump(self.vectorizer, f)
            
            if self.course_vectors is not None:
                np.save(os.path.join(self.persist_path, 'vectors.npy'), self.course_vectors)
    
    def _load_data(self):
        """Load existing vector store data from disk"""
        try:
            if os.path.exists(os.path.join(self.persist_path, 'data.pkl')):
                with open(os.path.join(self.persist_path, 'data.pkl'), 'rb') as f:
                    data = pickle.load(f)
                
                self.course_catalog = data.get('course_catalog', [])
                self.course_content = data.get('course_content', [])
                self.vectorizer_fitted = data.get('vectorizer_fitted', False)
                
                if self.vectorizer_fitted:
                    with open(os.path.join(self.persist_path, 'vectorizer.pkl'), 'rb') as f:
                        self.vectorizer = pickle.load(f)
                    
                    if os.path.exists(os.path.join(self.persist_path, 'vectors.npy')):
                        self.course_vectors = np.load(os.path.join(self.persist_path, 'vectors.npy'), allow_pickle=True)
        except Exception as e:
            print(f"Error loading vector store data: {e}")
    
    def search(self, 
               query: str,
               course_name: Optional[str] = None,
               lesson_number: Optional[int] = None,
               limit: Optional[int] = None) -> SearchResults:
        """
        Main search interface that handles course resolution and content search.
        """
        if not self.course_content or not self.vectorizer_fitted:
            return SearchResults.empty("No data available for search")
        
        try:
            # Vectorize the query
            query_vector = self.vectorizer.transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vector, self.course_vectors)[0]
            
            # Get all results sorted by similarity
            all_indices = np.argsort(similarities)[::-1]
            search_limit = limit if limit is not None else self.max_results
            
            # Diversify results across lessons to avoid lesson clustering
            filtered_results = []
            lesson_counts = {}  # Track how many results per lesson
            max_per_lesson = max(1, search_limit // 3)  # Allow max 1-2 results per lesson initially
            
            for idx in all_indices:
                if len(filtered_results) >= search_limit:
                    break
                if similarities[idx] < 0.01:  # Skip very low similarity results
                    continue
                    
                content_item = self.course_content[idx]
                
                # Apply filters
                if course_name and course_name.lower() not in content_item['metadata']['course_title'].lower():
                    continue
                if lesson_number is not None and content_item['metadata']['lesson_number'] != lesson_number:
                    continue
                
                # Check lesson diversity
                lesson_key = f"{content_item['metadata']['course_title']}-{content_item['metadata']['lesson_number']}"
                current_count = lesson_counts.get(lesson_key, 0)
                
                # Allow more results from same lesson if we haven't filled our quota yet
                if current_count < max_per_lesson or len(filtered_results) < search_limit // 2:
                    lesson_counts[lesson_key] = current_count + 1
                    filtered_results.append({
                        'document': content_item['document'],
                        'metadata': content_item['metadata'],
                        'distance': 1 - similarities[idx]  # Convert similarity to distance
                    })
            
            # If we still have space and haven't found enough diverse results, 
            # fill remaining spots with best remaining matches
            if len(filtered_results) < search_limit:
                for idx in all_indices:
                    if len(filtered_results) >= search_limit:
                        break
                    if similarities[idx] < 0.01:
                        continue
                        
                    content_item = self.course_content[idx]
                    
                    # Apply filters
                    if course_name and course_name.lower() not in content_item['metadata']['course_title'].lower():
                        continue
                    if lesson_number is not None and content_item['metadata']['lesson_number'] != lesson_number:
                        continue
                    
                    # Check if we already have this result
                    result_exists = any(
                        r['document'] == content_item['document'] 
                        for r in filtered_results
                    )
                    
                    if not result_exists:
                        filtered_results.append({
                            'document': content_item['document'],
                            'metadata': content_item['metadata'],
                            'distance': 1 - similarities[idx]
                        })
            
            return SearchResults(
                documents=[r['document'] for r in filtered_results],
                metadata=[r['metadata'] for r in filtered_results],
                distances=[r['distance'] for r in filtered_results]
            )
            
        except Exception as e:
            return SearchResults.empty(f"Search error: {str(e)}")
    
    def add_course_metadata(self, course: Course):
        """Add course information to the catalog"""
        lessons_metadata = []
        for lesson in course.lessons:
            lessons_metadata.append({
                "lesson_number": lesson.lesson_number,
                "lesson_title": lesson.title,
                "lesson_link": lesson.lesson_link
            })
        
        course_meta = {
            "title": course.title,
            "instructor": course.instructor,
            "course_link": course.course_link,
            "lessons": lessons_metadata,
            "lesson_count": len(course.lessons)
        }
        
        # Remove existing course if it exists
        self.course_catalog = [c for c in self.course_catalog if c['title'] != course.title]
        self.course_catalog.append(course_meta)
        
        self._save_data()
    
    def add_course_content(self, chunks: List[CourseChunk]):
        """Add course content chunks to the vector store"""
        if not chunks:
            return
        
        # Add new content
        for chunk in chunks:
            content_item = {
                'document': chunk.content,
                'metadata': {
                    "course_title": chunk.course_title,
                    "lesson_number": chunk.lesson_number,
                    "chunk_index": chunk.chunk_index
                }
            }
            self.course_content.append(content_item)
        
        # Refit vectorizer with all content
        documents = [item['document'] for item in self.course_content]
        self.course_vectors = self.vectorizer.fit_transform(documents)
        self.vectorizer_fitted = True
        
        self._save_data()
    
    def clear_all_data(self):
        """Clear all data"""
        self.course_catalog = []
        self.course_content = []
        self.course_vectors = None
        self.vectorizer_fitted = False
        
        # Remove persisted data
        import shutil
        if os.path.exists(self.persist_path):
            shutil.rmtree(self.persist_path)
    
    def get_existing_course_titles(self) -> List[str]:
        """Get all existing course titles from the vector store"""
        return [course['title'] for course in self.course_catalog]
    
    def get_course_count(self) -> int:
        """Get the total number of courses in the vector store"""
        return len(self.course_catalog)
    
    def get_all_courses_metadata(self) -> List[Dict[str, Any]]:
        """Get metadata for all courses in the vector store"""
        return self.course_catalog.copy()
    
    def get_course_link(self, course_title: str) -> Optional[str]:
        """Get course link for a given course title"""
        for course in self.course_catalog:
            if course['title'] == course_title:
                return course.get('course_link')
        return None
    
    def get_lesson_link(self, course_title: str, lesson_number: int) -> Optional[str]:
        """Get lesson link for a given course title and lesson number"""
        for course in self.course_catalog:
            if course['title'] == course_title:
                for lesson in course.get('lessons', []):
                    if lesson.get('lesson_number') == lesson_number:
                        return lesson.get('lesson_link')
        return None