#!/bin/bash

set -e

# Colors for output
GREEN='\033[0;32m'
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

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Detect the operating system
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

# Create a virtual environment
python3 -m venv orgi_env
source orgi_env/bin/activate

# Install the package directly from GitHub
pip install git+https://github.com/Mohamed-Rirash/orgi.git

echo -e "${GREEN}✅ Orgi CLI has been successfully installed!${NC}"
echo "To use, simply run 'orgi auto' in any directory"

# Optional: Add to PATH or create a wrapper script
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

# Create a wrapper script
WRAPPER_SCRIPT="$INSTALL_DIR/orgi"
cat << 'EOF' > "$WRAPPER_SCRIPT"
#!/bin/bash
source "$HOME/.orgi_env/bin/activate"
command orgi "$@"
EOF

chmod +x "$WRAPPER_SCRIPT"

echo -e "${GREEN}✅ Added 'orgi' to $INSTALL_DIR${NC}"
echo "You may need to restart your terminal or run 'source ~/.bashrc'"