# Authentication configuration for FastAPI backend
from sqlalchemy.ext.asyncio import create_async_engine
from ..db.pg_client import save_user_profile
import os
import asyncio

# Initialize database connection for Neon Postgres
DATABASE_URL = os.getenv("NEON_DATABASE_URL")

# Simple authentication configuration (placeholder for real auth system)
class AuthConfig:
    SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Mock function to save extended profile for new users
async def save_extended_profile(user_data):
    """
    Save extended profile information for new users
    """
    try:
        # Create default profile with software/hardware background
        profile_data = {
            "software_background": {
                "level": user_data.get('software_level', 'beginner'),
                "stack": user_data.get('software_stack', ''),
            },
            "hardware_background": {
                "level": user_data.get('hardware_level', 'none'),
                "platforms": user_data.get('hardware_platforms', ''),
            },
            "preferences": {}
        }

        # Save the profile to the database
        user_id = user_data.get('id', 'unknown')
        success = await save_user_profile(str(user_id), profile_data)
        if success:
            print(f"Extended profile saved for user: {user_data.get('email', 'unknown')}")
        else:
            print(f"Failed to save extended profile for user: {user_data.get('email', 'unknown')}")
    except Exception as e:
        print(f"Error saving extended profile: {str(e)}")