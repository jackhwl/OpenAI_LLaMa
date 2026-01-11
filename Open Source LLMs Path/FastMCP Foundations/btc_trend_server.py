from __future__ import annotations

import os
import time
import random
from typing import Dict, Any, List, Literal

import requests
from fastmcp import FastMCP
from dotenv import load_dotenv, find_dotenv


# ------------------------------------------------------------
# Env init (mirror btc_price_server pattern)
# ------------------------------------------------------------
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


mcp = FastMCP("BTC Trend MCP (SMA Signal)")

VsCurrency = Literal["USD", "EUR", "GBP", "CAD", "AUD", "CHF", "JPY", "INR"]

CMC_QUOTES_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
USER_AGENT = "btc-trend-mcp/1.0"
CACHE_TTL_SECONDS = 10

# Simple in-memory price cache and history per currency
_CACHE: Dict[str, Dict[str, Any]] = {}
_HISTORY: Dict[str, List[Dict[str, float]]] = {}  # key: vs_currency, value: list of {ts, price}
_HISTORY_MAX = 1000
_LAST_SPOT: Dict[str, Dict[str, Any]] = {}  # last fetched spot by vs_currency


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
        "symbol": "BTC",
        "convert": convert,
    }
    try:
        resp = requests.get(CMC_QUOTES_URL, headers=headers, params=params, timeout=10)
    except requests.RequestException as e:
        return {"error": f"network_error: {e.__class__.__name__}: {e}"}

    if resp.status_code != 200:
        return {"error": f"http_{resp.status_code}", "details": resp.text[:400]}

    try:
        j = resp.json()
        quote = j["data"]["BTC"]["quote"][convert]
        price = float(quote["price"])
        pct_24h = float(quote.get("percent_change_24h", 0.0))
        ts = quote.get("last_updated")
    except Exception as e:
        return {
            "error": f"parse_error: {e.__class__.__name__}",
            "details": str(e)[:400],
            "body": resp.text[:400],
        }

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
    name="fetch_btc_spot",
    description=(
        "Fetch the current BTC spot price (CoinMarketCap) and update in-memory history. "
        "Call this first in a chain before computing trend."
    ),
)
def fetch_btc_spot(vs_currency: VsCurrency = "USD") -> dict:
    """
    Fetch BTC spot price in the specified fiat currency, cache it briefly, and append
    the price to the in-memory history for subsequent trend calculations.

    Returns the spot payload or an error dict.
    """
    vs = vs_currency.upper()

    # Use small cache to avoid hitting API too often
    cache_key = f"btc:{vs}"
    hit = _get_cached(cache_key)
    if hit is None:
        spot = _fetch_cmc_btc_spot(vs)
        if "error" in spot:
            return spot
        _set_cached(cache_key, spot)
    else:
        spot = hit

    # Side effects for chaining: remember and extend history
    try:
        price = float(spot["price"])
    except Exception:
        return {"error": "invalid_spot_payload", "details": "Missing price from spot response."}

    _append_history(vs, price)
    _LAST_SPOT[vs] = spot
    return spot


def _append_history(vs: str, price: float, ts: float | None = None) -> None:
    ts = ts or time.time()
    hist = _HISTORY.setdefault(vs, [])
    hist.append({"ts": ts, "price": float(price)})
    if len(hist) > _HISTORY_MAX:
        del hist[: len(hist) - _HISTORY_MAX]


def _ensure_history_for_windows(
    vs: str,
    target_points: int,
    current_price: float,
    pct_24h_bias: float,
    simulate_if_needed: bool = True,
) -> int:
    """Ensure we have at least target_points in history for vs.

    Returns the number of synthetic points added (0 if none).
    Simulation uses a mild random walk around current_price, biased by pct_24h_bias.
    """
    hist = _HISTORY.setdefault(vs, [])
    have = len(hist)
    if have >= target_points or not simulate_if_needed:
        return 0

    to_add = target_points - have
    # Convert 24h pct to per-minute drift approximation
    # drift_per_minute ~ (1 + pct_24h/100) ** (1/1440) - 1
    try:
        drift_per_min = (1.0 + pct_24h_bias / 100.0) ** (1.0 / 1440.0) - 1.0
    except Exception:
        drift_per_min = 0.0

    # Use small volatility: e.g., 5 bps stddev per synthetic step
    vol_bps = 5.0  # basis points
    vol = vol_bps / 10000.0

    # Start from the earliest known price or current
    base_price = hist[0]["price"] if hist else current_price
    # Generate older points back in time so ordering remains chronological
    synthetic: List[Dict[str, float]] = []
    now = time.time()
    for i in range(to_add, 0, -1):
        # time i minutes ago
        t = now - i * 60
        # random shock around drift
        shock = random.gauss(mu=drift_per_min, sigma=vol)
        base_price *= (1.0 + shock)
        synthetic.append({"ts": t, "price": base_price})

    # Prepend synthetic so history remains chronological
    _HISTORY[vs] = synthetic + hist
    # Trim to max
    if len(_HISTORY[vs]) > _HISTORY_MAX:
        del _HISTORY[vs][: len(_HISTORY[vs]) - _HISTORY_MAX]
    return to_add


def _sma(values: List[float], window: int) -> float:
    if window <= 0 or window > len(values):
        raise ValueError("window must be in 1..len(values)")
    return float(sum(values[-window:]) / window)


def _signal_from_sma(short_sma: float, long_sma: float, threshold_bps: float) -> dict:
    if long_sma <= 0:
        return {"signal": "neutral", "ratio_bps": 0.0, "rationale": "Invalid long SMA"}
    ratio = (short_sma - long_sma) / long_sma
    ratio_bps = round(ratio * 10000.0, 2)
    thr = threshold_bps
    if ratio_bps > thr:
        sig = "bullish"
    elif ratio_bps < -thr:
        sig = "bearish"
    else:
        sig = "neutral"
    rationale = (
        f"short SMA {short_sma:.2f} vs long SMA {long_sma:.2f}; "
        f"spread {ratio_bps:.2f} bps (threshold ±{thr:.2f} bps)"
    )
    return {"signal": sig, "ratio_bps": ratio_bps, "rationale": rationale}


@mcp.tool(
    name="compute_btc_trend_signal",
    description=(
        "Compute BTC SMA trend from in-memory price history. "
        "Chain by calling fetch_btc_spot first to update history with the latest price."
    ),
)
def compute_btc_trend_signal(
    vs_currency: VsCurrency = "USD",
    lookback_minutes: int = 60,
    short_window: int = 5,
    long_window: int = 20,
    neutral_threshold_bps: float = 25.0,
    simulate_if_needed: bool = True,
) -> dict:
    """
    Compute a simple SMA-based trend signal for BTC using already-fetched price history.

    Args:
        vs_currency: Target fiat (USD, EUR, GBP, CAD, AUD, CHF, JPY, INR)
        lookback_minutes: Desired recent window (min 5, max 1440)
        short_window: Short SMA window (points)
        long_window: Long SMA window (points, must be > short_window)
        neutral_threshold_bps: Band around 0 for which signal is neutral (basis points)
        simulate_if_needed: If true, backfill synthetic prices when history is short

    Returns:
        {
          symbol, vs_currency, price, last_updated,
          sma_short, sma_long, signal, ratio_bps, threshold_bps,
          points_used, source, attribution, note?
        } or { error, ... }
    """
    if short_window <= 0 or long_window <= 0:
        return {"error": "invalid_window", "details": "Windows must be positive"}
    if short_window >= long_window:
        return {"error": "invalid_window_order", "details": "short_window must be < long_window"}
    lookback_minutes = max(5, min(int(lookback_minutes), 1440))

    vs = vs_currency.upper()

    # Require that fetch_btc_spot be called first so we have the most recent spot
    spot = _LAST_SPOT.get(vs)
    if not spot:
        return {
            "error": "missing_spot",
            "details": "No recent spot price in memory. Call fetch_btc_spot first, then compute_btc_trend_signal.",
        }

    try:
        price = float(spot["price"])  # last fetched current price
    except Exception:
        return {"error": "invalid_spot_payload", "details": "Missing price from stored spot response."}
    pct_24h = float(spot.get("percent_change_24h", 0.0))

    # Step 3: ensure we have enough points in the lookback and windows
    # We treat each point as ~1-minute granularity for simplicity
    target_points = max(long_window, min(lookback_minutes, _HISTORY_MAX))
    added = _ensure_history_for_windows(vs, target_points, price, pct_24h, simulate_if_needed)

    # Step 4: take the last target_points within the lookback window
    hist = _HISTORY.get(vs, [])
    now = time.time()
    cutoff_ts = now - lookback_minutes * 60
    recent = [p for p in hist if p["ts"] >= cutoff_ts]
    if len(recent) < long_window:
        return {
            "error": "insufficient_history",
            "details": f"Need at least {long_window} points, have {len(recent)}. Set simulate_if_needed=true or wait to accumulate.",
        }

    prices = [p["price"] for p in recent]

    try:
        sma_short = _sma(prices, short_window)
        sma_long = _sma(prices, long_window)
    except ValueError as e:
        return {"error": "sma_error", "details": str(e)}

    sig = _signal_from_sma(sma_short, sma_long, neutral_threshold_bps)

    out = {
        "symbol": "BTC",
        "vs_currency": vs,
        "price": price,
        "last_updated": spot.get("last_updated"),
        "sma_short": round(sma_short, 2),
        "sma_long": round(sma_long, 2),
        "signal": sig["signal"],
        "ratio_bps": sig["ratio_bps"],
        "threshold_bps": float(neutral_threshold_bps),
        "points_used": len(prices),
        "source": spot.get("source", "coinmarketcap"),
        "attribution": spot.get("attribution", "Data from CoinMarketCap"),
        "endpoint": spot.get("endpoint", "quotes/latest"),
        "note": f"simulated {added} synthetic points to fill history" if added > 0 else "",
    }
    return out


# Backward-compatible convenience wrapper that chains the two steps internally
@mcp.tool(
    name="get_btc_trend_signal",
    description=(
        "Convenience wrapper: fetch latest BTC spot and then compute the SMA trend signal. "
        "For explicit chaining, call fetch_btc_spot then compute_btc_trend_signal."
    ),
)
def get_btc_trend_signal(
    vs_currency: VsCurrency = "USD",
    lookback_minutes: int = 60,
    short_window: int = 5,
    long_window: int = 20,
    neutral_threshold_bps: float = 25.0,
    simulate_if_needed: bool = True,
) -> dict:
    # 1) Fetch and append to history
    spot = fetch_btc_spot(vs_currency=vs_currency)
    if "error" in spot:
        return spot
    # 2) Compute using the updated history
    return compute_btc_trend_signal(
        vs_currency=vs_currency,
        lookback_minutes=lookback_minutes,
        short_window=short_window,
        long_window=long_window,
        neutral_threshold_bps=neutral_threshold_bps,
        simulate_if_needed=simulate_if_needed,
    )


@mcp.resource("trend://btc/{vs_currency}")
def btc_trend_resource(
    vs_currency: VsCurrency = "USD",
) -> dict:
    # Provide a convenient resource wrapper using defaults (runs the full chain)
    return get_btc_trend_signal(vs_currency=vs_currency)


if __name__ == "__main__":
    # stdio transport by default
    mcp.run()
