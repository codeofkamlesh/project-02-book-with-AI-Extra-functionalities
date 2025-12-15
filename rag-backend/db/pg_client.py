"""
PostgreSQL client for Neon database integration in the Physical AI & Humanoid Robotics RAG system.
Handles user profile retrieval and other database operations.
"""
import os
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import json
import asyncio


class PostgresClient:
    """
    Async PostgreSQL client for Neon database operations
    """

    def __init__(self):
        self.engine = None
        self.async_session = None

    async def initialize(self):
        """
        Initialize the async engine and session
        """
        database_url = os.getenv("NEON_DATABASE_URL")
        if not database_url:
            raise ValueError("NEON_DATABASE_URL environment variable is required")

        self.engine = create_async_engine(
            database_url,
            echo=False,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True
        )

        self.async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user profile from the database
        """
        if not self.async_session:
            await self.initialize()

        async with self.async_session() as session:
            query = text("""
                SELECT up.software_background, up.hardware_background, up.preferences
                FROM user_profiles up
                WHERE up.user_id = :user_id
            """)
            result = await session.execute(query, {"user_id": int(user_id)})
            row = result.fetchone()

            if row:
                return {
                    "software_background": row[0] if row[0] else {},
                    "hardware_background": row[1] if row[1] else {},
                    "preferences": row[2] if row[2] else {}
                }
            return None

    async def save_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """
        Save or update user profile in the database
        """
        if not self.async_session:
            await self.initialize()

        async with self.async_session() as session:
            async with session.begin():
                query = text("""
                    INSERT INTO user_profiles (user_id, software_background, hardware_background, preferences)
                    VALUES (:user_id, :software_background, :hardware_background, :preferences)
                    ON CONFLICT (user_id)
                    DO UPDATE SET
                        software_background = EXCLUDED.software_background,
                        hardware_background = EXCLUDED.hardware_background,
                        preferences = EXCLUDED.preferences,
                        updated_at = CURRENT_TIMESTAMP
                """)
                try:
                    await session.execute(
                        query,
                        {
                            "user_id": int(user_id),
                            "software_background": json.dumps(profile_data.get("software_background", {})),
                            "hardware_background": json.dumps(profile_data.get("hardware_background", {})),
                            "preferences": json.dumps(profile_data.get("preferences", {}))
                        }
                    )
                    await session.commit()
                    return True
                except Exception as e:
                    await session.rollback()
                    print(f"Error saving user profile: {str(e)}")
                    return False

    async def save_personalized_content(self, user_id: str, doc_path: str, mode: str, content: str) -> bool:
        """
        Save personalized content to the cache
        """
        if not self.async_session:
            await self.initialize()

        async with self.async_session() as session:
            async with session.begin():
                query = text("""
                    INSERT INTO personalized_docs (user_id, doc_path, mode, content)
                    VALUES (:user_id, :doc_path, :mode, :content)
                    ON CONFLICT (user_id, doc_path, mode)
                    DO UPDATE SET
                        content = EXCLUDED.content,
                        created_at = CURRENT_TIMESTAMP,
                        expires_at = CURRENT_TIMESTAMP + INTERVAL '1 day'
                """)
                try:
                    await session.execute(
                        query,
                        {
                            "user_id": int(user_id),
                            "doc_path": doc_path,
                            "mode": mode,
                            "content": content
                        }
                    )
                    await session.commit()
                    return True
                except Exception as e:
                    await session.rollback()
                    print(f"Error saving personalized content: {str(e)}")
                    return False

    async def get_personalized_content(self, user_id: str, doc_path: str, mode: str) -> Optional[str]:
        """
        Retrieve personalized content from cache
        """
        if not self.async_session:
            await self.initialize()

        async with self.async_session() as session:
            query = text("""
                SELECT content
                FROM personalized_docs
                WHERE user_id = :user_id AND doc_path = :doc_path AND mode = :mode
                AND expires_at > CURRENT_TIMESTAMP
            """)
            result = await session.execute(
                query,
                {"user_id": int(user_id), "doc_path": doc_path, "mode": mode}
            )
            row = result.fetchone()
            return row[0] if row else None

    async def save_translation(self, doc_path: str, target_language: str, content: str) -> bool:
        """
        Save translation to the cache
        """
        if not self.async_session:
            await self.initialize()

        async with self.async_session() as session:
            async with session.begin():
                query = text("""
                    INSERT INTO translations (doc_path, target_language, content, updated_at)
                    VALUES (:doc_path, :target_language, :content, CURRENT_TIMESTAMP)
                    ON CONFLICT (doc_path, target_language)
                    DO UPDATE SET
                        content = EXCLUDED.content,
                        updated_at = EXCLUDED.updated_at
                """)
                try:
                    await session.execute(
                        query,
                        {
                            "doc_path": doc_path,
                            "target_language": target_language,
                            "content": content
                        }
                    )
                    await session.commit()
                    return True
                except Exception as e:
                    await session.rollback()
                    print(f"Error saving translation: {str(e)}")
                    return False

    async def get_translation(self, doc_path: str, target_language: str) -> Optional[str]:
        """
        Retrieve translation from cache
        """
        if not self.async_session:
            await self.initialize()

        async with self.async_session() as session:
            query = text("""
                SELECT content
                FROM translations
                WHERE doc_path = :doc_path AND target_language = :target_language
            """)
            result = await session.execute(
                query,
                {"doc_path": doc_path, "target_language": target_language}
            )
            row = result.fetchone()
            return row[0] if row else None


# Global instance
postgres_client = PostgresClient()


# Convenience functions for use in API endpoints
async def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to get user profile
    """
    return await postgres_client.get_user_profile(user_id)


async def save_user_profile(user_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Convenience function to save user profile
    """
    return await postgres_client.save_user_profile(user_id, profile_data)


async def save_personalized_content(user_id: str, doc_path: str, mode: str, content: str) -> bool:
    """
    Convenience function to save personalized content
    """
    return await postgres_client.save_personalized_content(user_id, doc_path, mode, content)


async def get_personalized_content(user_id: str, doc_path: str, mode: str) -> Optional[str]:
    """
    Convenience function to get personalized content
    """
    return await postgres_client.get_personalized_content(user_id, doc_path, mode)


async def save_translation(doc_path: str, target_language: str, content: str) -> bool:
    """
    Convenience function to save translation
    """
    return await postgres_client.save_translation(doc_path, target_language, content)


async def get_translation(doc_path: str, target_language: str) -> Optional[str]:
    """
    Convenience function to get translation
    """
    return await postgres_client.get_translation(doc_path, target_language)


# Initialize the client when module is imported
async def init_db():
    """
    Initialize the database client
    """
    await postgres_client.initialize()


# Example usage
if __name__ == "__main__":
    import asyncio

    async def test_db():
        await init_db()

        # Test user profile operations
        test_profile = {
            "software_background": {"level": "intermediate", "languages": ["Python", "C++"]},
            "hardware_background": {"experience": "ROS experience", "platforms": ["TurtleBot", "UR5"]},
            "preferences": {"learning_style": "hands-on", "complexity": "moderate"}
        }

        success = await save_user_profile("123", test_profile)
        print(f"Saved profile: {success}")

        retrieved = await get_user_profile("123")
        print(f"Retrieved profile: {retrieved}")

        # Test personalization cache
        success = await save_personalized_content("123", "/docs/test.md", "simpler", "Simplified content")
        print(f"Saved personalized content: {success}")

        retrieved = await get_personalized_content("123", "/docs/test.md", "simpler")
        print(f"Retrieved personalized content: {retrieved}")

        # Test translation cache
        success = await save_translation("/docs/test.md", "ur", "Urdu translation")
        print(f"Saved translation: {success}")

        retrieved = await get_translation("/docs/test.md", "ur")
        print(f"Retrieved translation: {retrieved}")

    # Run the test
    asyncio.run(test_db())