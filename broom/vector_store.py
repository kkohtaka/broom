"""
Vector store module for managing the vector database.
"""

from typing import Any, Dict, List, Optional

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


class VectorStore:
    """Class for managing the vector database."""

    def __init__(
        self,
        persist_directory: str = "./data/chroma",
        collection_name: str = "go_code",
        embedding_model: Optional[Embeddings] = None,
    ):
        """Initialize the vector store.

        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection to use
            embedding_model: Optional embedding model to use
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding_model = embedding_model or HuggingFaceEmbeddings(
            model_name="nomic-ai/CodeRankEmbed",
            model_kwargs={"device": "cpu", "trust_remote_code": True},
            encode_kwargs={
                "normalize_embeddings": True,
                "padding": True,
                "truncation": True,
                "max_length": 512,
            },
        )

        self.db = Chroma(
            persist_directory=persist_directory,
            collection_name=collection_name,
            embedding_function=self.embedding_model,
        )

    def add_embeddings(
        self,
        embeddings: List[Dict[str, Any]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Add embeddings to the vector store.

        Args:
            embeddings: List of embedding dictionaries
            metadatas: Optional list of metadata dictionaries
        """
        texts = [item["code"] for item in embeddings]
        if metadatas is None:
            metadatas = [{} for _ in embeddings]

        documents = [
            Document(page_content=text, metadata=metadata)
            for text, metadata in zip(texts, metadatas)
        ]

        self.db.add_documents(documents)
        self.db.persist()

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar texts.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            List of similar items with their metadata
        """
        results = self.db.similarity_search_with_score(
            query=query,
            k=n_results,
        )

        return [
            {
                "text": doc.page_content,
                "metadata": doc.metadata,
                "score": score,
            }
            for doc, score in results
        ]
