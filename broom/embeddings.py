"""
Embeddings module for generating and managing code embeddings.
"""

from typing import Any, Dict, List

import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings


class CodeEmbedder:
    """Class for generating embeddings from code."""

    def __init__(self, model_name: str = "nomic-ai/CodeRankEmbed"):
        """Initialize the code embedder.

        Args:
            model_name: Name of the HuggingFace model to use
        """
        self.model: Embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu", "trust_remote_code": True},
            encode_kwargs={
                "normalize_embeddings": True,
                "padding": True,
                "truncation": True,
                "max_length": 512,
            },
        )

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to generate embeddings for

        Returns:
            NumPy array of embeddings
        """
        embeddings = self.model.embed_documents(texts)
        return np.array(embeddings)

    def generate_embeddings_with_metadata(
        self, texts: List[str], metadata: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate embeddings with metadata.

        Args:
            texts: List of text strings to generate embeddings for
            metadata: List of metadata dictionaries for each text

        Returns:
            List of dictionaries containing embeddings and metadata
        """
        embeddings = self.generate_embeddings(texts)
        return [
            {"embedding": emb.tolist(), **meta}
            for emb, meta in zip(embeddings, metadata)
        ]
