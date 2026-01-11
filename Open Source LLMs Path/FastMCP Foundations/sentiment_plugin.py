# sentiment_plugin.py
from __future__ import annotations
from typing import Dict, Any
from fastmcp import FastMCP

def register(server: FastMCP) -> None:
    """Attach sentiment tools to the given FastMCP server."""

    @server.tool
    def analyze_sentiment(text: str) -> Dict[str, Any]:
        """Analyze text sentiment (simple rule-based demo)."""
        t = text.lower()
        pos = any(w in t for w in ["love", "great", "awesome", "excellent", "amazing"])
        neg = any(w in t for w in ["hate", "bad", "terrible", "awful", "crash", "bug"])
        if pos and neg:
            label = "mixed"
        elif pos:
            label = "positive"
        elif neg:
            label = "negative"
        else:
            label = "neutral"
        return {"sentiment": label, "input": text}

