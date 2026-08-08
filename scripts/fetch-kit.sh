#!/usr/bin/env bash
# One-command installer for the multi-agent contributor kit.
#
# Usage (run inside the target repository, any agent/human):
#   bash <(curl -fsSL https://raw.githubusercontent.com/SIMON-WORLD/github-multiagent-contributor/main/scripts/fetch-kit.sh)
#   # or: curl -fsSL -o /tmp/fetch-kit.sh https://raw.githubusercontent.com/SIMON-WORLD/github-multiagent-contributor/main/scripts/fetch-kit.sh && bash /tmp/fetch-kit.sh
#
# Optional: pass another source repo as $1, e.g. bash fetch-kit.sh owner/repo
set -euo pipefail

SRC="${1:-SIMON-WORLD/github-multiagent-contributor}"
BASE="https://raw.githubusercontent.com/${SRC}/main"

dl() {
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL -o "$2" "$1"
  elif command -v wget >/dev/null 2>&1; then
    wget -q -O "$2" "$1"
  else
    echo "error: need curl or wget" >&2
    exit 1
  fi
}

mkdir -p scripts docs
dl "$BASE/scripts/build_contributors.py" scripts/build_contributors.py
dl "$BASE/docs/contributor-catalog.md" docs/contributor-catalog.md
dl "$BASE/docs/add-contributors-with-agent.md" docs/add-contributors-with-agent.md
chmod +x scripts/build_contributors.py

echo "contributor kit installed."
echo "Next steps:"
echo "  python scripts/build_contributors.py --list"
echo "  python scripts/build_contributors.py --apply --tools codex,claude,renovate"
