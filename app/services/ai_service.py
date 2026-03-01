from groq import AsyncGroq
from app.config.settings import settings

async def stream_groq_response(messages: list):
    """
    Streams the response from Groq using Server-Sent Events (SSE).
    """
    client = AsyncGroq(api_key=settings.GROQ_API_KEY)
    
    try:
        stream = await client.chat.completions.create(
            messages=messages,
            model=settings.GROQ_MODEL,
            temperature=0.7,
            stream=True,
        )
        
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    except Exception as e:
        yield f"[ERROR] Groq API Error: {str(e)}"
