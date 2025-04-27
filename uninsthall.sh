#!/bin/bash

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Detect shell configuration file
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo -e "${RED}Could not detect shell configuration file.${NC}"
    exit 1
}

# Paths to remove
VENV_DIR="$HOME/.orgi_env"
INSTALL_DIR="$HOME/.local/bin"
WRAPPER_SCRIPT="$INSTALL_DIR/orgi"

# Function to remove PATH entry
remove_path_entry() {
    local rc_file="$1"
    # Remove the Orgi PATH entry if it exists
    sed -i '\|export PATH=\$PATH:'"$INSTALL_DIR"'|d' "$rc_file"
}

# Confirm uninstallation
echo -e "${YELLOW}This will completely remove Orgi CLI and its associated files.${NC}"
read -p "Are you sure you want to uninstall Orgi? (y/N) " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
    # Remove virtual environment
    if [ -d "$VENV_DIR" ]; then
        echo -e "${YELLOW}Removing Orgi virtual environment...${NC}"
        rm -rf "$VENV_DIR"
    fi

    # Remove wrapper script
    if [ -f "$WRAPPER_SCRIPT" ]; then
        echo -e "${YELLOW}Removing Orgi wrapper script...${NC}"
        rm -f "$WRAPPER_SCRIPT"
    fi

    # Remove PATH entry
    remove_path_entry "$SHELL_RC"

    # Uninstall pip package
    if pip list | grep -q orgi; then
        echo -e "${YELLOW}Uninstalling Orgi pip package...${NC}"
        pip uninstall -y orgi
    fi

    echo -e "${GREEN}✅ Orgi CLI has been completely uninstalled.${NC}"
    echo -e "${YELLOW}To complete the uninstallation, please:${NC}"
    echo -e "1. Restart your terminal"
    echo -e "2. Or run: ${GREEN}source $SHELL_RC${NC}"
else
    echo -e "${RED}Uninstallation cancelled.${NC}"
fi