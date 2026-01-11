# weather_plugins.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Literal, Dict, Any
from fastmcp import FastMCP

Units = Literal["imperial", "metric"]

@dataclass
class Location:
    city: str
    country: str = "US"

@dataclass
class CurrentWeather:
    location: Location
    temperature: float
    humidity: int
    condition: str
    observed_at: str
    units: Units

@dataclass
class DailyForecast:
    date: str
    high: float
    low: float
    condition: str

@dataclass
class ForecastResponse:
    location: Location
    days: List[DailyForecast]
    units: Units

# Create your FastMCP instance (decorate off this)
server = FastMCP("weather-with-plugins")

# --- helpers/stubs ---
_CONDITIONS = ["Sunny", "Partly Cloudy", "Cloudy", "Showers", "Thunderstorms"]

def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"

def _fake_temp(city: str, units: Units) -> float:
    base = 72.0 if units == "imperial" else 22.0
    tweak = (sum(ord(c) for c in city) % 7) - 3  # -3..+3
    return float(base + tweak)

def _fake_forecast(city: str, units: Units, days: int) -> List[DailyForecast]:
    start = datetime.utcnow().date()
    out: List[DailyForecast] = []
    base = 72.0 if units == "imperial" else 22.0
    for i in range(days):
        d = start + timedelta(days=i+1)
        delta = (i % 5) - 2
        high = base + 5 + delta
        low = base - 3 + delta
        cond = _CONDITIONS[(i + (sum(ord(c) for c in city) % 5)) % len(_CONDITIONS)]
        out.append(DailyForecast(date=d.isoformat(), high=float(high), low=float(low), condition=cond))
    return out

# --- core tools (decorate off `server`) ---
@server.tool
def get_weather(city: str, units: Units = "imperial") -> Dict[str, Any]:
    """Get current weather (stubbed) for a city."""
    if units not in ("imperial", "metric"):
        raise ValueError('units must be "imperial" or "metric"')
    cw = CurrentWeather(
        location=Location(city=city),
        temperature=_fake_temp(city, units),
        humidity=55,
        condition="Sunny",
        observed_at=_now_iso(),
        units=units,
    )
    return asdict(cw)

@server.tool
def get_forecast(city: str, days: int = 5, units: Units = "imperial") -> Dict[str, Any]:
    """Get a multi-day forecast (stubbed)."""
    if not (1 <= days <= 7):
        raise ValueError("days must be between 1 and 7")
    if units not in ("imperial", "metric"):
        raise ValueError('units must be "imperial" or "metric"')
    resp = ForecastResponse(location=Location(city=city), days=_fake_forecast(city, units, days), units=units)
    return {"location": asdict(resp.location), "days": [asdict(d) for d in resp.days], "units": resp.units}

# --- plugin registration (each plugin exposes register(server)) ---
try:
    import sentiment_plugin
    sentiment_plugin.register(server)
except Exception as e:
    print(f"[weather-with-plugins] sentiment_plugin not loaded: {e}")

try:
    import translate_plugin
    translate_plugin.register(server)
except Exception as e:
    print(f"[weather-with-plugins] translate_plugin not loaded: {e}")

if __name__ == "__main__":
    server.run()

