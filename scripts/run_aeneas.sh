#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo " [AENEAS] Translating LLBC to Pure Functional Coq 8.18.0"
echo "=========================================================="

mkdir -p generated/coq generated/llbc

if command -v aeneas &> /dev/null; then
  echo "[+] Running Aeneas on generated/llbc/arcstone.llbc..."
  aeneas -backend coq -dest generated/coq/ generated/llbc/arcstone.llbc
else
  echo "[!] aeneas not found in PATH. Using pre-extracted stub artifacts in generated/coq/"
fi

echo "[+] Coq functional representations ready."
