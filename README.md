# ⚔️ SoraGiri (空斬り)

```
╔═══════════════════════════════════════════════════════════════╗
║  ░██████╗░█████╗░██████╗░█████╗░░██████╗░██╗██████╗░██╗       ║
║  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝░██║██╔══██╗██║       ║
║  ╚█████╗░██║░░██║██████╔╝███████║██║░░██╗░██║██████╔╝██║       ║
║  ░╚═══██╗██║░░██║██╔══██╗██╔══██║██║░░╚██╗██║██╔══██╗██║       ║
║  ██████╔╝╚█████╔╝██║░░██║██║░░██║╚██████╔╝██║██║░░██║██║       ║
║  ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░╚═╝╚═╝░░╚═╝╚═╝       ║
║                         空 斬 り                               ║
║              [ Watermark Slicing Engine ]                     ║
╚═══════════════════════════════════════════════════════════════╝
```

**The blade that severs Sora watermarks.**

A portable watermark removal engine with CLI for self-hosting and a Discord Cog for server integration. Powered by [Kie.ai](https://kie.ai).

---

## 🗡️ Features

- **Core Engine** — Zero-dependency watermark removal class
- **CLI Tool** — Terminal interface for quick slicing
- **Discord Bot** — Full-featured cog with slash commands
- **Docker Ready** — One image, multiple modes

---

## ⚡ Quick Start

### 1. Get Your API Key

Sign up at [kie.ai](https://kie.ai) and get your API key. Cost: ~$0.05 per video.

### 2. Clone & Configure

```bash
git clone https://github.com/yourusername/soragiri.git
cd soragiri
cp .env.example .env
# Edit .env with your KIE_API_KEY
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🖥️ CLI Usage

The fastest way to slice watermarks from your terminal.

```bash
# Basic usage
python soragiri_cli.py https://sora.chatgpt.com/p/s_abc123

# Custom output file
python soragiri_cli.py https://sora.chatgpt.com/p/s_abc123 -o clean_video.mp4

# Quiet mode
python soragiri_cli.py https://sora.chatgpt.com/p/s_abc123 -q
```

**Output:**
```
╔═══════════════════════════════════════════════════════════════╗
║   SoraGiri 空斬り - Watermark Slicing Engine                  ║
╚═══════════════════════════════════════════════════════════════╝

  │ Target acquired:
  │ https://sora.chatgpt.com/p/s_abc123...
  │
  │ ⚡ Unsheathing the blade...
  │ ◈ Task locked: e989621f...
  │ ⚔ Slicing... [3/60]
  │ ⚔ Watermark severed.
  │ ↓ Retrieving the clean cut...
  │ ✓ Saved to soragiri_20241229_161823.mp4
  │
  │ SLICE COMPLETE
  │ Output: soragiri_20241229_161823.mp4
  │ Time: 8420ms
```

---

## 🤖 Discord Bot

Full Discord integration with slash commands and @mention support.

### Setup

1. Create a Discord application at [discord.com/developers](https://discord.com/developers/applications)
2. Add `DISCORD_TOKEN` to your `.env`
3. Invite bot with `applications.commands` and `bot` scopes

### Run

```bash
python bot.py
```

### Commands

| Command | Description |
|---------|-------------|
| `/slice <url>` | Slash command |
| `!slice <url>` | Prefix command |
| `@SoraGiri <url>` | Mention with URL |
| `!help` | Show help |

---

## 🐳 Docker

One image to rule them all. Pre-built on GitHub Container Registry.

### Pull

```bash
docker pull ghcr.io/arealicehole/soragiri:latest
```

### Run Discord Bot

```bash
docker run -d \
  -e DISCORD_TOKEN=your_token \
  -e KIE_API_KEY=your_key \
  --name soragiri \
  ghcr.io/arealicehole/soragiri:latest
```

### Run CLI

```bash
docker run --rm \
  -e KIE_API_KEY=your_key \
  -v $(pwd)/output:/output \
  ghcr.io/arealicehole/soragiri:latest \
  python soragiri_cli.py https://sora.chatgpt.com/... -o /output/clean.mp4
```

### Build Locally (optional)

```bash
docker build -t soragiri .
```

---

## 🔧 Architecture

```
soragiri/
├── cogs/
│   └── soragiri/            # Self-contained cog (drop into any bot)
│       ├── __init__.py      # Exports setup() + classes
│       ├── cog.py           # Discord Cog
│       └── core.py          # The Blade - zero Discord deps
├── bot.py                   # Standalone bot entry point
├── soragiri_cli.py          # CLI wrapper
├── Dockerfile
├── requirements.txt
└── .env.example
```

### Drop-In Cog

Copy `cogs/soragiri/` into any bot's cogs folder:

```python
# In your hub bot
await bot.load_extension("cogs.soragiri")
```

### The Blade (`cogs/soragiri/core.py`)

The core engine with no external dependencies (except aiohttp). Use it in your own projects:

```python
from cogs.soragiri import SoraGiri

async def main():
    giri = SoraGiri(api_key="your_key")

    result = await giri.slice(
        video_url="https://sora.chatgpt.com/...",
        output_path="clean.mp4"
    )

    if result.success:
        print(f"Saved to {result.output_path}")
```

---

## 💰 Pricing

SoraGiri uses the [Kie.ai](https://kie.ai) API:
- **Cost:** 10 credits (~$0.05) per video
- **Processing:** 1-30 seconds typical

---

## 📜 License

MIT

---

<p align="center">
  <strong>空斬り</strong> — <em>The blade that severs watermarks</em>
</p>
