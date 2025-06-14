"""
Repository module for handling Git operations.
"""

from pathlib import Path
from typing import List, Optional

from git import Repo


class Repository:
    """Class for handling Git repository operations."""

    def __init__(self, repo_path: str):
        """Initialize the repository handler.

        Args:
            repo_path: Path to the Git repository
        """
        self.repo_path = Path(repo_path)
        self.repo = Repo(repo_path)

    def get_go_files(self, branch: Optional[str] = None) -> List[Path]:
        """Get all Go files in the repository.

        Args:
            branch: Optional branch name to check out before getting files

        Returns:
            List of paths to Go files
        """
        if branch:
            self.repo.git.checkout(branch)

        go_files = []
        for path in self.repo_path.rglob("*.go"):
            if not any(part.startswith(".") for part in path.parts):
                go_files.append(path)

        return go_files

    def get_file_content(self, file_path: Path) -> str:
        """Get the content of a file.

        Args:
            file_path: Path to the file

        Returns:
            Content of the file as string
        """
        return file_path.read_text(encoding="utf-8")
