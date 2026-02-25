# Security Review (2025-02-25)

## Credentials & Secrets

- **API keys**: All from `os.getenv()` (OPENAI_API_KEY, GOOGLE_API_KEY). No hardcoded keys.
- **.env**: Listed in `.gitignore`. Never committed.
- **Tests**: Use placeholder values (`test_api_key`, `test_openai_key`).

## Privacy

- **Prompt logging**: `llm_processor.py` previously logged full prompts (including user text) at INFO. Fixed to log only prompt length at DEBUG.
- **Realtime text deltas**: Logged at DEBUG level with `repr(delta[:50])`; not exposed in production logs.

## Recommendations

- Run production with `LOG_LEVEL=WARNING` or `INFO` to avoid debug output.
- Rotate API keys if `.env` was ever committed or exposed.
