# Security Policy

## Reporting a Vulnerability

If you discover a formal verification unsoundness, proof-checking bypass, translation leakage, or boundary containment flaw affecting `arcstone-refinement-harness`, please **do not open a public issue**.

Submit reports through either of the following private channels:

1. **GitHub Private Vulnerability Reporting (Recommended):**
   * Go to the **Security** tab of this repository (`trencinodin-stack/arcstone-refinement-harness`).
   * Click **Report a vulnerability**.
   * Fill out the form to submit a private report directly to maintainers.

2. **Email:**
   * Contact us at **security@arcstoneos.com**.

---

## What to Include

Please include, where applicable:
- A concise description of the proof soundness flaw, extractor discrepancy, or translation gap.
- Minimal reproduction steps, Coq proof script (`.v`), or CI workflow trace demonstrating the issue.
- The affected harness version, commit SHA, or pinned upstream hash (`A-77-DELTA-SHIELD-LOCKED`).
- Whether the issue involves:
  * Proof unsoundness or axiom leakage (failure of `coqchk` or non-empty `Print Assumptions`);
  * Forward simulation violation (`Rust_Impl ⊑ Coq_Spec` failing to hold);
  * Fail-closed mechanical trip bypass on invalid capabilities (`c.is_valid = false` failing to trip);
  * Extraction semantic drift between `rustc` MIR, Charon LLBC, and Aeneas Coq terms;
  * Container isolation or hermetic boundary breach (`--network none`, read-only mounts);
  * Poset dominance rank misattribution per **ARC-MONO-2026-REFINEMENT-01**;
  * Violation of the Zero-Upstream-Modification Rule ($C_{\text{ops}} = 0$ leakage).

---

## Upstream Core Immutability & Airlock Boundary

`arcstone-refinement-harness` operates as an external, downstream verification airlock ($C_{\text{ops}} > 0$). It consumes frozen, immutable upstream baselines (`domain-projection-spec`, `arcstone-continuity-core`) pinned by `PINS.lock`.

- **Strict Upstream Immutability ($C_{\text{ops}} = 0$):** Reporting an issue does not authorize modifying upstream core source trees, theorem statements, or baseline operational thresholds (`TAU_OVERRIDE_US`, `MAX_BUFFER_BYTES`).
- **Downstream Remediation:** Any proof obligation adjustments, extractor shims, or simulation lemmas must be absorbed and resolved strictly downstream in this harness.
- **Fail-Closed Principle:** Any ambiguity in capability validation or reachability margins must deterministically resolve to `mechanical_stop_tripped = true` (`POSIX 32 (REFUSAL)` or `POSIX 40 (BREACH)`).

---

## Scope & Bounded Claims

`arcstone-refinement-harness` provides translation validation and mechanized forward simulation proofs.

The repository explicitly does **not** claim:
- In-place runtime execution (execution occurs strictly within the freestanding `#[no_std]` upstream kernels);
- Bidirectional behavioral equivalence (`Rust_Impl ≡ Coq_Spec`);
- End-to-end hardware silicon validation beyond certified Coq 8.18.0 abstract models and extracted LLBC semantics;
- Dynamic runtime capability issuance (handled downstream in `arcstone-mcp-sidecar`).

---

## Response Timeline

We will acknowledge receipt within **48 hours** and work with you on a coordinated resolution and disclosure timeline.
