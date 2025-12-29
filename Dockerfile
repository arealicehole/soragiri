# ╔═══════════════════════════════════════════════════════════════╗
# ║  SoraGiri (空斬り) - Watermark Slicing Engine                  ║
# ║  Docker Image: Dual-mode (Bot + CLI)                          ║
# ╚═══════════════════════════════════════════════════════════════╝

FROM python:3.11-slim

LABEL maintainer="SoraGiri"
LABEL description="Cyber-Samurai Watermark Removal Engine"

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create output directory for CLI
RUN mkdir -p /output

# Environment variables (override at runtime)
ENV DISCORD_TOKEN=""
ENV KIE_API_KEY=""

# Expose nothing - this is a client, not a server

# Default: Run the Discord bot
# Override with: docker run soragiri python soragiri_cli.py <url>
CMD ["python", "bot.py"]
