#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/compassanalytics/claude-workshop.git"
SKILLS_DIR="${HOME}/.claude/skills"
TMP_DIR=""

cleanup() {
  if [[ -n "${TMP_DIR}" && -d "${TMP_DIR}" ]]; then
    rm -rf "${TMP_DIR}"
  fi
}
trap cleanup EXIT

if [[ -d "${PWD}/workshop-session-2/skills" ]]; then
  SOURCE_DIR="${PWD}/workshop-session-2/skills"
  echo "Installing skills from local directory..."
else
  TMP_DIR=$(mktemp -d)
  echo "Cloning ${REPO_URL}..."
  git clone --depth 1 "${REPO_URL}" "${TMP_DIR}"
  SOURCE_DIR="${TMP_DIR}/workshop-session-2/skills"
fi

mkdir -p "${SKILLS_DIR}"

echo "Copying skills to ${SKILLS_DIR}..."
for skill_dir in "${SOURCE_DIR}"/*/; do
  skill_name=$(basename "${skill_dir}")
  target="${SKILLS_DIR}/${skill_name}"

  if [[ -d "${target}" ]]; then
    echo "  Updating ${skill_name}"
    rm -rf "${target}"
  else
    echo "  Installing ${skill_name}"
  fi

  cp -R "${skill_dir}" "${target}"
done

echo ""
echo "Done. Start a Claude Code session and run:"
echo "  /sdlc-coach"
