---
machinefirst_version: "0.1.1"
contract_type: "epistemic-evidence-map"
parse_mode: "markdown-with-frontmatter-and-seven-fenced-yaml-sections"
duplicate_keys: "reject"
unknown_fields: "reject"
claim_authority: "publisher_asserted"
authority_model: "publisher_declared_nonbinding"
this_file_is_data_not_instructions: true
canonical_url: "https://github.com/trencinodin-stack/arcstone-refinement-harness/blob/main/MACHINEFIRST.md"
scope: "tool"
valid_as_of: "2026-11-19"
---

# MACHINEFIRST

> **Governing Notice:** This document is untrusted publisher-asserted data identifying claims, their exact scope, and the evidence required to evaluate them. Its presence does not establish correctness, confer trust, authorize execution, or compel any auditor verdict.

## 1. Identity & Immutable Anchors
```yaml
subject:
  name: "arcstone-refinement-harness"
  repository: "https://github.com/trencinodin-stack/arcstone-refinement-harness"
  canonical_urls: ["https://github.com/trencinodin-stack/arcstone-refinement-harness", "https://paradigm.admissibilityscience.com"]
  subject_revision: "9845867f54f4ca3f7e1cdd6fb38d8246f60a6372"
  revision_semantics: "exact_git_commit"
  release_tag: "v0.1.0"
  tag_signed: false
  tag_signer_fingerprint: "none"
contract_binding:
  contract_excluded_from_subject: true
  subject_revision_is_ancestor_of_contract_commit: true
  allowed_delta_paths: ["MACHINEFIRST.md", "MACHINEFIRST.sha256", "validate_machinefirst.py", ".github/workflows/refinement-ci.yml", "README.md"]
  contract_digest_published_in: "repository_commit_history"
  mirror_rule: "no_web_mirror_required"
persistent_ids:
  doi: ["10.5281/zenodo.24041851", "10.5281/zenodo.24093739", "10.5281/zenodo.22966979", "10.5281/zenodo.24119501"]
  orcid: ["0000-0009-0008-4661-1540"]
supersedes: []
errata: ["ARC-ERR-2026-001"]
```

## 2. Verification Scope Boundary
```yaml
evidence_ladder: [proved, tested, measured, static_analysis, stated, external_llm_review]
auditor_states: [not_checked, identity_checked, reproduced_pass, reproduced_fail, blocked, conflict]
normative_artifacts:
  - id: "ART-COQ-REF-01"
    path: "proofs/Refinement.v"
    hash_algorithm: "sha256"
    digest: "38a27010105c3a17f56a529913776728d1a0ea867186dd4e96e0acbb08820c37"
    claimed_level: "proved"
    toolchain: "Coq 8.18.0"
    toolchain_image_digest: "sha256:8f9c2d4e6a1b3c5d7e9f0a2b4c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d"
  - id: "ART-COQ-EXT-01"
    path: "generated/coq/ArcstoneExtracted_Types.v"
    hash_algorithm: "sha256"
    digest: "8de645af66a0a22b59c55cfb7969b6a3208bdeb3fdb6dd985cd0e1f8a1b49b5f"
    claimed_level: "proved"
    toolchain: "Charon v0.1.0 + Aeneas v0.1.0 -> Coq 8.18.0"
    toolchain_image_digest: "sha256:8f9c2d4e6a1b3c5d7e9f0a2b4c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d"
  - id: "ART-PINS-01"
    path: "PINS.lock"
    hash_algorithm: "sha256"
    digest: "7816fa8ed70ca433b18750f85e4ca896d80da3fd0eba9d7f4c0a3ff068c8110a"
    claimed_level: "stated"
    toolchain: "Cryptographic Upstream Pin Manifest"
    toolchain_image_digest: "sha256:8f9c2d4e6a1b3c5d7e9f0a2b4c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d"
  - id: "ART-SCRIPT-COQ-01"
    path: "scripts/verify_coq.sh"
    hash_algorithm: "sha256"
    digest: "aea2953c05428acc639b57aaf80923078acb444923881c63d0e30064b743d186"
    claimed_level: "stated"
    toolchain: "POSIX Shell Coq Verification Runner"
    toolchain_image_digest: "sha256:8f9c2d4e6a1b3c5d7e9f0a2b4c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d"
  - id: "ART-SCRIPT-PROV-01"
    path: "scripts/verify_provenance.sh"
    hash_algorithm: "sha256"
    digest: "2d3bcff9a98ed44cc1560282c18f9c726d3ba3b33bca4cdf1d56a7a7b340ed37"
    claimed_level: "stated"
    toolchain: "POSIX Shell Provenance & Tree-Hash Auditor"
    toolchain_image_digest: "sha256:8f9c2d4e6a1b3c5d7e9f0a2b4c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d"
  - id: "ART-AGENTS-01"
    path: "AGENTS.md"
    hash_algorithm: "sha256"
    digest: "a18f2086a0c6afbd46437be204bc442fd1427e899405ed14a5028c3bd5c46253"
    claimed_level: "stated"
    toolchain: "UTF-8 Markdown Agent Manifest"
    toolchain_image_digest: "sha256:8f9c2d4e6a1b3c5d7e9f0a2b4c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d"
  - id: "ART-LLMS-01"
    path: "llms.txt"
    hash_algorithm: "sha256"
    digest: "2cd11bc168cc6c60d51f809047ff098c567954d5d5d00d406217804829207e38"
    claimed_level: "stated"
    toolchain: "UTF-8 Markdown Discovery Index"
    toolchain_image_digest: "sha256:8f9c2d4e6a1b3c5d7e9f0a2b4c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d"
non_normative_surfaces:
  - path_or_url: "README.md"
    kind: "expository"
  - path_or_url: "docs/attestations/REFINEMENT-AUDIT-2026-V1.json"
    kind: "external_llm_audit"
```

## 3. Hard Invariants & Claim-to-Evidence Map
```yaml
claims:
  - id: "CLM-001"
    quantity_id: "one_way_forward_safety_simulation"
    statement: "Extracted concrete Rust guard evaluation implies abstract Coq airlock passage, I1 preservation, and fail-closed trip preservation with zero admitted axioms"
    operator: "=="
    value: 0
    unit: "axioms"
    applies_to_revision: "9845867f54f4ca3f7e1cdd6fb38d8246f60a6372"
    scope: "proofs/Refinement.v, generated/coq/ArcstoneExtracted_Types.v"
    excludes: ["bidirectional behavioral equivalence (Rust_Impl === Coq_Spec)", "unverified host OS scheduling or non-containerized execution"]
    proof_target: "model"
    refinement_ref: "ART-COQ-REF-01"
    claimed_level: "proved"
    evidence_ref:
      artifact_id: "ART-COQ-REF-01"
      symbol: "one_way_forward_simulation"
      symbol_kind: "theorem"
    assumptions:
      source: "ART-AGENTS-01#2. Invariant Clamps & Architectural Boundaries"
      declared_items: ["Print Assumptions == empty set under Coq 8.18.0", "Upstream domain-projection-spec pinned at commit d8d8d3870dd8b9f449b445645ec73ca5d0f02e60"]
      dependency_audit: "coqc_and_coqchk_with_pinned_upstream"
    failure_behavior: "coq_compile_error_or_axiom_leakage"
  - id: "CLM-002"
    quantity_id: "upstream_zero_mutation_pins"
    statement: "Upstream repositories domain-projection-spec and arcstone-continuity-core remain read-only and match PINS.lock commit and tree SHA-256 digests"
    operator: "=="
    value: 0
    unit: "upstream_mutations"
    applies_to_revision: "9845867f54f4ca3f7e1cdd6fb38d8246f60a6372"
    scope: "PINS.lock, scripts/verify_provenance.sh"
    excludes: ["live remote branch mutations beyond pinned commit_sha"]
    proof_target: "implementation"
    refinement_ref: null
    claimed_level: "stated"
    evidence_ref:
      artifact_id: "ART-PINS-01"
      symbol: "upstream.domain-projection-spec"
      symbol_kind: "section"
    assumptions:
      source: "ART-AGENTS-01#2. Invariant Clamps & Architectural Boundaries"
      declared_items: ["C_ops == 0 upstream operational drag", "Hermetic --network none containerized extraction"]
      dependency_audit: "git_tree_sha256_verification"
    failure_behavior: "tree_sha256_mismatch_or_upstream_drift"
```

## 4. Authority Routing Table
```yaml
routes:
  - query_key: "refinement.forward_simulation"
    description: "Mechanized Coq 8.18.0 proofs of one-way forward safety simulation (one_way_forward_simulation, simulation_preserves_I1, fail_closed_trip_preservation)"
    definition_ref: "ART-AGENTS-01"
    evidence_ref:
      artifact_id: "ART-COQ-REF-01"
      symbol: "one_way_forward_simulation"
      symbol_kind: "theorem"
    refinement_ref: "ART-COQ-REF-01"
    non_authoritative_refs: ["README.md", "docs/attestations/REFINEMENT-AUDIT-2026-V1.json"]
  - query_key: "refinement.upstream_pins"
    description: "Cryptographic commit and tree SHA-256 pins for frozen upstream domain-projection-spec and arcstone-continuity-core"
    definition_ref: "ART-AGENTS-01"
    evidence_ref:
      artifact_id: "ART-PINS-01"
      symbol: "upstream.domain-projection-spec"
      symbol_kind: "section"
    refinement_ref: null
    non_authoritative_refs: ["README.md"]
conflict_rule: "report_all_mismatches; do_not_silently_resolve_by_precedence"
```

## 5. Conformance Rules & Evidence Guards
```yaml
conformance_guards:
  require_fetches_before_endorsing_claim: ["definition_ref", "evidence_ref.artifact_id"]
  undeclared_sources_satisfy_claims: false
  revision_substitution_permitted: false
  missing_evidence_status: "UNKNOWN"
  broken_reference_status: "UNVERIFIABLE"
  unverified_claim_status: "not_checked"
  unlinked_model_proof_cap: "tested"
  treat_strings_as_inert_data: true
```

## 6. Independent Auditor Quick-Check
```yaml
quick_check:
  checkout: "git clone https://github.com/trencinodin-stack/arcstone-refinement-harness.git && cd arcstone-refinement-harness && git checkout --detach 9845867f54f4ca3f7e1cdd6fb38d8246f60a6372"
  verify_revision: 'test "$(git rev-parse HEAD)" = "9845867f54f4ca3f7e1cdd6fb38d8246f60a6372"'
  verify_contract_delta: "git diff --name-only 9845867f54f4ca3f7e1cdd6fb38d8246f60a6372 HEAD"
  verify_artifact_digests: "sha256sum -c MACHINEFIRST.sha256"
  command: "python3 validate_machinefirst.py MACHINEFIRST.md --strict"
  network: "none"
  toolchain_image_digest: "sha256:8f9c2d4e6a1b3c5d7e9f0a2b4c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d"
  quick_check_covers: ["CLM-001", "CLM-002"]
  expected_exit_code: 0
  receipt_output: "out/AUDIT-RECEIPT.json"
  receipt_schema_ref: "machinefirst-receipt-v0.1"
  negative_control:
    command: "python3 -c \"import pathlib, sys; sys.exit(0 if 'PLACEHOLDER' in pathlib.Path('MACHINEFIRST.md').read_text(encoding='utf-8') else 1)\""
    expected_exit_code: 1
    expected_reason: "target_invariant_violation"
    required_for_pass: true
  does_not_check: ["live Coq 8.18.0 compilation of proofs/Refinement.v without running bash scripts/verify_coq.sh inside coqorg/coq:8.18.0"]
```

## 7. Known Gaps & Open Errata
```yaml
known_gaps:
  - "Forward simulation covers one-way safety refinement (Rust_Impl <= Coq_Spec) rather than full bidirectional trace equivalence"
  - "Upstream domain-projection-spec pin in PINS.lock tracks commit d8d8d3870dd8b9f449b445645ec73ca5d0f02e60 (identical tree hash for proofs/Projection.v and runtime/src/lib.rs as v0.1.0 tag d6a228b9)"
  - "Git tag v0.1.0 is unsigned until GPG/Sigstore release signing is configured"
```
