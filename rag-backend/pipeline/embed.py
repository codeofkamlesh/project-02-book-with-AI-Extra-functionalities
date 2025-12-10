"""
Embedding module for the Physical AI & Humanoid Robotics RAG system.
Handles text embedding using OpenAI's embedding models.
"""
import asyncio
import os
from typing import List, Dict, Any
import openai
from openai import AsyncOpenAI
import numpy as np

class Embedder:
    """
    Handles text embedding using OpenAI's embedding models
    """

    def __init__(self, model: str = "text-embedding-3-small", dimensions: int = 1536):
        self.model = model
        self.dimensions = dimensions
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts
        """
        try:
            # Batch embeddings for efficiency (OpenAI supports up to 2048 texts per request)
            # But we'll limit to 100 per request to be safe
            all_embeddings = []

            # Process in batches of 100
            for i in range(0, len(texts), 100):
                batch = texts[i:i+100]

                response = await self.client.embeddings.create(
                    model=self.model,
                    input=batch,
                    encoding_format="float"
                )

                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)

            return all_embeddings

        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            raise

    async def embed_single_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=[text],
                encoding_format="float"
            )

            return response.data[0].embedding

        except Exception as e:
            print(f"Error generating embedding for text: {str(e)}")
            raise

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        """
        # Convert to numpy arrays
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        # Calculate cosine similarity
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0

        return float(dot_product / (norm_v1 * norm_v2))


# Example usage
if __name__ == "__main__":
    import asyncio

    async def test_embedder():
        embedder = Embedder()

        # Test with sample texts
        sample_texts = [
            "Introduction to Physical AI & Humanoid Robotics",
            "Welcome to the comprehensive guide to humanoid robotics using modern tools",
            "This book covers the complete pipeline from basic ROS 2 concepts"
        ]

        print("Generating embeddings for sample texts...")
        embeddings = await embedder.embed_texts(sample_texts)

        print(f"Generated {len(embeddings)} embeddings with dimension {len(embeddings[0])}")

        # Test similarity between first two embeddings
        similarity = embedder.cosine_similarity(embeddings[0], embeddings[1])
        print(f"Cosine similarity between first two embeddings: {similarity:.4f}")

    # Run the test
    asyncio.run(test_embedder())