import json
import httpx
from app.config.settings import settings

async def stream_openai_response(messages: list):
    """
    Streams the response from Local Ollama or OpenAI using Server-Sent Events (SSE).
    """
    if settings.AI_PROVIDER == "openai":
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        try:
            stream = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                stream=True
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"[ERROR] OpenAI Error: {str(e)}"
        return

    # Default to Ollama
    ollama_url = f"{settings.OPENAI_API_BASE.rstrip('/')}/api/generate"
    model_name = settings.OPENAI_MODEL
    
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
        yield f"[ERROR] Failed to connect to Ollama at {ollama_url}. Make sure Ollama is running."
    except Exception as e:
        yield f"[ERROR] Ollama Error: {str(e)}"
