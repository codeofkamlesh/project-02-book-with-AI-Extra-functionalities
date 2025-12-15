from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import asyncio
from ...db.pg_client import save_user_profile as db_save_user_profile, get_user_profile as db_get_user_profile

router = APIRouter()

class ProfileRequest(BaseModel):
    user_id: str
    software_background: dict
    hardware_background: dict
    preferences: Optional[dict] = {}

class ProfileResponse(BaseModel):
    user_id: str
    software_background: dict
    hardware_background: dict
    preferences: dict
    created_at: str

@router.post("/better-auth-callback")
async def better_auth_callback():
    """
    Verify Better-Auth token and create session
    """
    # In a real implementation, this would verify the Better-Auth token
    # For now, returning success
    return {"status": "verified"}

@router.post("/profile")
async def save_user_profile(request: ProfileRequest):
    """
    Save user profile with software/hardware background to Neon Postgres
    """
    try:
        # Save profile to database
        success = await db_save_user_profile(
            request.user_id,
            {
                "software_background": request.software_background,
                "hardware_background": request.hardware_background,
                "preferences": request.preferences
            }
        )

        if not success:
            raise HTTPException(status_code=500, detail="Failed to save profile to database")

        return ProfileResponse(
            user_id=request.user_id,
            software_background=request.software_background,
            hardware_background=request.hardware_background,
            preferences=request.preferences or {},
            created_at="2025-12-10T17:47:00Z"  # Current timestamp
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile saving failed: {str(e)}")

@router.get("/me")
async def get_current_user():
    """
    Return current user's profile and information
    """
    # This would retrieve the current user's profile from the database
    # For now, return a mock user profile
    # In a real implementation, we would extract the user_id from the auth token
    user_id = "12345"  # This would come from the auth token in practice
    profile = await db_get_user_profile(user_id)

    if not profile:
        # Return default profile if not found
        profile = {
            "software_background": {
                "level": "beginner",
                "languages": ["Python"]
            },
            "hardware_background": {
                "experience": "none",
                "platforms": []
            },
            "preferences": {
                "learning_style": "visual",
                "complexity": "moderate"
            }
        }

    return {
        "user": {
            "id": f"user_{user_id}",
            "email": "user@example.com",  # Would come from auth system
            "name": "Test User"  # Would come from auth system
        },
        "profile": profile
    }