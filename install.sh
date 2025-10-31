#!/bin/bash

# 🎨 Blender MCP Server Installation Script
# This script automates the installation and setup of the Blender MCP Server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 12 ]; then
            print_success "Python $PYTHON_VERSION found"
            return 0
        else
            print_error "Python 3.12+ required, found $PYTHON_VERSION"
            return 1
        fi
    else
        print_error "Python 3 not found"
        return 1
    fi
}

# Function to check Blender installation
check_blender() {
    if command_exists blender; then
        BLENDER_VERSION=$(blender --version | head -n 1 | grep -o '[0-9]\+\.[0-9]\+' | head -n 1)
        print_success "Blender $BLENDER_VERSION found"
        return 0
    else
        print_warning "Blender not found in PATH"
        print_status "Please ensure Blender is installed and accessible from command line"
        echo ""
        echo "Installation instructions:"
        echo "- Windows: Download from https://www.blender.org/download/"
        echo "- macOS: Install from https://www.blender.org/download/"
        echo "- Linux: Use package manager or download from https://www.blender.org/download/"
        echo ""
        return 1
    fi
}

# Function to install UV package manager
install_uv() {
    if ! command_exists uv; then
        print_status "Installing UV package manager..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null || true
        
        if command_exists uv; then
            print_success "UV package manager installed"
        else
            print_error "Failed to install UV"
            return 1
        fi
    else
        print_success "UV package manager already installed"
    fi
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    if command_exists uv; then
        uv sync
        print_success "Dependencies installed with UV"
    else
        pip install -e .
        print_success "Dependencies installed with pip"
    fi
}

# Function to verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    # Test server can be imported
    if python3 -c "import blender_mcp_server.server; print('Server import successful')" 2>/dev/null; then
        print_success "Server module imported successfully"
    else
        print_error "Failed to import server module"
        return 1
    fi
    
    # Test that tools are available
    python3 -c "
import asyncio
from blender_mcp_server.server import BlenderMCPServer

async def test_tools():
    server = BlenderMCPServer()
    tools = await server.list_tools()
    print(f'Found {len(tools)} tools')

asyncio.run(test_tools())
" 2>/dev/null && print_success "Tool discovery working" || print_warning "Tool discovery test skipped (Blender may not be running)"
}

# Function to setup Git hooks
setup_git_hooks() {
    if [ -d .git ]; then
        print_status "Setting up Git hooks..."
        if command_exists pre-commit; then
            pre-commit install
            print_success "Git hooks installed"
        else
            print_warning "pre-commit not available, skipping Git hooks setup"
        fi
    fi
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    if command_exists pytest; then
        pytest tests/ -v --tb=short
        print_success "Tests completed"
    else
        print_warning "pytest not available, skipping tests"
    fi
}

# Function to display usage information
show_usage() {
    echo ""
    print_status "🎨 Blender MCP Server installed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Start Blender with the MCP addon:"
    echo "   blender"
    echo ""
    echo "2. Enable the Blender MCP addon in Blender preferences"
    echo ""
    echo "3. Click 'Connect to Claude' in the addon panel"
    echo ""
    echo "4. Run the MCP server:"
    echo "   blender-mcp-server"
    echo ""
    echo "5. Configure your MCP client (Claude Desktop, VS Code, etc.)"
    echo ""
    echo "📚 Documentation: https://github.com/YOUR_USERNAME/blender-mcp-server"
    echo "🐛 Issues: https://github.com/YOUR_USERNAME/blender-mcp-server/issues"
    echo "💬 Discussions: https://github.com/YOUR_USERNAME/blender-mcp-server/discussions"
}

# Function to cleanup on error
cleanup() {
    print_error "Installation failed!"
    echo "Please check the error messages above and try again."
    echo "For help, see: https://github.com/YOUR_USERNAME/blender-mcp-server/issues"
}

# Main installation function
main() {
    echo "🎨 Blender MCP Server Installation"
    echo "=================================="
    echo ""
    
    # Set trap for cleanup
    trap cleanup EXIT
    
    # Check prerequisites
    print_status "Checking prerequisites..."
    check_python_version || exit 1
    check_blender  # Warning only, not blocking
    echo ""
    
    # Install UV if needed
    if ! command_exists uv; then
        install_uv || print_warning "UV installation failed, continuing with pip"
    fi
    echo ""
    
    # Install dependencies
    install_dependencies
    echo ""
    
    # Verify installation
    verify_installation
    echo ""
    
    # Setup Git hooks (optional)
    setup_git_hooks
    echo ""
    
    # Run tests (optional)
    if [ "${1}" = "--with-tests" ]; then
        run_tests
        echo ""
    fi
    
    # Success
    trap - EXIT
    show_usage
}

# Help function
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --with-tests    Run tests after installation"
    echo "  --help, -h      Show this help message"
    echo ""
    echo "This script installs and sets up the Blender MCP Server."
    echo ""
    echo "For more information, visit:"
    echo "https://github.com/YOUR_USERNAME/blender-mcp-server"
}

# Parse command line arguments
case "${1}" in
    --help|-h)
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac