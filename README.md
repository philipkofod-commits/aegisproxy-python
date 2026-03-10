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

## Supported Providers (built-in)

The following providers are intercepted automatically — no configuration needed:

- **OpenAI** (`api.openai.com`)
- **Anthropic** (`api.anthropic.com`)
- **Google Gemini** (`generativelanguage.googleapis.com`)
- **Groq** (`api.groq.com`)
- **Mistral** (`api.mistral.ai`)
- **Together AI** (`api.together.xyz`)
- **Cohere** (`api.cohere.com`)
- **Perplexity** (`api.perplexity.ai`)

## Advanced Configuration

```python
aegis.protect(
    aegis_key="your_api_key",
    proxy_url="https://api.aegisproxy.com",
    debug=True,  # See what's being intercepted
    extra_providers={  # Add providers not yet in the default list
        "api.deepseek.com": "/v1/deepseek"
    }
)
```

## Security Features

Aegis handles the full spectrum of Agentic Security:

- **Prompt Injection Defense**: Blocks malicious system-instruction overrides and indirect injections.
- **RBAC & Privilege Control**: Enforces strict boundaries on what tools and actions an agent can execute.
- **Semantic Loop Detection**: Detects and halts unproductive logic loops that waste tokens and resources.
- **SSRF Protection**: Prevents agents from accessing internal network metadata or local resources.
- **PII Redaction (DLP)**: Automatically identifies and masks sensitive data in both input and output.
- **Supply Chain Firewall**: Validates package installs (npm/pip) against our reputation registry to prevent slopsquatting.

## License

MIT
