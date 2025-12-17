# User models for authentication
from pydantic import BaseModel
from typing import Optional, Dict, Any

class User(BaseModel):
    """
    Basic user model
    """
    id: str
    email: str
    name: Optional[str] = None
    created_at: Optional[str] = None

class ExtendedUser(User):
    """
    Extended user model with software/hardware background fields
    """
    software_level: Optional[str] = 'beginner'
    software_stack: Optional[str] = ''
    hardware_level: Optional[str] = 'none'
    hardware_platforms: Optional[str] = ''

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"

class UserDict(Dict[str, Any]):
    """
    Type definition for user dictionary
    """
    pass