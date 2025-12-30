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

from cogs.soragiri import SoraGiri, SliceState

# Load environment
load_dotenv()

# ═══════════════════════════════════════════════════════════════
# CYBER-SAMURAI AESTHETIC
# ═══════════════════════════════════════════════════════════════

KATANA = r"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ░██████╗░█████╗░██████╗░█████╗░░██████╗░██╗██████╗░██╗  ║
    ║   ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝░██║██╔══██╗██║  ║
    ║   ╚█████╗░██║░░██║██████╔╝███████║██║░░██╗░██║██████╔╝██║  ║
    ║   ░╚═══██╗██║░░██║██╔══██╗██╔══██║██║░░╚██╗██║██╔══██╗██║  ║
    ║   ██████╔╝╚█████╔╝██║░░██║██║░░██║╚██████╔╝██║██║░░██║██║  ║
    ║   ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░╚═╝╚═╝░░╚═╝╚═╝  ║
    ║                        空 斬 り                            ║
    ║               [ Watermark Slicing Engine ]                ║
    ╚═══════════════════════════════════════════════════════════╝
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
    print(f"  {C.DIM}│{C.RESET} {color}{msg}{C.RESET}")


def progress_bar(current: int, total: int, width: int = 30) -> str:
    """Generate a katana-style progress bar"""
    filled = int(width * current / total)
    bar = "━" * filled + "╍" * (width - filled)
    tip = "⚔" if current < total else "✓"
    return f"{C.BLADE}[{bar}]{C.RESET} {tip}"


def on_progress(state: SliceState, message: str):
    """Handle progress updates with cyber-samurai flair"""
    icons = {
        SliceState.INITIALIZING: f"{C.CYAN}⚡",
        SliceState.UPLOADING: f"{C.YELLOW}↑",
        SliceState.QUEUED: f"{C.MAGENTA}◈",
        SliceState.SLICING: f"{C.NEON}⚔",
        SliceState.DOWNLOADING: f"{C.BLUE}↓",
        SliceState.COMPLETE: f"{C.GREEN}✓",
        SliceState.FAILED: f"{C.RED}✗",
    }
    icon = icons.get(state, "•")
    blade_print(f"{icon} {message}{C.RESET}")


async def run_slice(url: str, output: Path, api_key: str) -> bool:
    """Execute the slice operation"""
    giri = SoraGiri(api_key)

    print()
    blade_print(f"{C.DIM}Target acquired:{C.RESET}")
    blade_print(f"{C.WHITE}{url}{C.RESET}")
    print(f"  {C.DIM}│{C.RESET}")

    result = await giri.slice(
        video_url=url,
        output_path=output,
        on_progress=on_progress
    )

    print(f"  {C.DIM}│{C.RESET}")

    if result.success:
        blade_print(f"{C.GREEN}{C.BOLD}SLICE COMPLETE{C.RESET}")
        blade_print(f"{C.DIM}Output:{C.RESET} {C.WHITE}{result.output_path}{C.RESET}")
        if result.cost_time_ms:
            blade_print(f"{C.DIM}Time:{C.RESET} {C.GLOW}{result.cost_time_ms}ms{C.RESET}")
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
        description="SoraGiri (空斬り) - Watermark Slicing Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python soragiri_cli.py https://sora.chatgpt.com/p/s_abc123
  python soragiri_cli.py https://sora.chatgpt.com/p/s_abc123 -o clean.mp4
        """
    )
    parser.add_argument("url", help="Sora video URL (sora.chatgpt.com/...)")
    parser.add_argument("-o", "--output", type=Path, help="Output file path (default: auto-generated)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Minimal output")

    args = parser.parse_args()

    # Validate URL
    if "sora.chatgpt.com" not in args.url:
        print(f"{C.RED}Error: URL must be from sora.chatgpt.com{C.RESET}")
        sys.exit(1)

    # Get API key
    api_key = os.getenv("KIE_API_KEY")
    if not api_key:
        print(f"{C.RED}Error: KIE_API_KEY not found in environment{C.RESET}")
        print(f"{C.DIM}Set it in .env or export KIE_API_KEY=your_key{C.RESET}")
        sys.exit(1)

    # Output path
    output = args.output or generate_output_name()

    # Show banner
    if not args.quiet:
        print_banner()

    # Run the slice
    try:
        success = asyncio.run(run_slice(args.url, output, api_key))
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}  Blade sheathed.{C.RESET}")
        sys.exit(130)


if __name__ == "__main__":
    main()
