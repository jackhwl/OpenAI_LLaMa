"""
简化的Text2SQL框架
基于RAGFlow方案实现的Text2SQL框架
"""

__version__ = "1.0.0"
__author__ = "RAG Team"

from .knowledge_base import SimpleKnowledgeBase
from .sql_generator import SimpleSQLGenerator
from .text2sql_agent import SimpleText2SQLAgent

__all__ = [
    "SimpleKnowledgeBase",
    "SimpleSQLGenerator", 
    "SimpleText2SQLAgent"
] 