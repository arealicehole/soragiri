"""
SoraGiri (空斬り) Discord Cog
Cyber-Samurai Watermark Removal for Discord

Drop this folder into any bot's cogs/ directory and load with:
    await bot.load_extension("cogs.soragiri")
"""

import os
import re
import io
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

# Import the blade (relative import - same package)
from .core import SoraGiri, SliceState


# Sora URL pattern
SORA_URL_PATTERN = re.compile(r'https?://sora\.chatgpt\.com/[^\s<>"]+')


class ProgressEmbed:
    """Manages the progress embed for Discord messages"""

    STATES = {
        SliceState.INITIALIZING: ("⚡", "Unsheathing...", 0x00FFFF),
        SliceState.UPLOADING: ("📤", "Uploading...", 0xFFFF00),
        SliceState.QUEUED: ("◈", "In Queue", 0xFF00FF),
        SliceState.SLICING: ("⚔️", "Slicing Watermark", 0xFF1493),
        SliceState.DOWNLOADING: ("📥", "Retrieving...", 0x00BFFF),
        SliceState.COMPLETE: ("✅", "Slice Complete", 0x00FF00),
        SliceState.FAILED: ("❌", "Slice Failed", 0xFF0000),
    }

    @classmethod
    def create(cls, state: SliceState, message: str, url: str = None) -> discord.Embed:
        """Create a progress embed"""
        icon, title, color = cls.STATES.get(state, ("•", "Processing", 0x808080))

        embed = discord.Embed(
            title=f"{icon} SoraGiri 空斬り",
            description=f"**{title}**\n{message}",
            color=color
        )

        if url:
            embed.add_field(name="Target", value=f"`{url[:50]}...`", inline=False)

        # Progress bar for active states
        if state in (SliceState.QUEUED, SliceState.SLICING):
            embed.set_footer(text="━━━━━━━━━━━━━━━━━━━━ ⚔")
        elif state == SliceState.COMPLETE:
            embed.set_footer(text="━━━━━━━━━━━━━━━━━━━━ ✓")

        return embed


class SoraGiriCog(commands.Cog, name="SoraGiri"):
    """
    SoraGiri (空斬り) - Watermark Slicing Engine

    Slash through Sora watermarks with precision.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        api_key = os.getenv("KIE_API_KEY")
        if api_key:
            self.giri = SoraGiri(api_key)
        else:
            self.giri = None
            print("[SoraGiri] WARNING: KIE_API_KEY not set - blade is dull")

    @app_commands.command(name="slice", description="Remove watermark from a Sora video")
    @app_commands.describe(url="The Sora video URL (sora.chatgpt.com/...)")
    async def slash_slice(self, interaction: discord.Interaction, url: str):
        """Slash command: /slice <url>"""
        await self._process_slice(interaction, url)

    @commands.command(name="slice", aliases=["soragiri", "giri"])
    async def prefix_slice(self, ctx: commands.Context, url: str = None):
        """Prefix command: !slice <url> or !soragiri <url>"""
        if not url:
            embed = discord.Embed(
                title="⚔️ SoraGiri 空斬り",
                description="**Usage:** `!slice <sora_url>`\n\nProvide a Sora video URL to slice the watermark.",
                color=0x00FFFF
            )
            await ctx.reply(embed=embed)
            return

        # Create a fake interaction-like context for unified handling
        await self._process_slice_ctx(ctx, url)

    async def _process_slice(self, interaction: discord.Interaction, url: str):
        """Process slice via slash command"""
        # Validate
        if not self.giri:
            await interaction.response.send_message(
                "❌ SoraGiri is not configured (missing API key)",
                ephemeral=True
            )
            return

        if not SORA_URL_PATTERN.match(url):
            await interaction.response.send_message(
                "❌ Invalid URL. Must be from `sora.chatgpt.com`",
                ephemeral=True
            )
            return

        # Initial response
        embed = ProgressEmbed.create(SliceState.INITIALIZING, "Preparing the blade...", url)
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()

        # Process
        await self._do_slice(message, url)

    async def _process_slice_ctx(self, ctx: commands.Context, url: str):
        """Process slice via prefix command"""
        # Validate
        if not self.giri:
            await ctx.reply("❌ SoraGiri is not configured (missing API key)")
            return

        if not SORA_URL_PATTERN.match(url):
            await ctx.reply("❌ Invalid URL. Must be from `sora.chatgpt.com`")
            return

        # Initial response
        embed = ProgressEmbed.create(SliceState.INITIALIZING, "Preparing the blade...", url)
        message = await ctx.reply(embed=embed)

        # Process
        await self._do_slice(message, url)

    async def _do_slice(self, message: discord.Message, url: str):
        """Execute the slice operation"""
        last_state = [None]  # Mutable container for closure

        async def update_progress(state: SliceState, msg: str):
            """Update the embed with progress"""
            if state != last_state[0]:
                last_state[0] = state
                embed = ProgressEmbed.create(state, msg, url)
                try:
                    await message.edit(embed=embed)
                except discord.errors.NotFound:
                    pass

        try:
            # Add reaction
            try:
                await message.add_reaction("⚔️")
            except:
                pass

            # Execute slice
            success, result = await self.giri.slice_to_bytes(
                video_url=url,
                on_progress=update_progress
            )

            if success:
                # Upload the video
                video_bytes = result
                file = discord.File(
                    fp=io.BytesIO(video_bytes),
                    filename="soragiri_clean.mp4"
                )

                # Final embed
                embed = ProgressEmbed.create(
                    SliceState.COMPLETE,
                    "Watermark has been severed.",
                    url
                )
                await message.edit(embed=embed)
                await message.reply("Here's your clean cut:", file=file)

                # Update reaction
                try:
                    await message.clear_reaction("⚔️")
                    await message.add_reaction("✅")
                except:
                    pass

            else:
                # Failed
                embed = ProgressEmbed.create(
                    SliceState.FAILED,
                    f"The blade could not complete the cut.\n`{result}`",
                    url
                )
                await message.edit(embed=embed)

                try:
                    await message.clear_reaction("⚔️")
                    await message.add_reaction("❌")
                except:
                    pass

        except Exception as e:
            embed = ProgressEmbed.create(
                SliceState.FAILED,
                f"Unexpected error: `{str(e)}`",
                url
            )
            await message.edit(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Auto-detect Sora URLs when bot is mentioned"""
        if message.author.bot:
            return

        if self.bot.user not in message.mentions:
            return

        # Check for Sora URLs
        urls = SORA_URL_PATTERN.findall(message.content)
        if not urls:
            return

        # Process each URL
        for url in urls:
            embed = ProgressEmbed.create(SliceState.INITIALIZING, "Preparing the blade...", url)
            reply = await message.reply(embed=embed)
            await self._do_slice(reply, url)


async def setup(bot: commands.Bot):
    """Setup function for loading the cog"""
    await bot.add_cog(SoraGiriCog(bot))
    print("[SoraGiri] Cog loaded - blade is ready")
