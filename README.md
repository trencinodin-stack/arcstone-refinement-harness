# arcstone-refinement-harness

[![Mechanized Refinement Verification (Coq 8.18.0 <-> Rust)](https://github.com/trencinodin-stack/arcstone-refinement-harness/actions/workflows/refinement-ci.yml/badge.svg)](https://github.com/trencinodin-stack/arcstone-refinement-harness/actions/workflows/refinement-ci.yml)

Mechanized Refinement & Simulation Harness for the Arcstone Computational Spine (ACS).

## Overview

This repository implements the **Decoupled Refinement Airlock** (`ARC-MONO-2026-REFINEMENT-01`). It acts as an external, content-addressed verification harness that mechanizes the one-way forward safety simulation:

$$\mathrm{Rust\_Impl} \sqsubseteq \mathrm{Coq\_Spec}$$

The upstream sovereign core (`arcstone-continuity-core` / `domain-projection-spec`) remains strictly read-only and frozen ($C_{\mathrm{ops}} = 0$, $M_{\mathrm{alloc}} = 0$, $S_{\max} \le 4096\text{ B}$, $\tau_{\mathrm{override}} \le 11.99\text{ ms}$). All formal extraction and translation maintenance drag ($C_{\mathrm{ops}} > 0$) is absorbed downstream inside this harness.

## Architecture & Pipeline
1. **Extraction:** `Charon` extracts Low-Level Borrow Calculus (LLBC) directly from `rustc` MIR without modifying upstream source code.
2. **Translation:** `Aeneas` compiles LLBC into pure functional definitions in Coq 8.18.0.
3. **Simulation Proofs:** Machine-checked proofs in Coq verify that concrete Rust evaluation guards imply abstract reachability theorems with zero admitted axioms (`Print Assumptions == ∅`).
4. **Hermetic CI & Attestation:** Verification runs inside a network-isolated container (`--network none`, `--cap-drop ALL`, read-only mounts) and emits a cryptographic proof receipt (`docs/attestations/REFINEMENT-AUDIT-2026-V1.json`).

## Local Quickstart

### Prerequisites
- Docker (recommended for hermetic execution) OR:
  - Coq 8.18.0 (`coqc` and `coqchk`)
  - Stable & Nightly Rust (`nightly-2024-05-01` pinned in `PINS.lock`)
  - Charon (`charon-driver`)
  - Aeneas compiler

### 1. Verification Setup
```bash
# Clone the frozen upstream specification pinned by PINS.lock
mkdir -p upstream
rm -rf upstream/domain-projection-spec
git clone https://github.com/trencinodin-stack/domain-projection-spec.git upstream/domain-projection-spec
git -C upstream/domain-projection-spec checkout --detach b06da20a7b4588e36780c65538eec4c414603957

# Verify cryptographic provenance and lockfile hashes
./scripts/verify_provenance.sh PINS.lock
```
### 2. Local Extraction & Compilation

```bash
# Extract LLBC from upstream Rust MIR
./extract/run_charon.sh

# Translate LLBC to Coq functional terms
./scripts/run_aeneas.sh

# Build and verify Coq simulation proofs (Print Assumptions == ∅)
./scripts/verify_coq.sh

```

### 3. Docker Run (Hermetic)

```bash
docker build -t arcstone/refinement-harness:local .
docker run --rm --network none --cap-drop ALL --read-only --tmpfs /tmp:rw arcstone/refinement-harness:local

```

## Non-Leakage & Governance Perimeters

- **Zero-Upstream-Modification:** Upstream files in `upstream/` are strictly read-only (`chmod -R a-w upstream/`).
- **One-Way Simulation:** Proves safety containment (every Rust admit satisfies Coq reachability), bypassing brittle bidirectional equivalence.
- **Cryptographic Attestation:** Automated CI proof receipts are archived under `docs/attestations/REFINEMENT-AUDIT-2026-V1.json`.
