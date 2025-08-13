# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack Retrieval-Augmented Generation (RAG) system for course materials built with FastAPI (backend) and vanilla HTML/CSS/JavaScript (frontend). The system allows users to query course content and receive AI-powered responses using semantic search.

## Development Commands

### Running the Application
```bash
# Quick start (from root directory)
chmod +x run.sh
./run.sh

# Manual start (from backend directory)
cd backend && uv run uvicorn app:app --reload --port 8000
```

### Package Management
```bash
# Install dependencies
uv sync

# Add new dependency
uv add <package-name>
```

### Environment Setup
Create `.env` file in root with:
```
ANTHROPIC_API_KEY=your_key_here
```

## Architecture

### Backend Structure (`backend/`)
- **`app.py`**: FastAPI application with CORS, static file serving, and API endpoints
- **`rag_system.py`**: Main orchestrator coordinating all RAG components
- **`config.py`**: Configuration dataclass with environment variable loading
- **`models.py`**: Pydantic models for Course, Lesson, and CourseChunk
- **`document_processor.py`**: Text processing and chunking with configurable overlap
- **`vector_store.py`**: ChromaDB integration with sentence-transformers embeddings
- **`ai_generator.py`**: Anthropic Claude API integration for response generation
- **`session_manager.py`**: Chat session and conversation history management
- **`search_tools.py`**: Tool-based search system for RAG queries

### Frontend Structure (`frontend/`)
- **`index.html`**: Single-page application with chat interface
- **`script.js`**: API communication and DOM manipulation
- **`style.css`**: Modern responsive styling

### Data Flow
1. Documents in `docs/` are processed into chunks on startup
2. User queries trigger vector similarity search via ChromaDB
3. Retrieved chunks provide context to Claude for response generation
4. Session manager maintains conversation history for context

### Key Configuration
- **Chunk size**: 800 characters with 100 character overlap
- **Embedding model**: all-MiniLM-L6-v2 (sentence-transformers)
- **AI model**: claude-sonnet-4-20250514
- **Vector store**: ChromaDB with local persistence (`./chroma_db`)
- **Max search results**: 5 chunks per query
- **Conversation history**: 2 messages retained

### API Endpoints
- `POST /api/query`: Process user queries with RAG
- `GET /api/courses`: Retrieve course analytics
- `GET /`: Serves frontend static files

## Development Notes

- The application automatically loads documents from `docs/` on startup
- Static files are served with no-cache headers for development
- CORS is configured for all origins during development
- ChromaDB warnings are suppressed in the FastAPI startup
- always use uv to run the server do not use pip directly
- make sure to use uv to manage all dependecies
- use uv to run Python files