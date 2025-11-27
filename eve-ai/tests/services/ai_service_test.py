import json
import pytest
from unittest.mock import MagicMock

from ollama import ChatResponse
from app.models.schemas import Character
from app.services.ai_service import AI_Service


@pytest.fixture
def character():
    return Character(
        name="Eve",
        description="an AI companion",
        personality="curious and helpful"
    )


@pytest.fixture
def cfg_mock(mocker):
    """Mock runtime config for local mode."""
    cfg = mocker.MagicMock()
    cfg.mode = "local"
    cfg.model_name = "llama3.1"
    cfg.temperature = 0.7
    cfg.max_tokens = 150
    cfg.gpu_layers = 35
    return cfg


@pytest.fixture
def ai_service():
    return AI_Service()


# ------------------------------------------------------------------
# Happy path
# ------------------------------------------------------------------
def test_generate_response_local_valid_json(ai_service, character, cfg_mock, mocker):
    mocker.patch("app.services.ai_service.config_service.get_runtime_config", return_value=cfg_mock)

    fake_ollama_response = MagicMock()
    fake_ollama_response.message.content = json.dumps(
        {"response": "Hi there!", "emotion": "happy"}
    )
    mocker.patch("app.services.ai_service.chat", return_value=fake_ollama_response)
    mocker.patch("time.time", side_effect=[100.0, 101.5])  # 1.5 s generation time

    messages = [{"role": "user", "content": "Hello"}]
    text, emotion, elapsed = ai_service.generate_response(messages, character)

    assert text == "Hi there!"
    assert emotion == "happy"
    assert elapsed == 1.5


# ------------------------------------------------------------------
# Invalid JSON -> fallback
# ------------------------------------------------------------------
def test_generate_response_invalid_json_fallback(ai_service, character, cfg_mock, mocker):
    mocker.patch("app.services.ai_service.config_service.get_runtime_config", return_value=cfg_mock)

    fake_ollama_response = MagicMock()
    fake_ollama_response.message.content = "not json at all"
    mocker.patch("app.services.ai_service.chat", return_value=fake_ollama_response)
    mocker.patch("time.time", side_effect=[100.0, 100.2])

    messages = [{"role": "user", "content": "Hello"}]
    text, emotion, elapsed = ai_service.generate_response(messages, character)

    assert text == "I had trouble formatting my response correctly."
    assert emotion == "neutral"
    assert elapsed == pytest.approx(0.2)


# ------------------------------------------------------------------
# Ollama raises → wrapped in generic error message
# ------------------------------------------------------------------
def test_generate_response_ollama_exception(ai_service, character, cfg_mock, mocker):
    mocker.patch("app.services.ai_service.config_service.get_runtime_config", return_value=cfg_mock)
    mocker.patch("app.services.ai_service.chat", side_effect=Exception("Ollama crashed"))
    mocker.patch("time.time", side_effect=[100.0, 100.1])

    messages = [{"role": "user", "content": "Hello"}]
    text, emotion, elapsed = ai_service.generate_response(messages, character)

    assert "Error generating response: Ollama crashed" in text
    assert emotion == "neutral"
    assert elapsed == pytest.approx(0.1)
