
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import List, Literal, Dict

from fastmcp import FastMCP

# -----------------------------------------------------------------------------
# Types & Data Models
# -----------------------------------------------------------------------------

Units = Literal["imperial", "metric"]

@dataclass
class Location:
    city: str
    country: str

@dataclass
class WeatherNow:
    location: Location
    temperature: float
    humidity: int
    condition: str
    observed_at: str
    units: Units

@dataclass
class ForecastDay:
    date: str
    high: float
    low: float
    condition: str

@dataclass
class WeatherForecast:
    location: Location
    days: List[ForecastDay]
    units: Units


# -----------------------------------------------------------------------------
# Server Initialization
# -----------------------------------------------------------------------------

mcp = FastMCP("Weather MCP (Stubbed)")


# -----------------------------------------------------------------------------
# Helpers (Deterministic Stubs)
# -----------------------------------------------------------------------------

# A minimal, deterministic baseline “climate” per city for demo purposes.
# You can expand this or switch to a real API later without changing the output shapes.
BASELINES: Dict[str, Dict[str, float]] = {
    "san diego": {"temp_f": 72.0, "humidity": 55},
    "seattle":   {"temp_f": 64.0, "humidity": 70},
    "austin":    {"temp_f": 90.0, "humidity": 60},
    "london":    {"temp_f": 68.0, "humidity": 65},
    "new york":  {"temp_f": 75.0, "humidity": 58},
}

CONDITION_CYCLE = ["Sunny", "Partly Cloudy", "Cloudy", "Rain"]

def normalize_city(city: str) -> str:
    return city.strip().lower()

def to_celsius(fahrenheit: float) -> float:
    return round((fahrenheit - 32) * 5.0 / 9.0, 1)

def maybe_convert_temp(temp_f: float, units: Units) -> float:
    return round(temp_f, 1) if units == "imperial" else to_celsius(temp_f)

def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def pick_country(city_norm: str) -> str:
    # Very simple heuristic for demo. Customize as needed.
    if city_norm in {"london"}:
        return "GB"
    return "US"

def baseline_for_city(city_norm: str) -> Dict[str, float]:
    return BASELINES.get(city_norm, {"temp_f": 70.0, "humidity": 55})

def rotated_condition(offset: int) -> str:
    return CONDITION_CYCLE[offset % len(CONDITION_CYCLE)]


# -----------------------------------------------------------------------------
# Tools
# -----------------------------------------------------------------------------

@mcp.tool()
def get_weather(
    city: str,
    units: Units = "imperial",
) -> WeatherNow:
    """
    Return stubbed current weather for a city in structured form.

    Args:
      city: City name (e.g., "San Diego")
      units: "imperial" or "metric"

    Returns:
      WeatherNow dataclass with location, temperature, humidity, condition, timestamp, and units.
    """
    city_norm = normalize_city(city)
    if units not in ("imperial", "metric"):
        raise ValueError("units must be 'imperial' or 'metric'")

    base = baseline_for_city(city_norm)
    # Deterministic condition based on city name hash
    cond_index = abs(hash(city_norm)) % len(CONDITION_CYCLE)
    condition = rotated_condition(cond_index)

    temp = maybe_convert_temp(base["temp_f"], units)
    humidity = int(base["humidity"])

    result = WeatherNow(
        location=Location(city=city.title(), country=pick_country(city_norm)),
        temperature=temp,
        humidity=humidity,
        condition=condition,
        observed_at=iso_now(),
        units=units,
    )
    # Return as dataclass (FastMCP serializes), or as dict via asdict(result)
    return result


@mcp.tool()
def get_forecast(
    city: str,
    days: int = 5,
    units: Units = "imperial",
) -> WeatherForecast:
    """
    Return a stubbed multi-day forecast for a city.

    Args:
      city: City name (e.g., "Austin")
      days: Number of days (1..7)
      units: "imperial" or "metric"

    Returns:
      WeatherForecast dataclass with a list of ForecastDay entries.
    """
    if not (1 <= days <= 7):
        raise ValueError("days must be between 1 and 7")
    if units not in ("imperial", "metric"):
        raise ValueError("units must be 'imperial' or 'metric'")

    city_norm = normalize_city(city)
    base = baseline_for_city(city_norm)
    base_temp_f = base["temp_f"]

    # Deterministic starting offset from city name so each city has a repeatable pattern.
    start_offset = abs(hash(city_norm)) % len(CONDITION_CYCLE)

    forecast_days: List[ForecastDay] = []
    today = datetime.now(timezone.utc).date()

    for i in range(days):
        # Cycle conditions predictably: Sunny -> Partly Cloudy -> Cloudy -> Rain -> ...
        condition = rotated_condition(start_offset + i)

        # Create simple, readable high/low pattern around baseline.
        # Example: +/- up to 5°F in a small wave so tables look realistic.
        wave = ((i % 3) - 1) * 3  # -3, 0, +3 repeating
        high_f = base_temp_f + 5 + wave
        low_f = base_temp_f - 5 + wave

        high = maybe_convert_temp(high_f, units)
        low = maybe_convert_temp(low_f, units)

        forecast_days.append(
            ForecastDay(
                date=(today + timedelta(days=i)).isoformat(),
                high=high,
                low=low,
                condition=condition,
            )
        )

    result = WeatherForecast(
        location=Location(city=city.title(), country=pick_country(city_norm)),
        days=forecast_days,
        units=units,
    )
    return result


# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Start the MCP server (stdio transport by default)
    mcp.run()
