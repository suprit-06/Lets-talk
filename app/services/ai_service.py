import json
import httpx
from app.config.settings import settings

async def stream_openai_response(messages: list):
    """
    Streams the response from Local Ollama using Server-Sent Events (SSE).
    Expected messages format: [{"role": "user", "content": "..."}, ...]
    """
    ollama_url = f"{settings.OPENAI_API_BASE.rstrip('/')}/api/generate" if hasattr(settings, 'OPENAI_API_BASE') and settings.OPENAI_API_BASE else "http://localhost:11434/api/generate"
    model_name = settings.OPENAI_MODEL if settings.OPENAI_MODEL else "llama3"
    
    # Re-build prompt manually for generic generate endpoint instead of Chat structure
    prompt = ""
    for msg in messages:
        if msg["role"] == "system":
            prompt += f"{msg['content']}\n\n"
        elif msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"Assistant: {msg['content']}\n"
            
    prompt += "Assistant: "
            
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": True
    }
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream('POST', ollama_url, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if 'response' in data:
                                yield data['response']
                        except json.JSONDecodeError:
                            continue
    except httpx.ConnectError:
        yield "[ERROR] Failed to connect to Ollama. Make sure the Ollama app is running locally (http://localhost:11434)."
    except Exception as e:
        yield f"[ERROR] Failed to fetch response: {str(e)}"
