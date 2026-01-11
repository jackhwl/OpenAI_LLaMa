# mcp_docs_server.py
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Literal
from datetime import datetime, timezone

from fastmcp import FastMCP

mcp = FastMCP("Docs & KB MCP")

# -----------------------------------------------------------------------------
# Simple in-memory stores for demo
# -----------------------------------------------------------------------------
@dataclass
class Document:
    uri: str           # e.g., doc://project/plan
    title: str
    body: str
    tags: List[str]
    space: Literal["project", "helpdesk"]
    key: str           # slug or id
    last_updated: str  # ISO8601

# project docs by slug
PROJECT_DOCS: Dict[str, Document] = {}
# helpdesk articles by id (string for simplicity)
HELP_ARTICLES: Dict[str, Document] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mk_project_uri(slug: str) -> str:
    return f"doc://project/{slug}"


def _mk_help_uri(aid: str) -> str:
    return f"help://article/{aid}"


# Seed a couple of examples
PROJECT_DOCS["plan"] = Document(
    uri=_mk_project_uri("plan"),
    title="Project Plan",
    body="## Objectives\n- Ship MVP in 4 weeks\n- Define success metrics\n\n## Milestones\n1. Spec\n2. Build\n3. Test\n4. Launch",
    tags=["project", "plan", "mvp"],
    space="project",
    key="plan",
    last_updated=_now_iso(),
)

HELP_ARTICLES["123"] = Document(
    uri=_mk_help_uri("123"),
    title="How to Reset Your Password",
    body="1) Click 'Forgot Password'\n2) Check your email\n3) Follow the link to reset",
    tags=["help", "password", "account"],
    space="helpdesk",
    key="123",
    last_updated=_now_iso(),
)

# -----------------------------------------------------------------------------
# Resources (URI-addressable)
# -----------------------------------------------------------------------------

# Project documents: doc://project/{slug}
@mcp.resource("doc://project/{slug}")
def get_project_doc(slug: str) -> dict:
    """
    Fetch a project document by slug as a resource.
    Returns a JSON-like structure with title, body, tags, last_updated, and uri.
    """
    doc = PROJECT_DOCS.get(slug)
    if not doc:
        return {"error": "not_found", "details": f"project doc '{slug}' not found"}
    return asdict(doc)


# Helpdesk articles: help://article/{aid}
@mcp.resource("help://article/{aid}")
def get_help_article(aid: str) -> dict:
    """
    Fetch a helpdesk article by id as a resource.
    """
    doc = HELP_ARTICLES.get(aid)
    if not doc:
        return {"error": "not_found", "details": f"help article '{aid}' not found"}
    return asdict(doc)


# -----------------------------------------------------------------------------
# Tools (manage content & discover resources)
# -----------------------------------------------------------------------------

@mcp.tool(
    name="list_resources",
    description="List available document URIs for browsing."
)
def list_resources(kind: Literal["all", "project", "helpdesk"] = "all") -> dict:
    """
    Returns a list of URIs (and minimal metadata) to discover what's available.
    """
    items = []

    def add_entry(d: Document):
        items.append({
            "uri": d.uri,
            "title": d.title,
            "tags": d.tags,
            "last_updated": d.last_updated,
        })

    if kind in ("all", "project"):
        for d in PROJECT_DOCS.values():
            add_entry(d)

    if kind in ("all", "helpdesk"):
        for d in HELP_ARTICLES.values():
            add_entry(d)

    return {"count": len(items), "items": items}


@mcp.tool(
    name="upsert_project_doc",
    description="Create or update a project doc at doc://project/{slug}."
)
def upsert_project_doc(slug: str, title: str, body: str, tags: Optional[List[str]] = None) -> dict:
    """
    Create or update a project document. Returns the stored document record.
    """
    tags = tags or []
    uri = _mk_project_uri(slug)
    doc = Document(
        uri=uri,
        title=title,
        body=body,
        tags=tags,
        space="project",
        key=slug,
        last_updated=_now_iso(),
    )
    PROJECT_DOCS[slug] = doc
    return {"status": "ok", "document": asdict(doc)}


@mcp.tool(
    name="upsert_help_article",
    description="Create or update a help article at help://article/{id}."
)
def upsert_help_article(aid: str, title: str, body: str, tags: Optional[List[str]] = None) -> dict:
    """
    Create or update a help article. Returns the stored document record.
    """
    tags = tags or []
    uri = _mk_help_uri(aid)
    doc = Document(
        uri=uri,
        title=title,
        body=body,
        tags=tags,
        space="helpdesk",
        key=aid,
        last_updated=_now_iso(),
    )
    HELP_ARTICLES[aid] = doc
    return {"status": "ok", "document": asdict(doc)}


# -----------------------------------------------------------------------------
# Server entrypoint
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Best for GitHub Copilot MCP (Developer Mode)
    mcp.run(transport="stdio")
    # Or, to expose HTTP (optional):
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=8787)
