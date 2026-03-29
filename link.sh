#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- defaults ---
MODE=""          # --global or --project
PROJECT=""
TOOL="both"      # --claude, --copilot, or both
UNLINK=false

# --- parse args ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --global)   MODE="global"; shift ;;
    --project)  MODE="project"; PROJECT="$2"; shift 2 ;;
    --claude)   TOOL="claude"; shift ;;
    --copilot)  TOOL="copilot"; shift ;;
    --unlink)   UNLINK=true; shift ;;
    -h|--help)
      echo "Usage: ./link.sh [--global | --project <path>] [--claude | --copilot] [--unlink]"
      exit 0 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$MODE" ]]; then
  echo "Specify --global or --project <path>"
  exit 1
fi

# --- resolve target dirs ---
if [[ "$MODE" == "global" ]]; then
  CLAUDE_DIR="$HOME/.claude/commands"
  COPILOT_DIR="$HOME/.copilot/agents"
else
  if [[ -z "$PROJECT" || ! -d "$PROJECT" ]]; then
    echo "Project path '$PROJECT' does not exist"
    exit 1
  fi
  PROJECT="$(cd "$PROJECT" && pwd)"
  CLAUDE_DIR="$PROJECT/.claude/commands"
  COPILOT_DIR="$PROJECT/.github/agents"
fi

# --- helpers ---

# Extract name from frontmatter or filename
get_name() {
  local file="$1"
  local name
  name=$(awk '/^---$/{n++; next} n==1 && /^name:/{sub(/^name:[[:space:]]*/, ""); print; exit}' "$file")
  if [[ -z "$name" ]]; then
    name=$(basename "$file" .md | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')
  fi
  echo "$name"
}

# Extract description from frontmatter or first non-empty line
get_description() {
  local file="$1"
  local desc
  desc=$(awk '/^---$/{n++; next} n==1 && /^description:/{sub(/^description:[[:space:]]*/, ""); print; exit}' "$file")
  if [[ -z "$desc" ]]; then
    desc=$(awk '/^---$/{n++; next} n>=2 && /^#/{sub(/^#+[[:space:]]*/, ""); print; exit}' "$file")
  fi
  if [[ -z "$desc" ]]; then
    desc="Custom agent"
  fi
  echo "$desc"
}

# Get slug from filename
get_slug() {
  basename "$1" .md
}

# --- link functions ---

link_claude() {
  local src="$1"
  local slug
  slug=$(get_slug "$src")
  local dest="$CLAUDE_DIR/$slug.md"

  if [[ "$UNLINK" == true ]]; then
    if [[ -L "$dest" ]]; then
      rm "$dest"
      echo "  removed $dest"
    fi
    return
  fi

  mkdir -p "$CLAUDE_DIR"
  if [[ -e "$dest" && ! -L "$dest" ]]; then
    echo "  skip $dest (exists, not a symlink)"
    return
  fi
  ln -sf "$src" "$dest"
  echo "  claude: /$slug -> $dest"
}

link_copilot() {
  local src="$1"
  local slug
  slug=$(get_slug "$src")
  local dest="$COPILOT_DIR/$slug.agent.md"

  if [[ "$UNLINK" == true ]]; then
    if [[ -e "$dest" ]]; then
      rm "$dest"
      echo "  removed $dest"
    fi
    return
  fi

  mkdir -p "$COPILOT_DIR"

  local name description body
  name=$(get_name "$src")
  description=$(get_description "$src")

  # Strip frontmatter from source to get body
  body=$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2{print}' "$src")
  if [[ -z "$body" ]]; then
    # No frontmatter — use entire file
    body=$(cat "$src")
  fi

  cat > "$dest" <<EOF
---
name: "$name"
description: "$description"
---

$body
EOF
  echo "  copilot: /agent $slug -> $dest"
}

# --- main ---

if [[ "$UNLINK" == true ]]; then
  echo "Unlinking ai-resources..."
else
  echo "Linking ai-resources ($MODE)..."
fi

for dir in commands prompts; do
  if [[ ! -d "$SCRIPT_DIR/$dir" ]]; then
    continue
  fi
  for file in "$SCRIPT_DIR/$dir"/*.md; do
    [[ -f "$file" ]] || continue
    slug=$(get_slug "$file")
    echo "[$dir/$slug.md]"

    if [[ "$TOOL" == "claude" || "$TOOL" == "both" ]]; then
      link_claude "$file"
    fi
    if [[ "$TOOL" == "copilot" || "$TOOL" == "both" ]]; then
      link_copilot "$file"
    fi
  done
done

echo "Done."
