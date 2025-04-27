#!/bin/bash

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python and pip are installed
command -v python3 >/dev/null 2>&1 || {
    echo -e "${RED}Error: Python3 is required but not installed.${NC}"
    exit 1
}

command -v pip3 >/dev/null 2>&1 || {
    echo -e "${RED}Error: pip3 is required but not installed.${NC}"
    exit 1
}

# Detect shell configuration file
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo -e "${RED}Could not detect shell configuration file.${NC}"
    exit 1
fi

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Create a virtual environment
VENV_DIR="$HOME/.orgi_env"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Install the package
pip install git+https://github.com/Mohamed-Rirash/orgi.git

# Ensure local bin directory exists
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

# Create a wrapper script
WRAPPER_SCRIPT="$INSTALL_DIR/orgi"
cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash
source "$HOME/.orgi_env/bin/activate"
command orgi "$@"
EOF

chmod +x "$WRAPPER_SCRIPT"

# Update PATH in shell configuration
if ! grep -q "$INSTALL_DIR" "$SHELL_RC"; then
    echo "export PATH=\$PATH:$INSTALL_DIR" >> "$SHELL_RC"
fi

# Clean up
cd ~
rm -rf "$TEMP_DIR"

echo -e "${GREEN}✅ Orgi CLI has been successfully installed!${NC}"
echo -e "${YELLOW}To use Orgi, you have two options:${NC}"
echo -e "1. Restart your terminal"
echo -e "2. Run: ${GREEN}source $SHELL_RC${NC}"
echo -e "\n${YELLOW}Try running:${NC}"
echo -e "  ${GREEN}orgi auto${NC}"