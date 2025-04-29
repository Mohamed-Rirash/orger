#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# uninstall.sh — Remove the Orger CLI completely
# -----------------------------------------------------------------------------
set -euo pipefail
IFS=$'\n\t'

# ──────────────────────────────────────────────────────────────────────────────
# Colors
# ──────────────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ──────────────────────────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────────────────────────
error() {
    echo -e "${RED}✗ $*${NC}" >&2
    exit 1
}

info() {
    echo -e "${GREEN}✔ $*${NC}"
}

warn() {
    echo -e "${YELLOW}! $*${NC}"
}

remove_if_exists() {
    local path="$1"
    local type="$2"
    if [[ -e "$path" ]]; then
        warn "Removing $type at $path..."
        rm -rf "$path"
        info "$type removed."
        return 0
    else
        warn "No $type found at $path."
        return 1
    fi
}

# ──────────────────────────────────────────────────────────────────────────────
# 1) Detect shell RC file and backup
# ──────────────────────────────────────────────────────────────────────────────
if [[ -f "$HOME/.zshrc" ]]; then
    RC_FILE="$HOME/.zshrc"
elif [[ -f "$HOME/.bashrc" ]]; then
    RC_FILE="$HOME/.bashrc"
else
    error "Could not detect ~/.bashrc or ~/.zshrc."
fi
info "Using shell RC: $RC_FILE"

# Create backup of RC file
cp "$RC_FILE" "${RC_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
info "Created backup of $RC_FILE"

# ──────────────────────────────────────────────────────────────────────────────
# 2) Confirm uninstallation
# ──────────────────────────────────────────────────────────────────────────────
echo -e "${YELLOW}This will completely remove the Orger CLI and all its files:${NC}"
echo -e "  • Virtual environment (~/.orger_env)"
echo -e "  • Launcher script (~/.local/bin/orger)"
echo -e "  • PATH modifications in $RC_FILE"
echo -e "  • Pip package (orger)"
echo
read -r -p "Are you sure you want to uninstall Orger? [y/N] " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    error "Uninstallation cancelled."
fi

# ──────────────────────────────────────────────────────────────────────────────
# 3) Remove components
# ──────────────────────────────────────────────────────────────────────────────

# Remove virtual environment
remove_if_exists "$HOME/.orger_env" "virtual environment"

# Remove launcher script
remove_if_exists "$HOME/.local/bin/orger" "launcher script"

# Clean up PATH entry from shell RC
if grep -q 'export.*PATH.*\.local/bin' "$RC_FILE"; then
    warn "Cleaning up PATH in $RC_FILE..."
    # Create a temporary file
    TEMP_RC=$(mktemp)
    # Remove the PATH line and any related comments, preserve other contents
    grep -v -E '(export.*PATH.*\.local/bin|# Add .* CLI to PATH)' "$RC_FILE" > "$TEMP_RC"
    # Replace original with cleaned version
    mv "$TEMP_RC" "$RC_FILE"
    info "PATH cleaned up in $RC_FILE"
else
    warn "No PATH modification found in $RC_FILE"
fi

# Uninstall pip package
if command -v pip3 >/dev/null 2>&1; then
    if pip3 list --disable-pip-version-check | grep -q "^orger "; then
        warn "Uninstalling Orger pip package..."
        pip3 uninstall -y orger
        info "Pip package uninstalled."
    else
        warn "Orger pip package not found."
    fi
else
    warn "pip3 not found, skipping package uninstallation."
fi

# ──────────────────────────────────────────────────────────────────────────────
# 4) Final message
# ──────────────────────────────────────────────────────────────────────────────
echo
info "Orger CLI has been fully uninstalled."
info "A backup of your shell configuration was created at: ${RC_FILE}.backup.*"
cat <<EOF

To finalize the uninstallation:
  • Restart your terminal, or
  • Run: ${GREEN}source $RC_FILE${NC}

EOF
