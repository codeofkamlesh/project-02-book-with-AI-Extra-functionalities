from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import asyncio
from fastapi import Request

# Import using absolute imports for the package
from rag_backend.db.pg_client import save_user_profile as db_save_user_profile, get_user_profile as db_get_user_profile

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

@router.post("/auth-callback")
async def auth_callback():
    """
    Authentication callback endpoint
    """
    # In a real implementation, this would verify the authentication token
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
async def get_current_user(request: Request):
    """
    Return current user's profile and information
    """
    try:
        # For now, we'll use a simple mock approach that works with the system
        # In a real implementation, this would extract user info from a proper auth system

        # Check for an auth token or session in the request
        # This is a simplified approach for the demo
        auth_header = request.headers.get("authorization")
        if not auth_header:
            # No authentication, return default response
            return {
                "user": {
                    "id": "anonymous",
                    "email": "",
                    "name": "Anonymous User"
                },
                "profile": {
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
            }

        # Mock user extraction based on auth token
        # In a real implementation, you would validate the token and extract user info
        user_id = "current_user_id"  # Would be extracted from validated token in real implementation

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
                "id": user_id,
                "email": "user@example.com",  # Would come from validated session
                "name": "Test User"  # Would come from validated session
            },
            "profile": profile
        }
    except Exception as e:
        print(f"Error getting current user: {str(e)}")
        # Return a default response if there's an error
        return {
            "user": {
                "id": "unknown",
                "email": "",
                "name": ""
            },
            "profile": {
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
        }