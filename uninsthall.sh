#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# uninstall.sh — Remove the Orgi CLI completely
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

# ──────────────────────────────────────────────────────────────────────────────
# 1) Detect shell RC file
# ──────────────────────────────────────────────────────────────────────────────
if [[ -f "$HOME/.zshrc" ]]; then
    RC_FILE="$HOME/.zshrc"
elif [[ -f "$HOME/.bashrc" ]]; then
    RC_FILE="$HOME/.bashrc"
else
    error "Could not detect ~/.bashrc or ~/.zshrc."
fi
info "Using shell RC: $RC_FILE"

# ──────────────────────────────────────────────────────────────────────────────
# 2) Paths to remove
# ──────────────────────────────────────────────────────────────────────────────
VENV_DIR="$HOME/.orgi_env"
BIN_DIR="$HOME/.local/bin"
WRAPPER="$BIN_DIR/orgi"

# ──────────────────────────────────────────────────────────────────────────────
# 3) Confirm
# ──────────────────────────────────────────────────────────────────────────────
echo -e "${YELLOW}This will completely remove the Orgi CLI and all its files.${NC}"
read -r -p "Are you sure you want to uninstall Orgi? [y/N] " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    error "Uninstallation cancelled."
fi

# ──────────────────────────────────────────────────────────────────────────────
# 4) Remove virtualenv
# ──────────────────────────────────────────────────────────────────────────────
if [[ -d "$VENV_DIR" ]]; then
    warn "Removing virtual environment at $VENV_DIR…"
    rm -rf "$VENV_DIR"
    info "Virtual environment removed."
else
    warn "No virtual environment found at $VENV_DIR."
fi

# ──────────────────────────────────────────────────────────────────────────────
# 5) Remove launcher script
# ──────────────────────────────────────────────────────────────────────────────
if [[ -f "$WRAPPER" ]]; then
    warn "Removing Orgi launcher script at $WRAPPER…"
    rm -f "$WRAPPER"
    info "Launcher script removed."
else
    warn "No launcher script found at $WRAPPER."
fi

# ──────────────────────────────────────────────────────────────────────────────
# 6) Remove PATH entry from shell RC
# ──────────────────────────────────────────────────────────────────────────────
# Matches lines exporting ~/.local/bin in any position
if grep -Fq 'export PATH="$HOME/.local/bin:$PATH"' "$RC_FILE"; then
    warn "Removing PATH update from $RC_FILE…"
    # Delete the exact export line plus any preceding comment
    sed -i.bak '/# Add Orgi CLI to PATH/ {N;d;}' "$RC_FILE"
    info "PATH update removed (backup at ${RC_FILE}.bak)."
else
    warn "No PATH update found in $RC_FILE."
fi

# ──────────────────────────────────────────────────────────────────────────────
# 7) Uninstall pip package
# ──────────────────────────────────────────────────────────────────────────────
if command -v pip3 >/dev/null 2>&1 && pip3 list --disable-pip-version-check | grep -Fq orgi; then
    warn "Uninstalling Orgi pip package…"
    pip3 uninstall -y orgi
    info "Pip package uninstalled."
else
    warn "Orgi pip package not found (or pip3 missing)."
fi

# ──────────────────────────────────────────────────────────────────────────────
# 8) Final message
# ──────────────────────────────────────────────────────────────────────────────
echo
info "Orgi CLI has been fully uninstalled."
cat <<EOF

To finalize:
  • Restart your terminal, or
  • Run: ${GREEN}source $RC_FILE${NC}

EOF
