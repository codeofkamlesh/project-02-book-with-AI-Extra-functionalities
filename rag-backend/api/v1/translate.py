from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ...agents.openai_agent_integration import OpenAIAgent
from ...db.pg_client import get_translation, save_translation

router = APIRouter()

class TranslateRequest(BaseModel):
    doc_path: str
    text: str
    target_language: str = "ur"  # Default to Urdu

class TranslateResponse(BaseModel):
    original_doc_path: str
    original_text: str
    target_language: str
    translated_text: str
    timestamp: datetime

@router.post("/translate/urdu", response_model=TranslateResponse)
async def translate_to_urdu_endpoint(request: TranslateRequest):
    """
    Translate English text to Urdu
    """
    try:
        # Check if translation is already cached
        cached_translation = await get_translation(request.doc_path, request.target_language)

        if cached_translation and cached_translation == request.text[:100]:  # Simple check
            # In a real implementation, we'd need a better way to match the exact text
            pass
        else:
            # Use the OpenAI agent to translate the content
            agent = OpenAIAgent()
            translated_text = await agent.translate_to_urdu(request.text)

            # Cache the translation
            await save_translation(request.doc_path, request.target_language, translated_text)
            request.text = translated_text

        return TranslateResponse(
            original_doc_path=request.doc_path,
            original_text=request.text,
            target_language=request.target_language,
            translated_text=request.text,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

# Additional endpoint for translating any language
@router.post("/translate", response_model=TranslateResponse)
async def translate_endpoint(request: TranslateRequest):
    """
    Translate text to target language (currently supports Urdu)
    """
    if request.target_language.lower() != "ur":
        raise HTTPException(status_code=400, detail="Currently only Urdu translation is supported")

    return await translate_to_urdu_endpoint(request)