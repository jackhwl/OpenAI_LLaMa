# btc_price_server.py
from __future__ import annotations

from fastmcp import FastMCP
from typing import Literal, Dict, Any
import os
import time
import requests

from dotenv import load_dotenv, find_dotenv

# Load environment variables from a .env file if present.
# Search from the current working directory upward; if not found, try the script directory.
def _init_env() -> None:
    try:
        dotenv_path = find_dotenv(usecwd=True)
    except Exception:
        dotenv_path = ""
    loaded = False
    if dotenv_path:
        loaded = load_dotenv(dotenv_path)
    if not loaded:
        # Fallback to a .env next to this file (works if MCP changes CWD)
        try:
            import pathlib
            script_env = pathlib.Path(__file__).resolve().parent / ".env"
            if script_env.exists():
                load_dotenv(script_env)
        except Exception:
            pass

_init_env()


mcp = FastMCP("Bitcoin Price MCP (CoinMarketCap)")

VsCurrency = Literal["USD", "EUR", "GBP", "CAD", "AUD", "CHF", "JPY", "INR"]

CMC_QUOTES_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
USER_AGENT = "btc-price-mcp/1.0"
CACHE_TTL_SECONDS = 10

# Simple in-memory cache
_CACHE: Dict[str, Dict[str, Any]] = {}

def _get_cached(key: str) -> dict | None:
    entry = _CACHE.get(key)
    if not entry or (time.time() - entry["ts"] > CACHE_TTL_SECONDS):
        return None
    return entry["data"]

def _set_cached(key: str, data: dict) -> None:
    _CACHE[key] = {"ts": time.time(), "data": data}

def _fetch_cmc_btc_spot(convert: str) -> dict:
    api_key = os.getenv("COINMARKETCAP_API_KEY")
    if not api_key:
        return {"error": "missing_api_key", "details": "Set COINMARKETCAP_API_KEY in your environment."}

    headers = {
        "X-CMC_PRO_API_KEY": api_key,
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    params = {
        "symbol": "BTC",       # or id=1
        "convert": convert,    # e.g., USD
    }
    try:
        resp = requests.get(CMC_QUOTES_URL, headers=headers, params=params, timeout=10)
    except requests.RequestException as e:
        return {"error": f"network_error: {e.__class__.__name__}: {e}"}

    if resp.status_code != 200:
        # helpful for 401/403/429 details
        return {"error": f"http_{resp.status_code}", "details": resp.text[:400]}

    try:
        j = resp.json()
        quote = j["data"]["BTC"]["quote"][convert]
        price = float(quote["price"])
        pct_24h = float(quote.get("percent_change_24h", 0.0))
        ts = quote.get("last_updated")
    except Exception as e:
        return {"error": f"parse_error: {e.__class__.__name__}", "details": str(e)[:400], "body": resp.text[:400]}

    return {
        "symbol": "BTC",
        "vs_currency": convert,
        "price": price,
        "percent_change_24h": pct_24h,
        "last_updated": ts,
        "source": "coinmarketcap",
        "endpoint": "quotes/latest",
        "attribution": "Data from CoinMarketCap",
    }

@mcp.tool(
    name="get_btc_price",
    description="Get the current BTC price (CoinMarketCap) in a target fiat currency."
)
def get_btc_price(vs_currency: VsCurrency = "USD") -> dict:
    """
    Args:
        vs_currency: One of USD, EUR, GBP, CAD, AUD, CHF, JPY, INR (default USD)
    Returns:
        { symbol, vs_currency, price, percent_change_24h, last_updated, source, ... } or { error, ... }
    """
    cur = vs_currency.upper()
    cache_key = f"btc:{cur}"
    hit = _get_cached(cache_key)
    if hit:
        return hit

    out = _fetch_cmc_btc_spot(cur)
    if "error" not in out:
        _set_cached(cache_key, out)
    return out

# Optional resource form
@mcp.resource("price://btc/{vs_currency}")
def btc_price_resource(vs_currency: VsCurrency = "USD") -> dict:
    return get_btc_price(vs_currency)

if __name__ == "__main__":

    mcp.run(transport="stdio")
  
