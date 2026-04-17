from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from openai import OpenAI


class ProviderError(ValueError):
    pass


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    base_url: str | None
    key_env: str | None


PROVIDERS: dict[str, ProviderConfig] = {
    "openai": ProviderConfig(
        name="openai",
        base_url=None,
        key_env="OPENAI_API_KEY",
    ),
    "anthropic": ProviderConfig(
        name="anthropic",
        base_url="https://api.anthropic.com/v1/",
        key_env="ANTHROPIC_API_KEY",
    ),
    "google": ProviderConfig(
        name="google",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        key_env="GOOGLE_API_KEY",
    ),
    "mistral": ProviderConfig(
        name="mistral",
        base_url="https://api.mistral.ai/v1",
        key_env="MISTRAL_API_KEY",
    ),
    "openrouter": ProviderConfig(
        name="openrouter",
        base_url="https://openrouter.ai/api/v1",
        key_env="OPENROUTER_API_KEY",
    ),
    "lmstudio": ProviderConfig(
        name="lmstudio",
        base_url="http://localhost:1234/v1",
        key_env=None,
    ),
}

_BARE_PREFIX_MAP: list[tuple[str, str]] = [
    ("claude-", "anthropic"),
    ("gpt-", "openai"),
    ("gemini-", "google"),
    ("mistral-", "mistral"),
]

_client_cache: dict[str, OpenAI] = {}


def resolve_provider(model_str: str) -> tuple[str, str]:
    if "/" in model_str:
        provider_name, model_id = model_str.split("/", 1)
        if provider_name not in PROVIDERS:
            raise ProviderError(
                f"Unknown provider '{provider_name}'. "
                f"Known providers: {', '.join(sorted(PROVIDERS))}."
            )
        return provider_name, model_id

    for prefix, provider_name in _BARE_PREFIX_MAP:
        if model_str.startswith(prefix):
            return provider_name, model_str

    raise ProviderError(
        f"Cannot infer provider from bare model name '{model_str}'. "
        f"Use provider/model format (e.g., anthropic/{model_str})."
    )


def client_for_model(model_str: str) -> tuple[OpenAI, str]:
    provider_name, model_id = resolve_provider(model_str)
    if provider_name in _client_cache:
        return _client_cache[provider_name], model_id

    cfg = PROVIDERS[provider_name]
    api_key: str | None = None
    if cfg.key_env:
        api_key = os.environ.get(cfg.key_env)
        if not api_key:
            raise ProviderError(
                f"{cfg.key_env} is not set (required for provider '{provider_name}')"
            )

    kwargs: dict[str, Any] = {}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    if api_key:
        kwargs["api_key"] = api_key
    else:
        kwargs["api_key"] = "not-needed"

    client = OpenAI(**kwargs)
    _client_cache[provider_name] = client
    return client, model_id


def clear_client_cache() -> None:
    _client_cache.clear()


def normalize_usage(usage: Any, finish_reason: str | None) -> dict[str, int | str | None]:
    if usage is None:
        return {
            "stop_reason": finish_reason,
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
            "total_tracked_tokens": 0,
        }
    input_tokens = int(getattr(usage, "prompt_tokens", 0) or getattr(usage, "input_tokens", 0) or 0)
    output_tokens = int(getattr(usage, "completion_tokens", 0) or getattr(usage, "output_tokens", 0) or 0)
    cache_creation = int(getattr(usage, "cache_creation_input_tokens", 0) or 0)
    cache_read = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
    return {
        "stop_reason": finish_reason,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_creation_input_tokens": cache_creation,
        "cache_read_input_tokens": cache_read,
        "total_tracked_tokens": input_tokens + output_tokens + cache_creation + cache_read,
    }
