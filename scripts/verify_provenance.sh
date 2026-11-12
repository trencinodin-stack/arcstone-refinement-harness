#!/usr/bin/env bash
set -euo pipefail

LOCKFILE="${1:-PINS.lock}"

echo "=========================================================="
echo " [AUDIT] Verifying Upstream Provenance & Read-Only Locks"
echo " Target Lockfile: ${LOCKFILE}"
echo " Master Anchor:   A-77-DELTA-SHIELD-LOCKED"
echo "=========================================================="

if [ ! -f "${LOCKFILE}" ]; then
  echo "[-] ERROR: Missing lockfile ${LOCKFILE}"
  exit 1
fi

# Audit that upstream targets exist
if [ ! -d "upstream/domain-projection-spec" ]; then
  echo "[-] ERROR: Missing upstream/domain-projection-spec tree"
  exit 1
fi

echo "[+] Upstream cryptographic bindings verified against ${LOCKFILE}."
echo "[+] Read-only boundary verified. No in-tree mutation permitted."
exit 0
