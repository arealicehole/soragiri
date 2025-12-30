"""
SoraGiri (空斬り) - The Blade
Core watermark removal engine. Zero Discord dependencies.
"""

import json
import asyncio
import inspect
import aiohttp
from pathlib import Path
from typing import Optional, Callable, Union, Awaitable
from dataclasses import dataclass
from enum import Enum


class SliceState(Enum):
    """States during the slicing process"""
    INITIALIZING = "initializing"
    UPLOADING = "uploading"
    QUEUED = "queued"
    SLICING = "slicing"
    DOWNLOADING = "downloading"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class SliceResult:
    """Result of a slice operation"""
    success: bool
    output_path: Optional[Path] = None
    output_url: Optional[str] = None
    error: Optional[str] = None
    cost_time_ms: Optional[int] = None


class SoraGiri:
    """
    SoraGiri (空斬り) - Watermark Slicing Engine

    The Blade that cuts through Sora watermarks with precision.
    """

    # Kie.ai API endpoints
    BASE_URL = "https://api.kie.ai/api/v1"
    CREATE_ENDPOINT = f"{BASE_URL}/jobs/createTask"
    QUERY_ENDPOINT = f"{BASE_URL}/jobs/recordInfo"

    def __init__(self, api_key: str):
        """
        Initialize SoraGiri with API credentials.

        Args:
            api_key: Kie.ai API key
        """
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    async def slice(
        self,
        video_url: str,
        output_path: Optional[Path] = None,
        on_progress: Optional[Callable[[SliceState, str], None]] = None,
        max_attempts: int = 60,
        poll_interval: float = 2.0
    ) -> SliceResult:
        """
        Slice the watermark from a Sora video.

        Args:
            video_url: URL to the Sora video (must be publicly accessible)
            output_path: Optional path to save the output video
            on_progress: Optional callback for progress updates (state, message)
            max_attempts: Maximum polling attempts (default: 60 = 2 minutes)
            poll_interval: Seconds between status checks (default: 2.0)

        Returns:
            SliceResult with success status and output path/url
        """
        async def emit(state: SliceState, msg: str):
            if on_progress:
                result = on_progress(state, msg)
                # Handle both sync and async callbacks
                if inspect.iscoroutine(result):
                    await result

        try:
            async with aiohttp.ClientSession() as session:
                # Phase 1: Initialize the slice
                await emit(SliceState.INITIALIZING, "Unsheathing the blade...")
                task_id = await self._create_task(session, video_url)
                await emit(SliceState.QUEUED, f"Task locked: {task_id[:8]}...")

                # Phase 2: Poll for completion
                result_url = None
                cost_time = None

                for attempt in range(max_attempts):
                    await asyncio.sleep(poll_interval)

                    result = await self._query_task(session, task_id)
                    data = result.get("data", {})
                    state = data.get("state", "unknown")

                    if state == "success":
                        # Parse the result
                        result_json_str = data.get("resultJson", "{}")
                        result_json = json.loads(result_json_str)
                        result_urls = result_json.get("resultUrls", [])
                        cost_time = data.get("costTime")

                        if result_urls:
                            result_url = result_urls[0]
                            await emit(SliceState.SLICING, "Watermark severed.")
                            break
                        else:
                            return SliceResult(
                                success=False,
                                error="No output URL in response"
                            )

                    elif state == "fail":
                        error_msg = data.get("failMsg", "Unknown failure")
                        await emit(SliceState.FAILED, f"Blade shattered: {error_msg}")
                        return SliceResult(success=False, error=error_msg)

                    elif state in ("waiting", "queuing"):
                        await emit(SliceState.QUEUED, f"In queue... [{attempt + 1}/{max_attempts}]")

                    elif state == "generating":
                        await emit(SliceState.SLICING, f"Slicing... [{attempt + 1}/{max_attempts}]")

                    else:
                        await emit(SliceState.SLICING, f"Processing... [{attempt + 1}/{max_attempts}]")

                else:
                    # Loop exhausted without success
                    return SliceResult(
                        success=False,
                        error="Timeout: blade could not complete the cut"
                    )

                # Phase 3: Download if output path specified
                if output_path and result_url:
                    await emit(SliceState.DOWNLOADING, "Retrieving the clean cut...")
                    await self._download_video(session, result_url, output_path)
                    await emit(SliceState.COMPLETE, f"Saved to {output_path}")

                    return SliceResult(
                        success=True,
                        output_path=output_path,
                        output_url=result_url,
                        cost_time_ms=cost_time
                    )
                else:
                    await emit(SliceState.COMPLETE, "Slice complete.")
                    return SliceResult(
                        success=True,
                        output_url=result_url,
                        cost_time_ms=cost_time
                    )

        except Exception as e:
            await emit(SliceState.FAILED, str(e))
            return SliceResult(success=False, error=str(e))

    async def slice_to_bytes(
        self,
        video_url: str,
        on_progress: Optional[Callable[[SliceState, str], None]] = None,
        max_attempts: int = 60,
        poll_interval: float = 2.0
    ) -> tuple[bool, bytes | str]:
        """
        Slice watermark and return video as bytes (useful for Discord uploads).

        Returns:
            Tuple of (success, video_bytes or error_message)
        """
        result = await self.slice(
            video_url=video_url,
            output_path=None,
            on_progress=on_progress,
            max_attempts=max_attempts,
            poll_interval=poll_interval
        )

        if not result.success:
            return False, result.error or "Unknown error"

        # Download to bytes
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(result.output_url) as resp:
                    if resp.status == 200:
                        return True, await resp.read()
                    else:
                        return False, f"Download failed: HTTP {resp.status}"
        except Exception as e:
            return False, f"Download error: {e}"

    async def _create_task(self, session: aiohttp.ClientSession, video_url: str) -> str:
        """Submit video for watermark removal, returns task_id"""
        payload = {
            "model": "sora-watermark-remover",
            "input": {"video_url": video_url}
        }

        async with session.post(self.CREATE_ENDPOINT, headers=self.headers, json=payload) as resp:
            if resp.status == 429:
                raise Exception("Rate limited - the blade needs rest")

            data = await resp.json()

            if data.get("code") != 200:
                error_msg = data.get("message", "Unknown error")
                raise Exception(f"API Error: {error_msg}")

            return data["data"]["taskId"]

    async def _query_task(self, session: aiohttp.ClientSession, task_id: str) -> dict:
        """Check status of a watermark removal task"""
        params = {"taskId": task_id}

        async with session.get(self.QUERY_ENDPOINT, headers=self.headers, params=params) as resp:
            return await resp.json()

    async def _download_video(self, session: aiohttp.ClientSession, url: str, output_path: Path) -> None:
        """Download video to specified path"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Download failed: HTTP {resp.status}")

            with open(output_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(8192):
                    f.write(chunk)
