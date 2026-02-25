"""Tests for config module."""
import config


def test_openai_realtime_model_is_string():
    assert isinstance(config.OPENAI_REALTIME_MODEL, str)
    assert len(config.OPENAI_REALTIME_MODEL) > 0


def test_openai_realtime_modalities_is_list():
    assert isinstance(config.OPENAI_REALTIME_MODALITIES, list)
    assert "text" in config.OPENAI_REALTIME_MODALITIES
