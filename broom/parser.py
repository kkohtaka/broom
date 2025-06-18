"""
Parser module for handling Go code parsing.
"""

from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

import tree_sitter
from langchain_community.document_loaders.git import GitLoader


class GoParser:
    """Class for parsing Go code."""

    def __init__(self):
        """Initialize the Go parser."""
        # Note: Build the Go grammar in a real implementation and load it here.
        # This is a placeholder for the actual implementation.
        self.parser = tree_sitter.Parser()
        # self.parser.set_language(
        #     Language('build/my-languages.so', 'go')
        # )

    def parse_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse a Go file and extract code blocks.

        Args:
            file_path: Path to the Go file

        Returns:
            List of code blocks with metadata
        """
        # This is a placeholder implementation
        # In a real implementation, you would:
        # 1. Parse the file using tree-sitter
        # 2. Extract functions, methods, and other code blocks
        # 3. Return them with appropriate metadata
        content = file_path.read_text(encoding="utf-8")
        return [{"code": content, "file_path": str(file_path), "type": "file"}]

    def parse_repository(
        self, repo_path: str | Path, branch: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """Parse all Go files in a Git repository using ``GitLoader``.

        Args:
            repo_path: Local path or URL to the repository.
            branch: Optional branch to check out before loading files.

        Yields:
            Code blocks with metadata.
        """
        loader = GitLoader(
            repo_path=str(repo_path),
            branch=branch,
            file_filter=lambda x: x.endswith(".go"),
        )
        for doc in loader.load():
            file_path = Path(doc.metadata.get("file_path", ""))
            # Skip hidden files or directories
            if any(part.startswith(".") for part in file_path.parts):
                continue
            for block in self.parse_file(file_path):
                yield block
