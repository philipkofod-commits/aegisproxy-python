# AegisProxy Python SDK 🛡️

The official Python SDK for [AegisProxy](https://aegisproxy.com), the zero-trust firewall for autonomous agents.

## Installation

```bash
pip install aegis-proxy
```

## Quick Start

Just add one line at the top of your agent's entry point. Aegis will automatically intercept calls to LLM providers (OpenAI, Anthropic, Gemini, etc.) and route them through your secure proxy.

```python
import aegis
aegis.protect()

# Now use your favorite LLM client as usual
import openai
client = openai.OpenAI()
# This request is now protected by Aegis!
response = client.chat.completions.create(...)
```

## Features

- **Zero-Code Integration**: Automatically patches `httpx` and `requests` libraries.
- **Provider Auto-Detection**: Supports OpenAI, Anthropic, Google Gemini, Groq, Mistral, and more.
- **Environment Driven**: Reads your `AEGIS_API_KEY` from environment variables by default.

## Advanced Configuration

```python
aegis.protect(
    aegis_key="your_api_key",
    proxy_url="https://api.aegisproxy.com",
    debug=True  # See what's being intercepted
)
```

## Security

Aegis handles:
- **Prompt Injection Defense**: Blocks malicious system-instruction overrides.
- **PII Redaction**: Prevents sensitive data from leaking into LLM logs.
- **Supply Chain Protection**: Validates package installations during agent runtime.

## License

MIT
