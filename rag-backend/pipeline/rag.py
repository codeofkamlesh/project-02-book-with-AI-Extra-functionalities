"""
RAG (Retrieval-Augmented Generation) orchestration module for the Physical AI & Humanoid Robotics system.
Coordinates the flow between embedding, retrieval, and generation components.
"""
import asyncio
import os
from typing import List, Dict, Any, Optional
from .embed import Embedder
from .retriever import Retriever
from ..agents.openai_agent_integration import OpenAIAgent

class RAGPipeline:
    """
    Orchestrates the complete RAG pipeline: retrieve relevant documents and generate answers
    """

    def __init__(self):
        self.embedder = Embedder()
        self.retriever = Retriever()
        self.agent = OpenAIAgent()

    async def initialize(self):
        """
        Initialize all required components
        """
        await self.retriever.initialize_collection()

    async def process_query(
        self,
        query: str,
        user_profile: Optional[Dict[str, Any]] = None,
        highlight_text: Optional[str] = None,
        top_k: int = 6
    ) -> Dict[str, Any]:
        """
        Process a user query through the complete RAG pipeline
        """
        try:
            # Step 1: Embed the query
            query_embedding = await self.embedder.embed_single_text(query)

            # Step 2: Retrieve relevant documents
            # If highlight_text is provided, search for documents containing that text
            if highlight_text:
                retrieved_docs = await self.retriever.search_by_text_content(highlight_text, top_k=top_k)
            else:
                retrieved_docs = await self.retriever.retrieve_documents(
                    query_embedding=query_embedding,
                    top_k=top_k,
                    user_profile=user_profile
                )

            # Step 3: Prepare context for generation
            context_texts = [doc["source_text"] for doc in retrieved_docs]
            context_str = "\n\n".join(context_texts)

            # Step 4: Generate answer using OpenAI
            answer = await self._generate_answer(query, context_str, user_profile)

            # Step 5: Format response with provenance
            response = {
                "answer": answer,
                "sources": [
                    {
                        "title": doc["title"],
                        "path": doc["path"],
                        "module": doc["module"],
                        "score": doc["score"],
                        "excerpt": doc["source_text"][:200] + "..." if len(doc["source_text"]) > 200 else doc["source_text"]
                    }
                    for doc in retrieved_docs
                ],
                "query": query,
                "retrieved_docs_count": len(retrieved_docs),
                "context_used": context_str[:500] + "..." if len(context_str) > 500 else context_str  # Truncate for response
            }

            return response

        except Exception as e:
            print(f"Error in RAG pipeline: {str(e)}")
            raise

    async def _generate_answer(
        self,
        query: str,
        context: str,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate an answer based on the query and retrieved context
        """
        try:
            # Use the OpenAI agent for response generation
            answer = await self.agent.generate_rag_response(query, context, user_profile)
            return answer

        except Exception as e:
            print(f"Error generating answer: {str(e)}")
            raise


    async def ingest_document(
        self,
        path: str,
        content: str,
        title: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ingest a document into the RAG system (chunk, embed, store)
        """
        try:
            # Import chunker here to avoid circular imports
            from .chunker import DocumentChunker
            chunker = DocumentChunker()

            # Step 1: Chunk the document
            chunks = chunker.chunk_document(content, path, title)

            # Step 2: Embed each chunk
            chunk_texts = [chunk["source_text"] for chunk in chunks]
            embeddings = await self.embedder.embed_texts(chunk_texts)

            # Step 3: Update chunks with embeddings
            for i, chunk in enumerate(chunks):
                chunk["embedding"] = embeddings[i]

            # Step 4: Store in Qdrant
            await self.retriever.upsert_chunks(chunks)

            return {
                "status": "success",
                "doc_path": path,
                "chunks_created": len(chunks),
                "doc_id": chunks[0]["doc_id"] if chunks else None
            }

        except Exception as e:
            print(f"Error ingesting document: {str(e)}")
            raise


# Example usage
if __name__ == "__main__":
    import asyncio

    async def test_rag_pipeline():
        rag_pipeline = RAGPipeline()

        # Initialize the pipeline
        await rag_pipeline.initialize()

        # Test query
        query = "What are the main modules covered in this Physical AI & Humanoid Robotics book?"

        result = await rag_pipeline.process_query(query)

        print(f"Query: {query}")
        print(f"Answer: {result['answer']}")
        print(f"Sources: {len(result['sources'])} documents retrieved")

    # Run the test
    asyncio.run(test_rag_pipeline())