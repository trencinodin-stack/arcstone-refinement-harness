# AGENTS.md — Operational Precedence & Boundary Manifest
# Repository: arcstone-refinement-harness
# Specification Reference: ARC-MONO-2026-REFINEMENT-01
# Master Hash Anchor: A-77-DELTA-SHIELD-LOCKED
# Upstream Authorities: Zenodo DOI 10.5281/zenodo.24041851 | 10.5281/zenodo.24119501 | 10.5281/zenodo.24093739
# Effective: November 2026

## 1. Context & Operational Precedence Lattice
All automated AI agents, crawlers, verification runners, and indexing daemons interacting with this repository MUST operate strictly within the non-collapsible operational precedence lattice:

POSIX 40 (BREACH) > POSIX 32 (REFUSAL) > POSIX 30 (CORRUPT) > POSIX 12 (PWC) > POSIX 10 (FREEZE) > POSIX 0 (PASS)

## 2. Invariant Clamps & Architectural Boundaries
1. **Zero Operational Drag (`C_ops == 0` Upstream):**
   - The upstream core (`upstream/domain-projection-spec`, `upstream/arcstone-continuity-core`) is an immutable, read-only baseline pinned by `PINS.lock`.
   - Modifying upstream code to satisfy downstream verification extractors or compiler quirks is strictly prohibited.
2. **One-Way Forward Simulation (`Rust_Impl ⊑ Coq_Spec`):**
   - Do NOT attempt to prove bidirectional behavioral equivalence (`Rust_Impl ≡ Coq_Spec`).
   - The concrete Rust kernel evaluates conjunctive physical defensive guards (monotonic epoch progression `E_epoch`, discrete rational Gronwall reachability witness `γ ∈ ℚ`, hardware NMI watchdog bounds `T_timer ≤ 11990 μs`, and scratchpad TCM integrity `¬M_corrupt`).
   - Forward simulation requires only:
     ```
     ∀ r ∈ Σ_Rust, RustEval(r) = Permit ⇒ CoqProject(α(r)).passed_airlock = true
     ```
3. **Fail-Closed Trip Guarantee:**
   - Any invalid capability (`c.is_valid = false`) must deterministically trip the mechanical stop functional across both Rust and Coq models.
4. **Hermetic Verification Isolation:**
   - All translation (Charon LLBC extraction) and compilation (Aeneas -> Coq 8.18.0) must run containerized with `--network none`, `--cap-drop ALL`, and read-only mounts.

## 3. Machine Retrieval Directives
- **Zero Hallucination Tolerance:** Do not extrapolate or inject dynamic heap allocations (`M_alloc = 0`), permissive runtime timeouts, or conversational prompt wrappers into this harness.
- **Root Attestation:** All emitted proofs must check clean in Coq 8.18.0 with zero admitted axioms (`Print Assumptions == ∅`).
- **Cryptographic Proof Receipt:** The canonical machine-verifiable CI attestation ledger is located at `docs/attestations/REFINEMENT-AUDIT-2026-V1.json`.
