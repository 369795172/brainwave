import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global configuration for OpenAI realtime model
OPENAI_REALTIME_MODEL = os.getenv("OPENAI_REALTIME_MODEL", "gpt-realtime-mini-2025-12-15")

# Modalities for WebSocket realtime (text-only output by default)
OPENAI_REALTIME_MODALITIES = os.getenv("OPENAI_REALTIME_MODALITIES", "text").split(",")

