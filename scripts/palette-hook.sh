#!/usr/bin/env bash
# Claude Code PostToolUse hook: enforce Palette 6 after edits to index.html.
# Reads the hook JSON on stdin; only acts when index.html was the edited file.
# Exit 2 (with stderr) feeds the violation back to Claude; exit 0 is silent.
set -euo pipefail

input=$(cat)
file_path=$(printf '%s' "$input" | python3 -c \
  "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" \
  2>/dev/null || true)

case "$file_path" in
  *index.html)
    if ! out=$(python3 "${CLAUDE_PROJECT_DIR:-.}/scripts/check-palette.py" \
                       "${CLAUDE_PROJECT_DIR:-.}/index.html" 2>&1); then
      echo "$out" >&2
      exit 2
    fi
    ;;
esac
exit 0
