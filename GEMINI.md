# Context: SoraGiri (The Engine)

**Role:** Standalone Watermark Removal Engine.
**Type:** Python Library + CLI + Discord Cog.
**Strategy:** Open Source Lead Magnet.

## Architecture
- **Core:** `core/soragiri.py` (Pure Python, Zero Dependencies).
- **CLI:** `soragiri_cli.py` (For TikTok demos/Self-hosting).
- **Cog:** `cogs/soragiri/` (Drop-in module for bots).

## Deployment
- **Library:** Installed by other bots via `pip install git+...`.
- **Docker:** `ghcr.io/arealicehole/soragiri`.

## Development Rules
1.  **Keep Core Clean:** `core/` must never import `discord`.
2.  **Versioning:** Update `pyproject.toml` version on every significant change.
3.  **Independence:** This repo knows nothing about "Tricon Lab". It is just a tool.
