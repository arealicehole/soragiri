# ⚔️ SoraGiri (空斬り)

```text
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   ██████╗░██████╗░██████╗░██████╗░░██████╗░██╗██████╗░██╗  ║
    ║   ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝░██║██╔══██╗██║  ║
    ║   ╚█████╗░██║░░██║██████╔╝███████║██║░░██╗░██║██████╔╝██║  ║
    ║   ░╚═══██╗██║░░██║██╔══██╗██╔══██║██║░░╚██╗██║██╔══██╗██║  ║
    ║   ██████╔╝╚█████╔╝██║░░██║██║░░██║╚██████╔╝██║██║░░██║██║  ║
    ║   ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░╚═╝╚═╝░░╚═╝╚═╝  ║
    ║                        空 斬 り                            ║
    ║               [ Watermark Slicing Engine ]               ║
    ╚══════════════════════════════════════════════════════════╝
```

**The blade that severs Sora watermarks.**

A portable watermark removal engine with CLI for self-hosting and a Discord Cog for server integration. Powered by [Kie.ai](https://kie.ai).

Built by **[Tricon Digital](https://tricondigital.com)**.

---

## ⚡ Features

- **Core Engine** — Zero-dependency watermark removal class
- **CLI Tool** — Terminal interface with Cyber-Samurai aesthetic
- **Discord Bot** — Full-featured cog with slash commands
- **Library** — Pip installable for your own python projects
- **Docker** — Container image on GitHub Container Registry

---

## 📂 Architecture

```
soragiri/
├── cogs/
│   └── soragiri/
│       ├── __init__.py      # Package exports
│       ├── core.py          # The Blade - zero-dependency engine
│       └── cog.py           # Discord Cog with commands
├── soragiri_cli.py          # CLI with cyber-samurai aesthetic
├── bot.py                   # Standalone Discord bot entry
├── pyproject.toml           # Pip package config
├── requirements.txt         # Dependencies
├── Dockerfile               # Container build
└── .github/workflows/
    └── docker.yml           # Auto-build to GHCR on tags
```

---

## ⚡ Quick Start

### 1. Get Your API Key

Sign up at [kie.ai](https://kie.ai) and get your API key. Cost: ~$0.05 per video.

### 2. Clone & Configure

```bash
git clone https://github.com/arealicehole/soragiri.git
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
```

**Output:**
```text
  │ Target acquired:
  │ https://sora.chatgpt.com/p/s_abc123
  │
  │ ⚡ Unsheathing the blade...
  │ ◎ Task locked: e989621f...
  │ ⚔ Slicing... ⚔ [━━━━━━━━━━━━━━━━━━━━━━━] ✓
  │ ⚔ Watermark severed.
  │ ✓ Saved to soragiri_20241229_161823.mp4
  │
  │ SLICE COMPLETE
  │ Local File: file:///C:/Users/User/videos/soragiri_20241229.mp4
  │ Time: 8420ms
```

---

## 🤖 Discord Bot

Full Discord integration with slash commands, prefix commands, and @mention support.

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
| `/slice <url>` | Slash command - remove watermark |
| `!slice <url>` | Prefix command - remove watermark |
| `@SoraGiri <url>` | Mention the bot with a URL |
| `!status` | Show bot status and usage |

---

## 🐳 Docker

Pull the pre-built image from GitHub Container Registry:

```bash
# Pull latest
docker pull ghcr.io/arealicehole/soragiri:latest

# Run as CLI
docker run --rm -e KIE_API_KEY=your_key \
  ghcr.io/arealicehole/soragiri \
  https://sora.chatgpt.com/p/s_abc123

# Run as Discord bot
docker run -d -e KIE_API_KEY=your_key -e DISCORD_TOKEN=your_token \
  ghcr.io/arealicehole/soragiri bot
```

Or build locally:

```bash
docker build -t soragiri .
```

---

## 🏗️ Install as Library (Pip)

You can install SoraGiri directly into your own projects (like we do in [Tricon Lab](https://discord.gg/QVAKXAerma)):

```bash
pip install git+https://github.com/arealicehole/soragiri.git
```

Then use it in Python:

```python
from cogs.soragiri import SoraGiri

async def main():
    giri = SoraGiri(api_key="your_key")
    result = await giri.slice("https://sora.chatgpt.com/...", "clean.mp4")
```

---

## 🧪 Tricon Lab

Don't want to self-host? Use the hosted version of SoraGiri in our public lab:

**[Join the Discord Lab](https://discord.gg/QVAKXAerma)**

---

## 📜 License

MIT License. Free to use, modify, and distribute.

---

<p align="center">
  <strong>空斬り</strong> — <em>The blade that severs watermarks</em>
</p>
