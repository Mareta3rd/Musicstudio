import pytest

import musicstudio.app as app_module


class HealthyProvider:
    name = "ace-step"

    async def health(self):
        return {"reachable": True, "status_code": 200, "response": {"status": "ok"}}


class BrokenProvider:
    name = "ace-step"

    async def health(self):
        raise RuntimeError("connection refused")


@pytest.mark.asyncio
async def test_provider_diagnostics_reports_healthy_provider(monkeypatch):
    monkeypatch.setattr(app_module, "provider", HealthyProvider())

    result = await app_module.provider_diagnostics()

    assert result["ok"] is True
    assert result["provider"] == "ace-step"
    assert result["reachable"] is True
    assert result["status_code"] == 200


@pytest.mark.asyncio
async def test_provider_diagnostics_reports_provider_failure(monkeypatch):
    monkeypatch.setattr(app_module, "provider", BrokenProvider())

    result = await app_module.provider_diagnostics()

    assert result == {
        "provider": "ace-step",
        "ok": False,
        "reachable": False,
        "error": "connection refused",
    }
