#!/usr/bin/env python3
"""
SoraGiri (空斬り) CLI
Cyber-Samurai Watermark Removal Tool

Usage:
    python soragiri_cli.py <sora_url>
    python soragiri_cli.py <sora_url> -o output.mp4
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Import from the local package logic
from cogs.soragiri import SoraGiri, SliceState

# Load environment
load_dotenv()

# ==============================================================================
# CYBER-SAMURAI AESTHETIC (ASCII-SAFE)
# ==============================================================================

KATANA = r"""
    +-----------------------------------------------------------+
    |                                                           |
    |   ____   ___  ____   ____  ____ ___ ____  _               |
    |  / ___| / _ \|  _ \ / _  |/ ___|_ _|  _ \| |              |
    |  \___ \| | | | |_) | (_| | |  _ | || |_) | |              |
    |   ___) | |_| |  _ < \__, | |_| || ||  _ <| |              |
    |  |____/ \___/|_| \_\  /  |\____|___|_| \_\_|              |
    |                      |__/  空 斬 り                       |
    |                                                           |
    |               [ Watermark Slicing Engine ]                |
    +-----------------------------------------------------------+
"""

# ANSI colors
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    # Cyber colors
    NEON = "\033[38;5;199m"
    BLADE = "\033[38;5;51m"
    GLOW = "\033[38;5;226m"


def print_banner():
    """Display the SoraGiri banner"""
    print(f"{C.BLADE}{KATANA}{C.RESET}")


def blade_print(msg: str, color: str = C.BLADE):
    """Print with blade prefix"""
    print(f"  {C.DIM}|{C.RESET} {color}{msg}{C.RESET}")


def on_progress(state: SliceState, message: str):
    """Handle progress updates with cyber-samurai flair"""
    icons = {
        SliceState.INITIALIZING: f"{C.CYAN}>>",
        SliceState.UPLOADING: f"{C.YELLOW}^",
        SliceState.QUEUED: f"{C.MAGENTA}#",
        SliceState.SLICING: f"{C.NEON}X",
        SliceState.DOWNLOADING: f"{C.BLUE}V",
        SliceState.COMPLETE: f"{C.GREEN}OK",
        SliceState.FAILED: f"{C.RED}ERR",
    }
    icon = icons.get(state, "*")
    blade_print(f"{icon} {message}{C.RESET}")


async def run_slice(url: str, output: Path, api_key: str) -> bool:
    """Execute the slice operation"""
    giri = SoraGiri(api_key)

    print()
    blade_print(f"{C.DIM}Target acquired:{C.RESET}")
    blade_print(f"{C.WHITE}{url}{C.RESET}")
    print(f"  {C.DIM}|{C.RESET}")

    result = await giri.slice(
        video_url=url,
        output_path=output,
        on_progress=on_progress
    )

    print(f"  {C.DIM}|{C.RESET}")

    if result.success:
        blade_print(f"{C.GREEN}{C.BOLD}SLICE COMPLETE{C.RESET}")
        blade_print(f"{C.DIM}Local File:{C.RESET} {C.WHITE}{result.output_path}{C.RESET}")
        
        # Add the full URL so it's clickable in modern terminals
        if result.output_url:
            blade_print(f"{C.DIM}Cloud Link:{C.RESET} {C.CYAN}{C.BOLD}{result.output_url}{C.RESET}")
            
        if result.cost_time_ms:
            blade_print(f"{C.DIM}Time Taken:{C.RESET} {C.GLOW}{result.cost_time_ms}ms{C.RESET}")
        print()
        return True
    else:
        blade_print(f"{C.RED}{C.BOLD}SLICE FAILED{C.RESET}")
        blade_print(f"{C.RED}{result.error}{C.RESET}")
        print()
        return False


def generate_output_name() -> Path:
    """Generate timestamped output filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path(f"soragiri_{timestamp}.mp4")


def main():
    parser = argparse.ArgumentParser(
        description="SoraGiri (空斬り) - Watermark Slicing Engine"
    )
    parser.add_argument("url", help="Sora video URL")
    parser.add_argument("-o", "--output", type=Path, help="Output file path")
    parser.add_argument("-q", "--quiet", action="store_true", help="Minimal output")

    args = parser.parse_args()

    # Get API key
    api_key = os.getenv("KIE_API_KEY")
    if not api_key:
        print(f"{C.RED}Error: KIE_API_KEY not found in environment{C.RESET}")
        sys.exit(1)

    output = args.output or generate_output_name()

    if not args.quiet:
        print_banner()

    try:
        success = asyncio.run(run_slice(args.url, output, api_key))
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}  Blade sheathed.{C.RESET}")
        sys.exit(130)


if __name__ == "__main__":
    main()