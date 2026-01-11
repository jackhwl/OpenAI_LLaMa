# password_server.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
import secrets
import math
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Password Generator")

# Character sets
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/\\|~`"
AMBIGUOUS = set("O0oIl1|")

def _filtered(chars: str, exclude_ambiguous: bool) -> str:
    """Optionally filter out ambiguous characters."""
    if not exclude_ambiguous:
        return chars
    return "".join(c for c in chars if c not in AMBIGUOUS)

def _entropy_bits(pool_size: int, length: int) -> float:
    """Estimate entropy in bits based on pool size and password length."""
    return length * math.log2(pool_size) if pool_size > 0 else 0.0

@dataclass
class PasswordResult:
    password: str
    length: int
    pool_size: int
    entropy_bits: float
    required_each_class: bool
    options: Dict[str, bool]

@mcp.tool
def generate_password(
    length: int = 16,
    include_upper: bool = True,
    include_lower: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
    exclude_ambiguous: bool = True,
    require_each_class: bool = True,
) -> PasswordResult:
    """
    Generate a strong random password with configurable options.

    Args:
      length: password length (min 4, max 256)
      include_upper: include A-Z
      include_lower: include a-z
      include_digits: include 0-9
      include_symbols: include symbols
      exclude_ambiguous: remove ambiguous characters (like O/0, l/1)
      require_each_class: ensure at least one char from each selected class

    Returns:
      PasswordResult: password + metadata including estimated entropy (bits).
    """
    if length < 4 or length > 256:
        raise ValueError("length must be between 4 and 256")

    pools = []
    if include_upper:  pools.append(_filtered(UPPER, exclude_ambiguous))
    if include_lower:  pools.append(_filtered(LOWER, exclude_ambiguous))
    if include_digits: pools.append(_filtered(DIGITS, exclude_ambiguous))
    if include_symbols:pools.append(_filtered(SYMBOLS, exclude_ambiguous))

    # Remove empty pools (e.g., if all chars filtered out)
    pools = [p for p in pools if p]
    if not pools:
        raise ValueError("No characters available. Enable at least one class or disable ambiguity filter.")

    pool = "".join(pools)

    # Ensure at least one char from each class if required
    password_chars = []
    if require_each_class:
        if length < len(pools):
            raise ValueError(f"length {length} too short for {len(pools)} required classes.")
        for p in pools:
            password_chars.append(secrets.choice(p))

    # Fill the rest
    while len(password_chars) < length:
        password_chars.append(secrets.choice(pool))

    # Shuffle to avoid predictable positions
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    password = "".join(password_chars)
    entropy = _entropy_bits(len(pool), length)

    return PasswordResult(
        password=password,
        length=length,
        pool_size=len(pool),
        entropy_bits=round(entropy, 2),
        required_each_class=require_each_class,
        options={
            "include_upper": include_upper,
            "include_lower": include_lower,
            "include_digits": include_digits,
            "include_symbols": include_symbols,
            "exclude_ambiguous": exclude_ambiguous,
        },
    )

if __name__ == "__main__":
    # Start the MCP server (stdio transport by default)
    mcp.run()

