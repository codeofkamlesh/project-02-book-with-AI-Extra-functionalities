"""
OpenAI Agent Integration for the Physical AI & Humanoid Robotics RAG system.
Handles OpenAI API calls for RAG, personalization, and translation.
"""
import asyncio
import os
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from pydantic import BaseModel


class OpenAIAgent:
    """
    Integration layer for OpenAI API calls including RAG, personalization, and translation
    """

    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def generate_rag_response(
        self,
        query: str,
        context: str,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a RAG response based on query and context
        """
        try:
            # Customize prompt based on user profile if available
            if user_profile:
                complexity_modifier = self._get_complexity_modifier(user_profile)
                prompt_instruction = f"Answer the question considering the user has a {complexity_modifier} background in robotics and AI."
            else:
                prompt_instruction = "Answer the question based on the provided context."

            system_message = f"""You are an expert assistant for the Physical AI & Humanoid Robotics book. {prompt_instruction}

Provide accurate answers based solely on the provided context. Do not hallucinate or provide information not present in the context. If the answer is not available in the context, say so explicitly.

Context:
{context}
"""

            user_message = f"Question: {query}\n\nProvide a comprehensive answer based on the context above. Include relevant citations to the source materials when possible."

            response = await self.client.chat.completions.create(
                model="gpt-4o",  # Using GPT-4o for balanced performance and cost
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,  # Lower temperature for more consistent, fact-based answers
                max_tokens=1000
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating RAG response: {str(e)}")
            raise

    async def personalize_content(
        self,
        content: str,
        user_profile: Dict[str, Any],
        mode: str = "simpler"
    ) -> str:
        """
        Personalize content based on user profile and requested mode
        """
        try:
            # Determine personalization instruction based on mode
            mode_instructions = {
                "simpler": "Rewrite the content to be more accessible for beginners, with simplified explanations and more examples.",
                "advanced": "Rewrite the content to be more technical and detailed, with advanced concepts and deeper explanations.",
                "visual": "Rewrite the content to emphasize visual elements and diagrams, with more descriptive explanations of visual components.",
                "code-heavy": "Rewrite the content to include more code examples, implementation details, and technical specifications."
            }

            personalization_instruction = mode_instructions.get(mode, mode_instructions["simpler"])

            system_message = f"""You are an expert content personalization assistant for the Physical AI & Humanoid Robotics book.
{personalization_instruction}

The user profile indicates:
- Software background: {user_profile.get('software_background', {})}
- Hardware background: {user_profile.get('hardware_background', {})}

Maintain all original facts and information from the source content, but adapt the presentation, complexity, and examples to match the user's background and the requested mode.
"""

            user_message = f"""Source content:\n{content}\n\nRewrite the content according to the personalization requirements while preserving all original facts and information."""

            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.5,  # Slightly higher for creative rewriting
                max_tokens=2000
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error personalizing content: {str(e)}")
            raise

    async def translate_to_urdu(
        self,
        text: str
    ) -> str:
        """
        Translate English text to Urdu
        """
        try:
            system_message = """You are a professional translator specializing in technical content. Translate the provided English text to Urdu while maintaining technical accuracy and meaning. Ensure the translation is natural and readable in Urdu."""

            user_message = f"Translate the following text to Urdu:\n\n{text}"

            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,  # Lower temperature for accuracy
                max_tokens=2000
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error translating to Urdu: {str(e)}")
            raise

    def _get_complexity_modifier(self, user_profile: Dict[str, Any]) -> str:
        """
        Determine complexity modifier based on user profile
        """
        software_level = user_profile.get("software_background", {}).get("level", "intermediate")
        hardware_experience = user_profile.get("hardware_background", {}).get("experience", "basic robotics")

        # Map profile to complexity level
        if software_level in ["advanced"] or hardware_experience in ["ROS experience"]:
            return "advanced"
        elif software_level in ["intermediate"] or hardware_experience in ["Jetson/embedded"]:
            return "intermediate"
        else:
            return "beginner-friendly"


# Example usage
if __name__ == "__main__":
    import asyncio

    async def test_agent():
        agent = OpenAIAgent()

        # Test RAG response
        query = "What are the main modules covered in this Physical AI & Humanoid Robotics book?"
        context = """This book follows a 4-model architecture:
1. ROS2 Foundations - Core concepts of Robot Operating System 2
2. Simulation - Gazebo and Unity environments for robot simulation
3. NVIDIA Isaac - Isaac Sim and Isaac ROS for perception and control
4. Vision-Language-Action (VLA) - Multimodal AI for humanoid control"""

        response = await agent.generate_rag_response(query, context)
        print(f"RAG Response: {response}")

        # Test personalization
        content = """ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms."""

        user_profile = {
            "software_background": {"level": "beginner", "languages": ["Python"]},
            "hardware_background": {"experience": "none"}
        }

        personalized = await agent.personalize_content(content, user_profile, "simpler")
        print(f"Personalized content: {personalized}")

        # Test translation
        urdu_translation = await agent.translate_to_urdu("Hello, this is a test of the Urdu translation feature.")
        print(f"Urdu translation: {urdu_translation}")

    # Run the test
    asyncio.run(test_agent())