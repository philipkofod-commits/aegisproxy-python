import os
import httpx
import logging
from typing import Optional, Dict

__version__ = "0.1.0"

# Set up logging
logger = logging.getLogger("aegis")

# The default Aegis Proxy endpoint
DEFAULT_AEGIS_URL = "https://api.aegisproxy.com"

# The original methods to avoid infinite recursion and allow unpatching
_originals = {
    "httpx_client_send": httpx.Client.send,
    "httpx_async_client_send": httpx.AsyncClient.send,
}

# Domain to Provider Path mapping
PROVIDER_MAP = {
    "openai.com": "/v1/openai",
    "anthropic.com": "/v1/anthropic",
    "googleapis.com": "/v1/google",
    "groq.com": "/v1/groq",
    "mistral.ai": "/v1/mistral",
    "together.xyz": "/v1/together",
    "cohere.com": "/v1/cohere",
    "perplexity.ai": "/v1/perplexity",
}

class AegisNetworkHook:
    def __init__(self, key: str, proxy_url: str, debug: bool = False, extra_providers: Optional[Dict[str, str]] = None):
        self.key = key
        self.proxy_url = proxy_url.rstrip("/")
        self.debug = debug
        # Merge default providers with any user-supplied extras
        self.provider_map = {**PROVIDER_MAP, **(extra_providers or {})}
        self.managed_domains = list(self.provider_map.keys())

    def __repr__(self):
        """Prevent API key from leaking in logs/tracebacks."""
        return f"AegisNetworkHook(proxy_url={self.proxy_url!r}, debug={self.debug})"

    def _log(self, msg: str):
        if self.debug:
            logger.info(f"[Aegis] {msg}")

    def _get_provider_path(self, host: str) -> Optional[str]:
        for domain, path in self.provider_map.items():
            if host.endswith(domain):
                return path
        return None

    def _transform_request(self, request: httpx.Request) -> httpx.Request:
        provider_path = self._get_provider_path(request.url.host)
        
        if provider_path:
            self._log(f"Intercepting request to {request.url.host}")
            original_path = request.url.path
            # Preserve query string parameters
            query = request.url.query
            new_url_str = f"{self.proxy_url}{provider_path}{original_path}"
            if query:
                new_url_str += f"?{query.decode() if isinstance(query, bytes) else query}"
            
            # Inject headers while preserving originals
            headers = dict(request.headers)
            headers["x-aegis-key"] = self.key
            headers["x-aegis-sdk"] = f"python/{__version__}"
            
            return httpx.Request(
                method=request.method,
                url=new_url_str,
                headers=headers,
                content=request.read(),
                extensions=request.extensions
            )
            
        return request

    def patched_send(self, client: httpx.Client, request: httpx.Request, *args, **kwargs) -> httpx.Response:
        if self._get_provider_path(request.url.host):
            request = self._transform_request(request)
        return _originals["httpx_client_send"](client, request, *args, **kwargs)

    async def patched_async_send(self, client: httpx.AsyncClient, request: httpx.Request, *args, **kwargs) -> httpx.Response:
        if self._get_provider_path(request.url.host):
            request = self._transform_request(request)
        return await _originals["httpx_async_client_send"](client, request, *args, **kwargs)

_hook_installed = False

def protect(aegis_key: Optional[str] = None, proxy_url: str = DEFAULT_AEGIS_URL, debug: bool = False, extra_providers: Optional[Dict[str, str]] = None):
    """
    Initializes the Aegis SDK, globally monkey-patching HTTP libraries.
    
    Args:
        aegis_key: Your AegisProxy API key. Falls back to AEGIS_API_KEY env var.
        proxy_url: Custom Aegis endpoint.
        debug: Enable verbose logging for debugging.
        extra_providers: Additional provider domain mappings, e.g. {"api.deepseek.com": "/v1/deepseek"}.
    """
    global _hook_installed
    if _hook_installed:
        return

    key = aegis_key or os.getenv("AEGIS_API_KEY")
    if not key:
        raise ValueError("Aegis API key is required. Pass aegis_key to protect() or set AEGIS_API_KEY environment variable.")
        
    hook = AegisNetworkHook(key=key, proxy_url=proxy_url, debug=debug, extra_providers=extra_providers)
    
    # Monkey-patch httpx
    httpx.Client.send = lambda self, req, *args, **kwargs: hook.patched_send(self, req, *args, **kwargs)
    httpx.AsyncClient.send = lambda self, req, *args, **kwargs: hook.patched_async_send(self, req, *args, **kwargs)
    
    # Optional: Patch 'requests' if it exists
    try:
        import requests
        from requests.adapters import HTTPAdapter
        
        _original_request_send = HTTPAdapter.send
        
        def patched_requests_send(adapter, request, **kwargs):
            parsed_url = httpx.URL(request.url)
            provider_path = hook._get_provider_path(parsed_url.host)
            
            if provider_path:
                hook._log(f"Intercepting requests-library call to {parsed_url.host}")
                new_url = f"{proxy_url.rstrip('/')}{provider_path}{parsed_url.path}"
                if parsed_url.query:
                    new_url += f"?{parsed_url.query.decode()}"
                
                request.url = new_url
                request.headers["x-aegis-key"] = key
                
            return _original_request_send(adapter, request, **kwargs)
            
        HTTPAdapter.send = patched_requests_send
        hook._log("Patched 'requests' library via HTTPAdapter.")
    except ImportError:
        pass

    _hook_installed = True
    logger.info("🛡️  AegisProxy activated: Global network hooks installed.")

