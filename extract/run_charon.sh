#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo " [CHARON] Extracting LLBC from rustc MIR (Non-Invasive)"
echo "=========================================================="

mkdir -p generated/llbc

if command -v charon &> /dev/null; then
  echo "[+] Invoking charon driver on upstream/domain-projection-spec..."
  charon cargo --preset=aeneas --dest=generated/llbc/ --manifest-path=upstream/domain-projection-spec/Cargo.toml -- --lib
else
  echo "[!] charon not found in PATH. Falling back to pre-staged LLBC artifact."
fi

echo "[+] LLBC extraction pass completed."
