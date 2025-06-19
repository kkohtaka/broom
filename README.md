# Broom

Broom is a Python tool for building embedding vector databases for Git repositories, with a focus on Go code. It helps you create semantic search capabilities for your codebase by generating embeddings from your Go source code and storing them in a vector database.

## Features

- Git repository integration for code extraction
- Go code parsing and analysis
- Code embedding generation using LangChain and HuggingFace models
- Vector database storage using LangChain's ChromaDB integration
- Command-line interface for processing and searching repositories

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/broom.git
cd broom
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Processing a Repository

Process a repository to build its vector database:
```bash
python -m broom process /path/to/your/go/repo
```

Process a specific branch:
```bash
python -m broom process /path/to/your/go/repo --branch main
```

Specify a custom persistence directory:
```bash
python -m broom process /path/to/your/go/repo --persist-dir ./my_data
```

### Searching the Vector Database

Search for code using natural language:
```bash
python -m broom search "how to handle HTTP requests"
```

Specify the number of results:
```bash
python -m broom search "error handling patterns" --n-results 10
```

Use a different vector database location:
```bash
python -m broom search "database connection" --persist-dir ./my_data
```

## Project Structure

- `broom/`
  - `__init__.py` - Package initialization
  - `main.py` - Main entry point and CLI
  - `repository.py` - Git repository handling
  - `parser.py` - Go code parsing
  - `embeddings.py` - Code embedding generation using LangChain
  - `vector_store.py` - Vector database management using LangChain

## Development

The project uses:
- `black` for code formatting
- `flake8` for linting
- `isort` for import sorting
- `pytest` for testing

To set up the development environment:
```bash
pip install -r requirements.txt
```

### Running Unit Tests

To run all unit tests using pytest:
```bash
pytest
```

To run only the parser tests:
```bash
pytest tests/test_parser.py
```

## Dependencies

- LangChain for embeddings and vector store management
- HuggingFace models for code embeddings
- ChromaDB for vector storage
- GitPython for repository handling
- Tree-sitter for Go code parsing

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Development Setup with DevContainer

This project uses VS Code's DevContainer feature to provide a consistent development environment. This eliminates the need for local Python virtual environments and ensures all developers work with the same dependencies.

### Prerequisites

- [VS Code](https://code.visualstudio.com/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [VS Code Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Getting Started

1. Clone this repository
2. Open the project in VS Code
3. When prompted, click "Reopen in Container" or use the command palette (F1) and select "Remote-Containers: Reopen in Container"
4. VS Code will build the container and set up the development environment automatically
5. The container includes:
   - Python 3.11
   - Git
   - GitHub CLI
   - Common Python development tools (Black, Flake8, isort)
   - All required dependencies from requirements.txt

### Working with the DevContainer

- All Python dependencies are managed at the container level
- No need to use virtual environments
- The container provides an isolated development environment
- Changes to requirements.txt will be applied when the container is rebuilt

### Rebuilding the Container

If you need to rebuild the container (e.g., after updating requirements.txt):

1. Open the command palette (F1)
2. Select "Remote-Containers: Rebuild Container"

This will ensure all dependencies are up to date.
