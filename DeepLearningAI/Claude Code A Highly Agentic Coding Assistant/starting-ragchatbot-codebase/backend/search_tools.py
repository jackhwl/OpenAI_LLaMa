from typing import Dict, Any, Optional, Protocol
from abc import ABC, abstractmethod
from simple_vector_store import SimpleVectorStore, SearchResults


class Tool(ABC):
    """Abstract base class for all tools"""
    
    @abstractmethod
    def get_tool_definition(self) -> Dict[str, Any]:
        """Return Anthropic tool definition for this tool"""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Execute the tool with given parameters"""
        pass


class CourseSearchTool(Tool):
    """Tool for searching course content with semantic course name matching"""
    
    def __init__(self, vector_store: SimpleVectorStore):
        self.store = vector_store
        self.last_sources = []  # Track sources from last search
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Return Anthropic tool definition for this tool"""
        return {
            "name": "search_course_content",
            "description": "Search course materials with smart course name matching and lesson filtering",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string", 
                        "description": "What to search for in the course content"
                    },
                    "course_name": {
                        "type": "string",
                        "description": "Course title (partial matches work, e.g. 'MCP', 'Introduction')"
                    },
                    "lesson_number": {
                        "type": "integer",
                        "description": "Specific lesson number to search within (e.g. 1, 2, 3)"
                    }
                },
                "required": ["query"]
            }
        }
    
    def execute(self, query: str, course_name: Optional[str] = None, lesson_number: Optional[int] = None) -> str:
        """
        Execute the search tool with given parameters.
        
        Args:
            query: What to search for
            course_name: Optional course filter
            lesson_number: Optional lesson filter
            
        Returns:
            Formatted search results or error message
        """
        
        # Use the vector store's unified search interface
        results = self.store.search(
            query=query,
            course_name=course_name,
            lesson_number=lesson_number
        )
        
        # Handle errors
        if results.error:
            return results.error
        
        # Handle empty results
        if results.is_empty():
            filter_info = ""
            if course_name:
                filter_info += f" in course '{course_name}'"
            if lesson_number:
                filter_info += f" in lesson {lesson_number}"
            return f"No relevant content found{filter_info}."
        
        # Format and return results
        return self._format_results(results)
    
    def _format_results(self, results: SearchResults) -> str:
        """Format search results with course and lesson context"""
        formatted = []
        sources = []  # Track sources for the UI with links
        
        for doc, meta in zip(results.documents, results.metadata):
            course_title = meta.get('course_title', 'unknown')
            lesson_num = meta.get('lesson_number')
            
            # Build context header
            header = f"[{course_title}"
            if lesson_num is not None:
                header += f" - Lesson {lesson_num}"
            header += "]"
            
            # Track source for the UI with lesson link
            source_text = course_title
            if lesson_num is not None:
                source_text += f" - Lesson {lesson_num}"
            
            # Get lesson link if available
            lesson_link = None
            if lesson_num is not None:
                lesson_link = self.store.get_lesson_link(course_title, lesson_num)
            
            # Create source object with text and optional link
            source_obj = {
                "text": source_text,
                "link": lesson_link
            }
            sources.append(source_obj)
            
            formatted.append(f"{header}\n{doc}")
        
        # Store sources for retrieval
        self.last_sources = sources
        
        return "\n\n".join(formatted)


class CourseOutlineTool(Tool):
    """Tool for getting complete course outlines with lesson lists"""
    
    def __init__(self, vector_store: SimpleVectorStore):
        self.store = vector_store
        self.last_sources = []  # Track sources from last search
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Return Anthropic tool definition for this tool"""
        return {
            "name": "get_course_outline",
            "description": "Get complete course outline with title, link, and all lessons for a specific course",
            "input_schema": {
                "type": "object",
                "properties": {
                    "course_title": {
                        "type": "string",
                        "description": "Course title or partial title to find (e.g. 'MCP', 'Building Toward Computer', 'Anthropic')"
                    }
                },
                "required": ["course_title"]
            }
        }
    
    def execute(self, course_title: str) -> str:
        """
        Execute the course outline tool to get complete course information.
        
        Args:
            course_title: Full or partial course title to search for
            
        Returns:
            Formatted course outline or error message
        """
        try:
            # Get all course metadata from vector store
            all_courses = self.store.get_all_courses_metadata()
            
            if not all_courses:
                return "No courses found in the system."
            
            # Find matching course using fuzzy matching (case-insensitive substring)
            matching_course = None
            course_title_lower = course_title.lower().strip()
            
            # Try exact match first
            for course in all_courses:
                if course['title'].lower() == course_title_lower:
                    matching_course = course
                    break
            
            # If no exact match, try partial matching
            if not matching_course:
                for course in all_courses:
                    if course_title_lower in course['title'].lower():
                        matching_course = course
                        break
            
            if not matching_course:
                available_courses = [course['title'] for course in all_courses]
                return f"Course '{course_title}' not found. Available courses: {', '.join(available_courses)}"
            
            # Format the course outline
            result = self._format_course_outline(matching_course)
            
            # Track source for the UI with course link
            source_obj = {
                "text": matching_course['title'],
                "link": matching_course.get('course_link')
            }
            self.last_sources = [source_obj]
            
            return result
            
        except Exception as e:
            return f"Error retrieving course outline: {str(e)}"
    
    def _format_course_outline(self, course_data: Dict[str, Any]) -> str:
        """Format course data into a readable outline"""
        lines = []
        
        # Course title
        lines.append(f"Course: {course_data['title']}")
        
        # Course link if available
        if course_data.get('course_link'):
            lines.append(f"Course Link: {course_data['course_link']}")
        
        # Instructor if available
        if course_data.get('instructor'):
            lines.append(f"Instructor: {course_data['instructor']}")
        
        # Lesson count
        lesson_count = course_data.get('lesson_count', len(course_data.get('lessons', [])))
        lines.append(f"Total Lessons: {lesson_count}")
        
        # Lessons list
        lessons = course_data.get('lessons', [])
        if lessons:
            lines.append("\nLessons:")
            for lesson in sorted(lessons, key=lambda x: x.get('lesson_number', 0)):
                lesson_num = lesson.get('lesson_number')
                lesson_title = lesson.get('lesson_title')
                lesson_link = lesson.get('lesson_link')
                
                if lesson_num is not None and lesson_title:
                    lesson_line = f"  {lesson_num}. {lesson_title}"
                    if lesson_link:
                        lesson_line += f" (Link: {lesson_link})"
                    lines.append(lesson_line)
        else:
            lines.append("\nNo lesson details available.")
        
        return "\n".join(lines)


class ToolManager:
    """Manages available tools for the AI"""
    
    def __init__(self):
        self.tools = {}
    
    def register_tool(self, tool: Tool):
        """Register any tool that implements the Tool interface"""
        tool_def = tool.get_tool_definition()
        tool_name = tool_def.get("name")
        if not tool_name:
            raise ValueError("Tool must have a 'name' in its definition")
        self.tools[tool_name] = tool

    
    def get_tool_definitions(self) -> list:
        """Get all tool definitions for Anthropic tool calling"""
        return [tool.get_tool_definition() for tool in self.tools.values()]
    
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        """Execute a tool by name with given parameters"""
        if tool_name not in self.tools:
            return f"Tool '{tool_name}' not found"
        
        return self.tools[tool_name].execute(**kwargs)
    
    def get_last_sources(self) -> list:
        """Get sources from the last search operation"""
        # Check all tools for last_sources attribute
        for tool in self.tools.values():
            if hasattr(tool, 'last_sources') and tool.last_sources:
                return tool.last_sources
        return []

    def reset_sources(self):
        """Reset sources from all tools that track sources"""
        for tool in self.tools.values():
            if hasattr(tool, 'last_sources'):
                tool.last_sources = []