# broom

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
