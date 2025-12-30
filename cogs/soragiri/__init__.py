"""
SoraGiri (空斬り) - Watermark Slicing Engine

A self-contained Discord cog for removing Sora watermarks.

Usage:
    # In your bot
    await bot.load_extension("cogs.soragiri")

Requires:
    - KIE_API_KEY environment variable
    - aiohttp
    - discord.py
"""

from .cog import SoraGiriCog, setup
from .core import SoraGiri, SliceState, SliceResult

__all__ = ["SoraGiriCog", "SoraGiri", "SliceState", "SliceResult", "setup"]
__version__ = "2.1.0"
