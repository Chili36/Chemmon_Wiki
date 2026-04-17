from __future__ import annotations

import pytest

from wiki_api.providers import resolve_provider, ProviderError


def test_explicit_provider_model():
    assert resolve_provider("anthropic/claude-sonnet-4-6") == ("anthropic", "claude-sonnet-4-6")


def test_explicit_provider_nested_model():
    assert resolve_provider("openrouter/deepseek/deepseek-r1") == ("openrouter", "deepseek/deepseek-r1")


def test_bare_claude_resolves_to_anthropic():
    assert resolve_provider("claude-sonnet-4-6") == ("anthropic", "claude-sonnet-4-6")


def test_bare_gpt_resolves_to_openai():
    assert resolve_provider("gpt-5.4-mini") == ("openai", "gpt-5.4-mini")


def test_bare_gemini_resolves_to_google():
    assert resolve_provider("gemini-2.5-pro") == ("google", "gemini-2.5-pro")


def test_bare_mistral_resolves_to_mistral():
    assert resolve_provider("mistral-large") == ("mistral", "mistral-large")


def test_lmstudio_provider():
    assert resolve_provider("lmstudio/llama-3-8b") == ("lmstudio", "llama-3-8b")


def test_unknown_bare_name_raises():
    with pytest.raises(ProviderError, match="provider/model"):
        resolve_provider("some-unknown-model")


def test_unknown_provider_raises():
    with pytest.raises(ProviderError, match="nope"):
        resolve_provider("nope/some-model")


from unittest.mock import patch

from wiki_api.providers import client_for_model, clear_client_cache
from openai import OpenAI


def test_client_for_model_returns_openai_instance():
    clear_client_cache()
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        client, model_id = client_for_model("openai/gpt-5.4-mini")
        assert model_id == "gpt-5.4-mini"
        assert isinstance(client, OpenAI)


def test_client_for_model_lmstudio_no_key_needed():
    clear_client_cache()
    client, model_id = client_for_model("lmstudio/llama-3-8b")
    assert model_id == "llama-3-8b"
    assert isinstance(client, OpenAI)


def test_client_for_model_missing_key_raises():
    clear_client_cache()
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ProviderError, match="ANTHROPIC_API_KEY"):
            client_for_model("anthropic/claude-sonnet-4-6")


def test_client_cache_reuses_instance():
    clear_client_cache()
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        c1, _ = client_for_model("openai/gpt-5.4-mini")
        c2, _ = client_for_model("openai/gpt-4o")
        assert c1 is c2
