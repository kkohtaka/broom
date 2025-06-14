"""
Main script for the broom tool.
"""

import argparse
from pathlib import Path
from typing import List, Optional

from langchain_community.document_loaders.git import GitLoader
from langchain_core.documents import Document

from .embeddings import CodeEmbedder
from .parser import GoParser
from .vector_store import VectorStore


def process_repository(
    repo_path: str,
    branch: Optional[str] = None,
    persist_dir: str = "./data/chroma"
) -> None:
    """Process a Git repository and build its vector database.

    Args:
        repo_path: Path to the Git repository
        branch: Optional branch name to process
        persist_dir: Directory to persist the vector database
    """
    # Initialize components
    parser = GoParser()
    embedder = CodeEmbedder()
    vector_store = VectorStore(
        persist_directory=persist_dir,
        embedding_model=embedder.model
    )

    # Load Go files from repository
    loader = GitLoader(
        repo_path=repo_path,
        branch=branch,
        file_filter=lambda x: x.endswith(".go")
    )
    documents = loader.load()

    # Parse Go files and prepare code blocks
    code_blocks: List[Document] = []
    for doc in documents:
        file_path = Path(doc.metadata["file_path"])
        blocks = parser.parse_file(file_path)

        # Convert blocks to Documents with metadata
        for block in blocks:
            code_blocks.append(
                Document(
                    page_content=block["code"],
                    metadata={
                        "file_path": str(file_path),
                        "type": block.get("type", "file"),
                        **block.get("metadata", {})
                    }
                )
            )

    # Store embeddings
    vector_store.add_embeddings(code_blocks)


def search_repository(
    query: str,
    persist_dir: str = "./data/chroma",
    n_results: int = 5
) -> None:
    """Search the vector database.

    Args:
        query: Search query
        persist_dir: Directory where the vector database is stored
        n_results: Number of results to return
    """
    vector_store = VectorStore(persist_directory=persist_dir)
    results = vector_store.search(query, n_results=n_results)

    print(f"\nSearch results for: {query}\n")
    for i, result in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"File: {result['metadata'].get('file_path', 'Unknown')}")
        print(f"Type: {result['metadata'].get('type', 'file')}")
        print(f"Score: {result['score']:.4f}")
        print(f"Code:\n{result['text']}\n")


def main() -> None:
    """Main entry point for the broom tool."""
    parser = argparse.ArgumentParser(
        description="Build embedding vector database for Go repositories"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Process command
    process_parser = subparsers.add_parser(
        "process",
        help="Process a repository and build its vector database"
    )
    process_parser.add_argument(
        "repo_path",
        help="Path to the Git repository"
    )
    process_parser.add_argument(
        "--branch",
        help="Branch to process (default: current branch)"
    )
    process_parser.add_argument(
        "--persist-dir",
        default="./data/chroma",
        help="Directory to persist the vector database"
    )

    # Search command
    search_parser = subparsers.add_parser(
        "search",
        help="Search the vector database"
    )
    search_parser.add_argument(
        "query",
        help="Search query"
    )
    search_parser.add_argument(
        "--persist-dir",
        default="./data/chroma",
        help="Directory where the vector database is stored"
    )
    search_parser.add_argument(
        "--n-results",
        type=int,
        default=5,
        help="Number of results to return"
    )

    args = parser.parse_args()

    if args.command == "process":
        process_repository(
            repo_path=args.repo_path,
            branch=args.branch,
            persist_dir=args.persist_dir
        )
    elif args.command == "search":
        search_repository(
            query=args.query,
            persist_dir=args.persist_dir,
            n_results=args.n_results
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
