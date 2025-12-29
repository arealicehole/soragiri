"""
Sora Watermark Removal Discord Bot
Monitors for Sora video URLs and removes watermarks using Kie.ai API
"""

import os
import re
import json
import asyncio
import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
KIE_API_KEY = os.getenv("KIE_API_KEY")

# Kie.ai API endpoints
KIE_BASE_URL = "https://api.kie.ai/api/v1"
CREATE_ENDPOINT = f"{KIE_BASE_URL}/jobs/createTask"
QUERY_ENDPOINT = f"{KIE_BASE_URL}/jobs/recordInfo"

# Regex to match Sora video URLs
SORA_URL_PATTERN = re.compile(r'https?://sora\.chatgpt\.com/[^\s<>"]+')

# Bot setup with required intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


class KieAIClient:
    """Async client for Kie.ai watermark removal API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    async def create_task(self, session: aiohttp.ClientSession, video_url: str) -> str:
        """Submit a video for watermark removal, returns task_id"""
        payload = {
            "model": "sora-watermark-remover",
            "input": {"video_url": video_url}
        }

        async with session.post(CREATE_ENDPOINT, headers=self.headers, json=payload) as resp:
            if resp.status == 429:
                raise Exception("Rate limited - please wait before trying again")

            data = await resp.json()

            if data.get("code") != 200:
                error_msg = data.get("message", "Unknown error")
                raise Exception(f"API Error: {error_msg}")

            return data["data"]["taskId"]

    async def query_task(self, session: aiohttp.ClientSession, task_id: str) -> dict:
        """Check status of a watermark removal task"""
        params = {"taskId": task_id}

        async with session.get(QUERY_ENDPOINT, headers=self.headers, params=params) as resp:
            return await resp.json()

    async def remove_watermark(self, video_url: str, max_attempts: int = 60) -> str:
        """
        Full watermark removal flow - submit and poll until complete
        Returns the clean video URL
        """
        async with aiohttp.ClientSession() as session:
            # Create the task
            task_id = await self.create_task(session, video_url)
            print(f"[Kie.ai] Task created: {task_id}")

            # Poll for completion
            for attempt in range(max_attempts):
                await asyncio.sleep(2)  # Wait 2 seconds between polls

                result = await self.query_task(session, task_id)
                data = result.get("data", {})
                state = data.get("state", "unknown")

                if state == "success":
                    # resultJson is a JSON string containing resultUrls array
                    result_json_str = data.get("resultJson", "{}")
                    result_json = json.loads(result_json_str)
                    result_urls = result_json.get("resultUrls", [])
                    if result_urls:
                        return result_urls[0]
                    raise Exception("Success but no video URL in response")

                elif state == "fail":
                    error = data.get("failMsg", "Unknown failure")
                    raise Exception(f"Processing failed: {error}")

                print(f"[Kie.ai] Processing... state={state} ({attempt + 1}/{max_attempts})")

            raise TimeoutError("Watermark removal timed out after 2 minutes")


# Initialize the Kie.ai client
kie_client = KieAIClient(KIE_API_KEY) if KIE_API_KEY else None


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    print(f"Kie.ai API: {'Configured' if kie_client else 'NOT CONFIGURED'}")
    print("Monitoring for Sora video URLs...")


@bot.event
async def on_message(message: discord.Message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Only process Sora URLs if the bot is mentioned
    if bot.user in message.mentions:
        sora_urls = SORA_URL_PATTERN.findall(message.content)
        if sora_urls:
            await process_sora_videos(message, sora_urls)

    # Process commands too
    await bot.process_commands(message)


async def process_sora_videos(message: discord.Message, urls: list[str]):
    """Process Sora video URLs and reply with watermark-free versions"""

    if not kie_client:
        await message.reply("Bot error: Kie.ai API key not configured!")
        return

    for url in urls:
        # React to show we're processing
        try:
            await message.add_reaction("⏳")
        except discord.errors.Forbidden:
            pass

        try:
            # Send processing message
            status_msg = await message.reply(
                f"Processing watermark removal for your Sora video...\n"
                f"This usually takes 5-30 seconds."
            )

            # Call Kie.ai API
            clean_url = await kie_client.remove_watermark(url)

            # Download the video to upload to Discord
            async with aiohttp.ClientSession() as session:
                async with session.get(clean_url) as resp:
                    if resp.status == 200:
                        video_data = await resp.read()

                        # Create a file to upload
                        file = discord.File(
                            fp=__import__('io').BytesIO(video_data),
                            filename="watermark_removed.mp4"
                        )

                        # Delete status message
                        await status_msg.delete()

                        # Reply with the clean video
                        await message.reply(
                            f"Here's your watermark-free video!",
                            file=file
                        )
                    else:
                        await status_msg.edit(
                            content=f"Failed to download processed video (HTTP {resp.status})"
                        )

            # Update reaction
            try:
                await message.remove_reaction("⏳", bot.user)
                await message.add_reaction("✅")
            except discord.errors.Forbidden:
                pass

        except Exception as e:
            error_msg = str(e)
            print(f"[Error] Watermark removal failed: {error_msg}")

            # Update reaction
            try:
                await message.remove_reaction("⏳", bot.user)
                await message.add_reaction("❌")
            except discord.errors.Forbidden:
                pass

            await message.reply(
                f"Failed to remove watermark: {error_msg}\n\n"
                f"**Note:** This only works with published Sora videos from `sora.chatgpt.com`"
            )


@bot.command(name="status")
async def status_command(ctx: commands.Context):
    """Check bot status"""
    embed = discord.Embed(
        title="Sora Watermark Remover Status",
        color=discord.Color.green() if kie_client else discord.Color.red()
    )
    embed.add_field(name="Bot", value="Online", inline=True)
    embed.add_field(
        name="Kie.ai API",
        value="Connected" if kie_client else "Not Configured",
        inline=True
    )
    embed.add_field(
        name="How to use",
        value="Mention me with a Sora video URL:\n`@SoraBot https://sora.chatgpt.com/...`",
        inline=False
    )
    await ctx.send(embed=embed)


@bot.command(name="remove")
async def remove_command(ctx: commands.Context, url: str = None):
    """Manually trigger watermark removal for a URL"""
    if not url:
        await ctx.reply("Please provide a Sora video URL: `!remove <url>`")
        return

    if not SORA_URL_PATTERN.match(url):
        await ctx.reply(
            "Invalid URL. This bot only works with Sora videos.\n"
            "URL must start with `https://sora.chatgpt.com/`"
        )
        return

    await process_sora_videos(ctx.message, [url])


def main():
    if not DISCORD_TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env file!")
        print("Create a .env file with:")
        print("  DISCORD_TOKEN=your_discord_bot_token")
        print("  KIE_API_KEY=your_kie_ai_api_key")
        return

    if not KIE_API_KEY:
        print("WARNING: KIE_API_KEY not found in .env file!")
        print("Bot will start but watermark removal won't work.")

    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
