#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# install.sh — Install the Orgi CLI (version v0.1.1)
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
# Helpers
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
# 1) Prerequisites
# ──────────────────────────────────────────────────────────────────────────────
command -v python3 >/dev/null 2>&1 || error "Python 3 is required but not found."
command -v pip3   >/dev/null 2>&1 || error "pip3 is required but not found."

# ──────────────────────────────────────────────────────────────────────────────
# 2) Detect shell RC file (bash or zsh)
# ──────────────────────────────────────────────────────────────────────────────
RC=""
case "${SHELL##*/}" in
  zsh)   RC="$HOME/.zshrc" ;;
  bash)  RC="$HOME/.bashrc" ;;
  *)     if [[ -f "$HOME/.bashrc" ]]; then
           RC="$HOME/.bashrc"
         elif [[ -f "$HOME/.zshrc" ]]; then
           RC="$HOME/.zshrc"
         else
           error "Could not detect ~/.bashrc or ~/.zshrc."
         fi
         ;;
esac
info "Using shell RC: $RC"

# ──────────────────────────────────────────────────────────────────────────────
# 3) Create & activate venv
# ──────────────────────────────────────────────────────────────────────────────
VENV_DIR="$HOME/.orgi_env"
if [[ ! -d "$VENV_DIR" ]]; then
    info "Creating virtualenv at $VENV_DIR"
    python3 -m venv "$VENV_DIR"
else
    info "Reusing existing virtualenv at $VENV_DIR"
fi
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

# ──────────────────────────────────────────────────────────────────────────────
# 4) Install (or upgrade) the Orgi package pinned to v0.1.1
# ──────────────────────────────────────────────────────────────────────────────
info "Installing Orgi CLI (v0.1.1) from GitHub..."
pip install --upgrade "git+https://github.com/Mohamed-Rirash/orgi.git@v0.1.1"

# ──────────────────────────────────────────────────────────────────────────────
# 5) Symlink wrapper into ~/.local/bin
# ──────────────────────────────────────────────────────────────────────────────
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

WRAPPER="$BIN_DIR/orgi"
cat > "$WRAPPER" <<'EOF'
#!/usr/bin/env bash
# OrgI wrapper: always run inside our venv
source "$HOME/.orgi_env/bin/activate"
exec orgi "$@"
EOF

chmod +x "$WRAPPER"
info "Created launcher script: $WRAPPER"

# ──────────────────────────────────────────────────────────────────────────────
# 6) Ensure ~/.local/bin is in PATH via shell rc
# ──────────────────────────────────────────────────────────────────────────────
EXPORT_CMD='export PATH="$HOME/.local/bin:$PATH"'
if ! grep -Fxq "$EXPORT_CMD" "$RC"; then
    echo "" >> "$RC"
    echo "# Add Orgi CLI to PATH" >> "$RC"
    echo "$EXPORT_CMD"  >> "$RC"
    info "Added PATH update to $RC"
else
    warn "PATH update already present in $RC"
fi

# ──────────────────────────────────────────────────────────────────────────────
# 7) Done!
# ──────────────────────────────────────────────────────────────────────────────
echo
info "Orgi CLI v0.1.1 has been installed successfully!"
cat <<EOF

To start using it, either:
  • Restart your terminal, or
  • Run: ${GREEN}source $RC${NC}

Then try:
  ${GREEN}orgi auto${NC}

EOF
