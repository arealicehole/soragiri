#!/usr/bin/env python3
"""
SoraGiri (空斬り) Discord Bot
Cyber-Samurai Watermark Removal Engine

Run with: python bot.py
"""

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Banner
BANNER = r"""
╔═══════════════════════════════════════════════════════════════╗
║  ░██████╗░█████╗░██████╗░█████╗░░██████╗░██╗██████╗░██╗       ║
║  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝░██║██╔══██╗██║       ║
║  ╚█████╗░██║░░██║██████╔╝███████║██║░░██╗░██║██████╔╝██║       ║
║  ░╚═══██╗██║░░██║██╔══██╗██╔══██║██║░░╚██╗██║██╔══██╗██║       ║
║  ██████╔╝╚█████╔╝██║░░██║██║░░██║╚██████╔╝██║██║░░██║██║       ║
║  ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░╚═╝╚═╝░░╚═╝╚═╝       ║
║                         空 斬 り                               ║
║              [ Discord Watermark Slicing Bot ]                ║
╚═══════════════════════════════════════════════════════════════╝
"""


class SoraGiriBot(commands.Bot):
    """SoraGiri Discord Bot"""

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        """Load cogs and sync commands"""
        # Load the SoraGiri cog
        await self.load_extension("discord.cogs.soragiri_cog")
        print("[SoraGiri] Cog loaded")

        # Sync slash commands
        await self.tree.sync()
        print("[SoraGiri] Slash commands synced")

    async def on_ready(self):
        """Called when bot is ready"""
        print(BANNER)
        print(f"[SoraGiri] Online as {self.user}")
        print(f"[SoraGiri] Servers: {len(self.guilds)}")
        print(f"[SoraGiri] Commands: /slice, !slice, @mention")
        print("[SoraGiri] The blade is ready.")


@commands.command(name="help")
async def help_command(ctx: commands.Context):
    """Custom help command"""
    embed = discord.Embed(
        title="⚔️ SoraGiri 空斬り",
        description="**Watermark Slicing Engine**\n\nRemove watermarks from Sora videos with precision.",
        color=0x00FFFF
    )
    embed.add_field(
        name="Commands",
        value=(
            "`/slice <url>` - Slash command\n"
            "`!slice <url>` - Prefix command\n"
            "`@SoraGiri <url>` - Mention with URL"
        ),
        inline=False
    )
    embed.add_field(
        name="Supported URLs",
        value="`https://sora.chatgpt.com/...`",
        inline=False
    )
    embed.set_footer(text="空斬り • The blade that severs watermarks")
    await ctx.send(embed=embed)


def main():
    if not DISCORD_TOKEN:
        print("[SoraGiri] ERROR: DISCORD_TOKEN not found")
        print("[SoraGiri] Create a .env file with:")
        print("  DISCORD_TOKEN=your_token")
        print("  KIE_API_KEY=your_api_key")
        return

    if not os.getenv("KIE_API_KEY"):
        print("[SoraGiri] WARNING: KIE_API_KEY not found")
        print("[SoraGiri] The blade will be dull without it.")

    bot = SoraGiriBot()
    bot.add_command(help_command)
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
