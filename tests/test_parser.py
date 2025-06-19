import tempfile
from pathlib import Path

import pytest

from broom.parser import GoParser


@pytest.mark.parametrize(
    "go_code",
    [
        # Simple main function
        """
package main

import \"fmt\"

func main() {
    fmt.Println(\"Hello, world!\")
}
""",
        # Go file with multiple functions
        """
package math

func Add(a int, b int) int {
    return a + b
}

func Sub(a int, b int) int {
    return a - b
}
""",
        # Go file with struct and method
        """
package user

type User struct {
    Name string
}

func (u *User) Greet() string {
    return \"Hello, \" + u.Name
}
""",
    ]
)
def test_parse_file_returns_code_block(go_code):
    """Test GoParser.parse_file returns correct code block for various Go files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.go"
        file_path.write_text(go_code, encoding="utf-8")

        parser = GoParser()
        result = parser.parse_file(file_path)

        assert isinstance(result, list)
        assert len(result) == 1
        block = result[0]
        assert isinstance(block, dict)
        assert block["code"] == go_code
        assert block["file_path"] == str(file_path)
        assert block["type"] == "file"


def test_parse_file_file_not_found():
    """Test GoParser.parse_file raises FileNotFoundError for missing file."""
    parser = GoParser()
    missing_dir = "/nonexistent/path/to"
    missing_file = Path(missing_dir) / "file.go"
    with pytest.raises(FileNotFoundError):
        parser.parse_file(missing_file)
