# translate_plugin.py
from __future__ import annotations
from typing import Dict, Any, Literal
from fastmcp import FastMCP

Lang = Literal["en", "es", "fr", "de", "it"]

_DICT = {
    ("hello", "es"): "hola",
    ("hello", "fr"): "bonjour",
    ("hello", "de"): "hallo",
    ("hello", "it"): "ciao",
}

def _fake_translate(text: str, target: Lang) -> str:
    key = (text.strip().lower(), target)
    return _DICT.get(key, f"[{target}] {text}")

def register(server: FastMCP) -> None:
    """Attach translation tools to the given FastMCP server."""

    @server.tool
    def translate_text(text: str, target_lang: Lang = "en") -> Dict[str, Any]:
        """Translate text to target_lang (demo stub)."""
        if target_lang not in ("en", "es", "fr", "de", "it"):
            raise ValueError("Unsupported target_lang. Use: en, es, fr, de, it.")
        return {"input": text, "target_lang": target_lang, "translated": _fake_translate(text, target_lang)}
