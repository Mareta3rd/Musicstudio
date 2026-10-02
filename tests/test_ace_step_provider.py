import json

import httpx
import pytest

from musicstudio.models import GenerationRequest, JobStatus
from musicstudio.providers.ace_step import AceStepProvider


@pytest.mark.asyncio
async def test_ace_step_submit_uses_release_task_contract():
    seen = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["url"] = str(request.url)
        seen["json"] = json.loads(request.content)
        return httpx.Response(200, json={"code": 200, "data": {"task_id": "task-123"}})

    provider = AceStepProvider("http://ace.local", transport=httpx.MockTransport(handler))
    task_id = await provider.submit(
        GenerationRequest(
            prompt="warm Mediterranean night",
            lyrics="[Verse]\nLa noche respira",
            duration=42,
            bpm=112,
            key_scale="Am",
            vocal_language="es",
            seed=77,
        )
    )

    assert task_id == "task-123"
    assert seen["method"] == "POST"
    assert seen["url"] == "http://ace.local/release_task"
    assert seen["json"]["prompt"] == "warm Mediterranean night"
    assert seen["json"]["audio_format"] == "mp3"
    assert seen["json"]["audio_duration"] == 42
    assert seen["json"]["use_random_seed"] is False
    assert seen["json"]["seed"] == 77


@pytest.mark.asyncio
async def test_ace_step_status_normalizes_completed_result():
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/query_result"
        return httpx.Response(
            200,
            json={
                "code": "200",
                "data": [
                    {
                        "status": 1,
                        "result": json.dumps(
                            [
                                {
                                    "prompt": "warm Mediterranean night",
                                    "file": "/tmp/song.mp3",
                                    "seed_value": 77,
                                    "metas": {
                                        "duration": 42,
                                        "bpm": 112,
                                        "keyscale": "Am",
                                        "timesignature": "4/4",
                                    },
                                }
                            ]
                        ),
                    }
                ],
            },
        )

    provider = AceStepProvider("http://ace.local", transport=httpx.MockTransport(handler))
    status = await provider.status("task-123")

    assert status.status == JobStatus.completed
    assert status.audio_path == "/tmp/song.mp3"
    assert status.title == "warm Mediterranean night"
    assert status.metadata == {
        "duration": 42,
        "bpm": 112,
        "key_scale": "Am",
        "time_signature": "4/4",
        "seed": 77,
        "lm_model": None,
        "dit_model": None,
    }


@pytest.mark.asyncio
async def test_ace_step_download_audio_uses_normalized_audio_url():
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/audio"
        assert request.url.params["path"] == "/tmp/song.mp3"
        return httpx.Response(200, content=b"fake-mp3", headers={"content-type": "audio/mpeg"})

    provider = AceStepProvider("http://ace.local", transport=httpx.MockTransport(handler))
    content, media_type = await provider.download_audio("/tmp/song.mp3")

    assert content == b"fake-mp3"
    assert media_type == "audio/mpeg"


@pytest.mark.asyncio
async def test_ace_step_failed_status_preserves_provider_error():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"code": 200, "data": [{"status": 2, "error": "GPU out of memory"}]},
        )

    provider = AceStepProvider("http://ace.local", transport=httpx.MockTransport(handler))
    status = await provider.status("task-123")

    assert status.status == JobStatus.failed
    assert status.error == "GPU out of memory"
