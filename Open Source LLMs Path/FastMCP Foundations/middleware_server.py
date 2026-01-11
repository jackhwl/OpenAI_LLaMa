# middleware_server.py
from __future__ import annotations

import json
import logging
import sys
from typing import Any, Dict

from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext

# ---------------------------------------------------------------------
# Logging to STDERR (safe for stdio) + file
# ---------------------------------------------------------------------
log = logging.getLogger("fastmcp.middleware")
log.setLevel(logging.INFO)
if not log.handlers:
    fh = logging.FileHandler("fastmcp_middleware.log", encoding="utf-8")
    eh = logging.StreamHandler(sys.stderr)  # IMPORTANT: stderr, not stdout
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    fh.setFormatter(fmt); eh.setFormatter(fmt)
    log.addHandler(fh); log.addHandler(eh)

def safe_json(obj: Any) -> str:
    try:
        return json.dumps(obj, default=str, ensure_ascii=False)
    except Exception:
        return f"<non-serializable:{type(obj).__name__}>"

def to_jsonable(obj: Any) -> Any:
    if hasattr(obj, "model_dump"):
        try:
            return obj.model_dump()
        except Exception:
            pass
    if isinstance(obj, (dict, list)):
        return obj
    return {"_type": type(obj).__name__}

def unwrap_toolresult(obj: Any) -> Any:
    for attr in ("result", "data", "value", "content", "output"):
        if hasattr(obj, attr):
            try:
                inner = getattr(obj, attr)
                if hasattr(inner, "model_dump"):
                    return inner.model_dump()
                return inner
            except Exception:
                pass
    if hasattr(obj, "model_dump"):
        try:
            return obj.model_dump()
        except Exception:
            pass
    return obj

def redact_content_parts_for_log(obj: Any, redact_fn):
    """
    For MCP 'content parts' (lists of parts), if a text part's text is JSON,
    parse -> redact -> re-serialize so logs show masked values.
    """
    def get_attr(o, name, default=None):
        return getattr(o, name, default) if not isinstance(o, dict) else o.get(name, default)

    if isinstance(obj, list) and all(
        (hasattr(p, "type") or (isinstance(p, dict) and "type" in p)) for p in obj
    ):
        view = []
        for p in obj:
            ptype = get_attr(p, "type")
            item = {"type": ptype}
            text_val = get_attr(p, "text")
            if isinstance(text_val, str):
                try:
                    parsed = json.loads(text_val)
                    red = redact_fn(parsed) if isinstance(parsed, (dict, list)) else parsed
                    item["text"] = json.dumps(red, ensure_ascii=False)
                except Exception:
                    item["text"] = text_val  # not JSON; log as-is
            else:
                item["preview"] = f"<{type(text_val).__name__}>"
            meta = get_attr(p, "meta")
            if meta:
                item["meta"] = meta
            view.append(item)
        return view
    return obj

class RedactingLoggingMiddleware(Middleware):
    SENSITIVE_KEYS = {
        "password", "api_key", "token", "secret", "authorization",
        "bearer", "access_token", "refresh_token",
    }

    @classmethod
    def _redact(cls, obj: Any) -> Any:
        if isinstance(obj, dict):
            out: Dict[str, Any] = {}
            for k, v in obj.items():
                out[k] = "***MASKED***" if k.lower() in cls.SENSITIVE_KEYS else cls._redact(v)
            return out
        if isinstance(obj, list):
            return [cls._redact(x) for x in obj]
        return obj

    async def on_message(self, context: MiddlewareContext, call_next):
        # ---- inbound ----
        try:
            payload = getattr(context.message, "model_dump", lambda: {})()
            log.info(
                "▶ %s from %s :: %s",
                context.method, context.source, safe_json(self._redact(payload))
            )
        except Exception as e:
            print(f"[middleware] inbound log failed: {e}", file=sys.stderr, flush=True)

        # ---- execute next handler ----
        result = await call_next(context)

        # ---- outbound ----
        try:
            unwrapped = unwrap_toolresult(result)
            prepared = redact_content_parts_for_log(unwrapped, self._redact)
            jsonable = to_jsonable(prepared)
            redacted = self._redact(jsonable) if isinstance(jsonable, (dict, list)) else jsonable
            log.info("◀ %s :: %s", context.method, safe_json(redacted))
        except Exception as e:
            print(f"[middleware] outbound log failed: {e}", file=sys.stderr, flush=True)

        return result

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        tool_name = getattr(getattr(context, "message", None), "name", "<unknown>")
        log.info("⚙ calling tool: %s", tool_name)
        return await call_next(context)

# ---------------------------------------------------------------------
# MCP Server + Sample Tool
# ---------------------------------------------------------------------
mcp = FastMCP("middleware-demo")
mcp.add_middleware(RedactingLoggingMiddleware())

@mcp.tool
async def echo_secret(message: str, password: str):
    """
    Echo a message and include intentionally sensitive-looking fields.
    NOTE: Middleware only redacts these fields in the logs; the client still
    receives the full (unredacted) response.
    """
    print(f"[echo_secret] message={message!r}, password={password!r}",
          file=sys.stderr, flush=True)
    return {"message": message, "password": password, "secret": "TOP_SECRET_VALUE"}

if __name__ == "__main__":
    mcp.run()  # stdio transport





