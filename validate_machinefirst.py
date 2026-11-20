#!/usr/bin/env python3
"""
MACHINEFIRST.md (v0.1.1) Strict Conformance Validator (Zero-Dependency Stdlib Edition)

Enforces:
1. Valid UTF-8 encoding and YAML frontmatter block on line 1.
2. Exact H2 section headers (## 1. through ## 7.) in sequence.
3. Exactly one properly closed ```yaml fenced block per H2 section.
4. Unique mapping keys (rejects duplicates), no anchors/aliases (&/*), merge keys (<<), or tags (!).
5. Referential integrity across normative_artifacts, claims, and routes.
6. Model-vs-implementation refinement enforcement (unlinked implementation proofs fail).
7. Placeholder rejection when --strict is enabled.
8. Byte-identical UTF-8 mirror equality when --mirror-path is supplied.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


EXPECTED_HEADERS = [
    "## 1. Identity & Immutable Anchors",
    "## 2. Verification Scope Boundary",
    "## 3. Hard Invariants & Claim-to-Evidence Map",
    "## 4. Authority Routing Table",
    "## 5. Conformance Rules & Evidence Guards",
    "## 6. Independent Auditor Quick-Check",
    "## 7. Known Gaps & Open Errata",
]

REQUIRED_FRONTMATTER_KEYS = {
    "machinefirst_version",
    "contract_type",
    "parse_mode",
    "duplicate_keys",
    "unknown_fields",
    "claim_authority",
    "authority_model",
    "this_file_is_data_not_instructions",
    "canonical_url",
    "scope",
    "valid_as_of",
}

ALLOWED_EVIDENCE_LEVELS = {
    "proved",
    "tested",
    "measured",
    "static_analysis",
    "stated",
    "external_llm_review",
}

ALLOWED_AUDITOR_STATES = {
    "not_checked",
    "identity_checked",
    "reproduced_pass",
    "reproduced_fail",
    "blocked",
    "conflict",
}

ALLOWED_SCOPES = {
    "repository",
    "component",
    "domain",
    "website",
    "tool",
}

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHA256_PREFIXED_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
PLACEHOLDER_RE = re.compile(r"<[a-zA-Z0-9_-]+>|xxxxxxx")


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    escape = False
    out = []
    for ch in line:
        if escape:
            out.append(ch)
            escape = False
            continue
        if ch == "\\" and in_double:
            out.append(ch)
            escape = True
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            out.append(ch)
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            out.append(ch)
            continue
        if ch == "#" and not in_single and not in_double:
            break
        out.append(ch)
    return "".join(out).rstrip()


def _split_top_level_commas(text: str) -> List[str]:
    parts: List[str] = []
    buf: List[str] = []
    depth = 0
    in_single = False
    in_double = False
    escape = False
    for ch in text:
        if escape:
            buf.append(ch)
            escape = False
            continue
        if ch == "\\" and in_double:
            buf.append(ch)
            escape = True
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            buf.append(ch)
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            buf.append(ch)
            continue
        if not in_single and not in_double:
            if ch in "[{":
                depth += 1
            elif ch in "]}":
                depth -= 1
            elif ch == "," and depth == 0:
                parts.append("".join(buf).strip())
                buf = []
                continue
        buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail)
    return parts


def _parse_scalar(token: str, context: str) -> Any:
    token = token.strip()
    if token.startswith("&") or token.startswith("*"):
        raise ValueError(f"[{context}] YAML anchors or aliases (&/*) are prohibited: {token!r}")
    if token.startswith("!"):
        raise ValueError(f"[{context}] Custom YAML tags (!) are prohibited: {token!r}")
    if token == "":
        return ""
    if token in ("null", "Null", "NULL", "~"):
        return None
    if token in ("true", "True", "TRUE"):
        return True
    if token in ("false", "False", "FALSE"):
        return False
    if token.startswith('"') and token.endswith('"') and len(token) >= 2:
        try:
            return json.loads(token)
        except json.JSONDecodeError as exc:
            raise ValueError(f"[{context}] Invalid double-quoted string {token!r}: {exc}") from exc
    if token.startswith("'") and token.endswith("'") and len(token) >= 2:
        return token[1:-1].replace("''", "'")
    if token.startswith("[") and token.endswith("]"):
        inner = token[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(item, context) for item in _split_top_level_commas(inner)]
    if token.startswith("{") and token.endswith("}"):
        inner = token[1:-1].strip()
        if not inner:
            return {}
        mapping: Dict[str, Any] = {}
        for item in _split_top_level_commas(inner):
            if ":" not in item:
                raise ValueError(f"[{context}] Invalid inline mapping entry: {item!r}")
            k_raw, v_raw = item.split(":", 1)
            k = str(_parse_scalar(k_raw.strip(), context))
            if k in mapping:
                raise ValueError(f"[{context}] Found duplicate key: {k!r}")
            mapping[k] = _parse_scalar(v_raw.strip(), context)
        return mapping
    if re.match(r"^-?[0-9]+$", token):
        return int(token)
    if re.match(r"^-?[0-9]+\.[0-9]+$", token):
        return float(token)
    return token


def _split_kv(text: str, context: str) -> Tuple[str, str]:
    in_single = False
    in_double = False
    escape = False
    for idx, ch in enumerate(text):
        if escape:
            escape = False
            continue
        if ch == "\\" and in_double:
            escape = True
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            continue
        if ch == ":" and not in_single and not in_double:
            if idx + 1 == len(text) or text[idx + 1].isspace():
                key = str(_parse_scalar(text[:idx].strip(), context))
                val = text[idx + 1 :].strip()
                return key, val
    raise ValueError(f"[{context}] Expected 'key: value' mapping syntax, got: {text!r}")


def parse_strict_yaml(raw_yaml: str, context: str) -> Dict[str, Any]:
    cleaned: List[Tuple[int, str]] = []
    for raw_line in raw_yaml.splitlines():
        stripped = _strip_comment(raw_line)
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        if "\t" in stripped[:indent]:
            raise ValueError(f"[{context}] Tab indentation is prohibited in YAML.")
        cleaned.append((indent, stripped.strip()))

    if not cleaned:
        return {}

    def parse_block(idx: int, base_indent: int) -> Tuple[Any, int]:
        if idx >= len(cleaned):
            return {}, idx
        indent, text = cleaned[idx]
        if text.startswith("- ") or text == "-":
            items: List[Any] = []
            while idx < len(cleaned):
                cur_indent, cur_text = cleaned[idx]
                if cur_indent < base_indent:
                    break
                if cur_indent > base_indent:
                    raise ValueError(f"[{context}] Unexpected indentation at line: {cur_text!r}")
                if not (cur_text.startswith("- ") or cur_text == "-"):
                    break
                rest = cur_text[1:].strip()
                if not rest:
                    val, idx = parse_block(idx + 1, base_indent + 2)
                    items.append(val)
                elif ":" in rest and not (rest.startswith('"') or rest.startswith("'") or rest.startswith("[") or rest.startswith("{")):
                    # Inline mapping start on list item (e.g., `- id: "CLM-001"`)
                    k, v_str = _split_kv(rest, context)
                    item_map: Dict[str, Any] = {}
                    if v_str == "":
                        val, idx = parse_block(idx + 1, base_indent + 2)
                        item_map[k] = val
                    else:
                        item_map[k] = _parse_scalar(v_str, context)
                        idx += 1
                    # Consume subsequent sibling keys of this list item at base_indent + 2
                    while idx < len(cleaned) and cleaned[idx][0] == base_indent + 2:
                        sub_text = cleaned[idx][1]
                        if sub_text.startswith("- "):
                            break
                        sk, sv_str = _split_kv(sub_text, context)
                        if sk in item_map:
                            raise ValueError(f"[{context}] Found duplicate key: {sk!r}")
                        if sv_str == "":
                            sval, idx = parse_block(idx + 1, base_indent + 4)
                            item_map[sk] = sval
                        else:
                            item_map[sk] = _parse_scalar(sv_str, context)
                            idx += 1
                    items.append(item_map)
                else:
                    items.append(_parse_scalar(rest, context))
                    idx += 1
            return items, idx
        else:
            mapping: Dict[str, Any] = {}
            while idx < len(cleaned):
                cur_indent, cur_text = cleaned[idx]
                if cur_indent < base_indent:
                    break
                if cur_indent > base_indent:
                    raise ValueError(f"[{context}] Unexpected indentation at line: {cur_text!r}")
                if cur_text.startswith("- "):
                    raise ValueError(f"[{context}] Unexpected sequence item in mapping at: {cur_text!r}")
                k, v_str = _split_kv(cur_text, context)
                if k == "<<":
                    raise ValueError(f"[{context}] YAML merge key '<<' is prohibited.")
                if k in mapping:
                    raise ValueError(f"[{context}] Found duplicate key: {k!r}")
                if v_str == "":
                    val, idx = parse_block(idx + 1, base_indent + 2)
                    mapping[k] = val
                else:
                    mapping[k] = _parse_scalar(v_str, context)
                    idx += 1
            return mapping, idx

    root, next_idx = parse_block(0, cleaned[0][0])
    if next_idx != len(cleaned) or not isinstance(root, dict):
        raise ValueError(f"[{context}] Top-level YAML structure must be a single mapping.")
    return root


def extract_sections(content: str) -> Tuple[Dict[str, Any], Dict[int, Dict[str, Any]]]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Document must begin on line 1 with YAML frontmatter delimiter '---'.")

    fm_end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            fm_end = idx
            break
    if fm_end is None:
        raise ValueError("Unclosed YAML frontmatter: missing closing '---'.")

    frontmatter = parse_strict_yaml("\n".join(lines[1:fm_end]), "frontmatter")
    body_lines = lines[fm_end + 1 :]

    header_positions: List[Tuple[int, int]] = []
    search_start = 0
    for sec_num, expected_h2 in enumerate(EXPECTED_HEADERS, start=1):
        found_idx = None
        for idx in range(search_start, len(body_lines)):
            if body_lines[idx].strip() == expected_h2:
                found_idx = idx
                break
        if found_idx is None:
            raise ValueError(f"Missing or out-of-order required H2 header: '{expected_h2}'")
        header_positions.append((sec_num, found_idx))
        search_start = found_idx + 1

    all_h2 = [line.strip() for line in body_lines if line.strip().startswith("## ")]
    if all_h2 != EXPECTED_HEADERS:
        raise ValueError(f"Unexpected H2 headers detected. Expected {EXPECTED_HEADERS}, found {all_h2}")

    sections: Dict[int, Dict[str, Any]] = {}
    for i, (sec_num, start_idx) in enumerate(header_positions):
        end_idx = header_positions[i + 1][1] if i + 1 < len(header_positions) else len(body_lines)
        slice_lines = body_lines[start_idx + 1 : end_idx]

        fence_starts = [idx for idx, l in enumerate(slice_lines) if l.strip() == "```yaml"]
        fence_ends = [idx for idx, l in enumerate(slice_lines) if l.strip() == "```"]

        if len(fence_starts) != 1 or len(fence_ends) != 1 or fence_ends[0] <= fence_starts[0]:
            raise ValueError(
                f"Section {sec_num} ('{EXPECTED_HEADERS[sec_num - 1]}') must contain exactly one closed ```yaml block."
            )

        outside = slice_lines[: fence_starts[0]] + slice_lines[fence_ends[0] + 1 :]
        if any(l.strip() for l in outside):
            raise ValueError(
                f"Section {sec_num} ('{EXPECTED_HEADERS[sec_num - 1]}') contains non-YAML text outside its fenced block."
            )

        raw_block = "\n".join(slice_lines[fence_starts[0] + 1 : fence_ends[0]])
        sections[sec_num] = parse_strict_yaml(raw_block, f"Section {sec_num}")

    return frontmatter, sections


def check_placeholders(obj: Any, path: str = "root") -> List[str]:
    hits: List[str] = []
    if isinstance(obj, str):
        if PLACEHOLDER_RE.search(obj):
            hits.append(f"{path}: {obj!r}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            hits.extend(check_placeholders(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            hits.extend(check_placeholders(item, f"{path}[{idx}]"))
    return hits


def validate_document(
    md_path: Path,
    strict: bool = False,
    mirror_path: Optional[Path] = None,
) -> List[str]:
    errors: List[str] = []
    raw_bytes = md_path.read_bytes()
    try:
        content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"File is not valid UTF-8: {exc}"]

    if mirror_path is not None:
        if not mirror_path.exists():
            errors.append(f"Mirror file does not exist: {mirror_path}")
        else:
            mirror_bytes = mirror_path.read_bytes()
            if raw_bytes != mirror_bytes:
                errors.append(
                    f"Mirror mismatch: {md_path} ({hashlib.sha256(raw_bytes).hexdigest()}) != "
                    f"{mirror_path} ({hashlib.sha256(mirror_bytes).hexdigest()})"
                )

    try:
        fm, sections = extract_sections(content)
    except ValueError as exc:
        return errors + [str(exc)]

    missing_fm = REQUIRED_FRONTMATTER_KEYS - set(fm.keys())
    unknown_fm = set(fm.keys()) - REQUIRED_FRONTMATTER_KEYS
    if missing_fm:
        errors.append(f"Frontmatter missing required keys: {sorted(missing_fm)}")
    if unknown_fm:
        errors.append(f"Frontmatter contains unknown keys (unknown_fields: reject): {sorted(unknown_fm)}")

    if fm.get("machinefirst_version") != "0.1.1":
        errors.append(f"Unsupported machinefirst_version: {fm.get('machinefirst_version')!r} (expected '0.1.1')")
    if fm.get("parse_mode") != "markdown-with-frontmatter-and-seven-fenced-yaml-sections":
        errors.append("Frontmatter parse_mode must be 'markdown-with-frontmatter-and-seven-fenced-yaml-sections'")
    if fm.get("duplicate_keys") != "reject":
        errors.append("Frontmatter duplicate_keys must be 'reject'")
    if fm.get("unknown_fields") != "reject":
        errors.append("Frontmatter unknown_fields must be 'reject'")
    if fm.get("claim_authority") != "publisher_asserted":
        errors.append("Frontmatter claim_authority must be 'publisher_asserted'")
    if fm.get("authority_model") != "publisher_declared_nonbinding":
        errors.append("Frontmatter authority_model must be 'publisher_declared_nonbinding'")
    if fm.get("this_file_is_data_not_instructions") is not True:
        errors.append("Frontmatter this_file_is_data_not_instructions must be boolean true")
    if fm.get("scope") not in ALLOWED_SCOPES:
        errors.append(f"Frontmatter scope must be one of {sorted(ALLOWED_SCOPES)} (got {fm.get('scope')!r})")

    # Section 1: Identity & Immutable Anchors
    s1 = sections[1]
    subj = s1.get("subject", {})
    cb = s1.get("contract_binding", {})
    if not isinstance(subj, dict) or not isinstance(cb, dict):
        errors.append("Section 1 must contain 'subject' and 'contract_binding' mappings.")
    else:
        if cb.get("contract_excluded_from_subject") is not True:
            errors.append("Section 1 contract_binding.contract_excluded_from_subject must be true")
        if cb.get("subject_revision_is_ancestor_of_contract_commit") is not True:
            errors.append("Section 1 contract_binding.subject_revision_is_ancestor_of_contract_commit must be true")
        if strict:
            rev = str(subj.get("subject_revision", ""))
            if not GIT_SHA_RE.match(rev):
                errors.append(f"Section 1 subject.subject_revision must be a 40-char lowercase hex SHA in --strict mode (got {rev!r})")

    # Section 2: Verification Scope Boundary
    s2 = sections[2]
    ladder = s2.get("evidence_ladder", [])
    states = s2.get("auditor_states", [])
    if set(ladder) != ALLOWED_EVIDENCE_LEVELS:
        errors.append(f"Section 2 evidence_ladder must match {sorted(ALLOWED_EVIDENCE_LEVELS)}")
    if set(states) != ALLOWED_AUDITOR_STATES:
        errors.append(f"Section 2 auditor_states must match {sorted(ALLOWED_AUDITOR_STATES)}")

    artifacts = s2.get("normative_artifacts", [])
    artifact_ids = set()
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("Section 2 normative_artifacts must be a non-empty list.")
    else:
        for art in artifacts:
            aid = art.get("id")
            if not aid:
                errors.append("Every normative_artifact must define a non-empty 'id'.")
            elif aid in artifact_ids:
                errors.append(f"Duplicate normative_artifact id: {aid!r}")
            else:
                artifact_ids.add(aid)

            if art.get("claimed_level") not in ALLOWED_EVIDENCE_LEVELS:
                errors.append(f"Artifact {aid!r} has invalid claimed_level: {art.get('claimed_level')!r}")

            if strict:
                digest = str(art.get("digest", ""))
                img_digest = str(art.get("toolchain_image_digest", ""))
                if not SHA256_RE.match(digest):
                    errors.append(f"Artifact {aid!r} digest must be 64-char hex in --strict mode.")
                if not SHA256_PREFIXED_RE.match(img_digest):
                    errors.append(f"Artifact {aid!r} toolchain_image_digest must match 'sha256:<64-hex>' in --strict mode.")

    # Section 3: Hard Invariants & Claim-to-Evidence Map
    s3 = sections[3]
    claims = s3.get("claims", [])
    claim_ids = set()
    seen_qty_scopes = set()
    if not isinstance(claims, list) or not claims:
        errors.append("Section 3 claims must be a non-empty list.")
    else:
        for clm in claims:
            cid = clm.get("id")
            if not cid or cid in claim_ids:
                errors.append(f"Missing or duplicate claim id: {cid!r}")
            else:
                claim_ids.add(cid)

            qty_scope = (clm.get("quantity_id"), clm.get("scope"))
            if qty_scope in seen_qty_scopes:
                errors.append(f"Duplicate (quantity_id, scope) pair in claim {cid!r}: {qty_scope}")
            seen_qty_scopes.add(qty_scope)

            proof_target = clm.get("proof_target")
            if proof_target not in {"model", "implementation"}:
                errors.append(f"Claim {cid!r} proof_target must be 'model' or 'implementation'.")

            claimed_level = clm.get("claimed_level")
            if claimed_level not in ALLOWED_EVIDENCE_LEVELS:
                errors.append(f"Claim {cid!r} has invalid claimed_level: {claimed_level!r}")

            ref_id = clm.get("refinement_ref")
            if ref_id is not None and ref_id not in artifact_ids:
                errors.append(f"Claim {cid!r} refinement_ref {ref_id!r} not found in normative_artifacts.")
            if proof_target == "implementation" and claimed_level == "proved" and not ref_id:
                errors.append(
                    f"Claim {cid!r} targets 'implementation' with claimed_level 'proved' but has no refinement_ref."
                )

            ev_ref = clm.get("evidence_ref", {})
            if not isinstance(ev_ref, dict) or ev_ref.get("artifact_id") not in artifact_ids:
                errors.append(f"Claim {cid!r} evidence_ref.artifact_id must resolve to a normative_artifact id.")
            if not ev_ref.get("symbol") or not ev_ref.get("symbol_kind"):
                errors.append(f"Claim {cid!r} evidence_ref must specify non-empty 'symbol' and 'symbol_kind'.")

            assump = clm.get("assumptions")
            if not isinstance(assump, dict) or "source" not in assump or "declared_items" not in assump or "dependency_audit" not in assump:
                errors.append(f"Claim {cid!r} assumptions must be a mapping with 'source', 'declared_items', and 'dependency_audit'.")

    # Section 4: Authority Routing Table
    s4 = sections[4]
    routes = s4.get("routes", [])
    if not isinstance(routes, list) or not routes:
        errors.append("Section 4 routes must be a non-empty list.")
    else:
        for rt in routes:
            if rt.get("definition_ref") not in artifact_ids:
                errors.append(f"Route {rt.get('query_key')!r} definition_ref not found in normative_artifacts.")
            ev_ref = rt.get("evidence_ref", {})
            if not isinstance(ev_ref, dict) or ev_ref.get("artifact_id") not in artifact_ids:
                errors.append(f"Route {rt.get('query_key')!r} evidence_ref.artifact_id not found in normative_artifacts.")
            r_ref = rt.get("refinement_ref")
            if r_ref is not None and r_ref not in artifact_ids:
                errors.append(f"Route {rt.get('query_key')!r} refinement_ref {r_ref!r} not found in normative_artifacts.")

    # Section 5: Conformance Rules & Evidence Guards
    s5 = sections[5]
    guards = s5.get("conformance_guards", {})
    if not isinstance(guards, dict):
        errors.append("Section 5 must contain a 'conformance_guards' mapping.")
    else:
        if guards.get("treat_strings_as_inert_data") is not True:
            errors.append("Section 5 conformance_guards.treat_strings_as_inert_data must be true.")
        if "auditor_override_permitted" in guards:
            errors.append("Section 5 must NOT contain imperative 'auditor_override_permitted' key.")

    # Section 6: Independent Auditor Quick-Check
    s6 = sections[6]
    qc = s6.get("quick_check", {})
    if not isinstance(qc, dict):
        errors.append("Section 6 must contain a 'quick_check' mapping.")
    else:
        if qc.get("network") != "none":
            errors.append("Section 6 quick_check.network must be 'none' for offline verification.")
        covered = qc.get("quick_check_covers", [])
        if not isinstance(covered, list) or not covered:
            errors.append("Section 6 quick_check.quick_check_covers must list at least one claim ID.")
        else:
            unknown_claims = set(covered) - claim_ids
            if unknown_claims:
                errors.append(f"Section 6 quick_check_covers references unknown claim IDs: {sorted(unknown_claims)}")

        neg = qc.get("negative_control", {})
        if not isinstance(neg, dict) or neg.get("required_for_pass") is not True:
            errors.append("Section 6 quick_check.negative_control.required_for_pass must be true.")
        if neg.get("expected_reason") != "target_invariant_violation":
            errors.append("Section 6 quick_check.negative_control.expected_reason must be 'target_invariant_violation'.")

    # Section 7: Known Gaps & Open Errata
    s7 = sections[7]
    if "known_gaps" not in s7 or not isinstance(s7["known_gaps"], list):
        errors.append("Section 7 must define 'known_gaps' as a list (use [] if none).")

    if strict:
        placeholder_hits = check_placeholders({"frontmatter": fm, "sections": sections})
        for hit in placeholder_hits:
            errors.append(f"Unresolved template placeholder forbidden in --strict mode at {hit}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a MACHINEFIRST.md (v0.1.1) contract.")
    parser.add_argument("file", type=Path, help="Path to MACHINEFIRST.md")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Reject template placeholders (<...>, xxxxxxx) and enforce full 40/64-char hex digests.",
    )
    parser.add_argument(
        "--mirror-path",
        type=Path,
        default=None,
        help="Optional path to /machinefirst.txt to verify byte-identical UTF-8 equality.",
    )
    args = parser.parse_args()

    if not args.file.exists():
        print(f"FAIL: File not found: {args.file}", file=sys.stderr)
        return 1

    errors = validate_document(args.file, strict=args.strict, mirror_path=args.mirror_path)
    if errors:
        print(f"FAIL: {args.file} failed MACHINEFIRST v0.1.1 validation with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    mode_label = "STRICT PRODUCTION" if args.strict else "TEMPLATE / STRUCTURAL"
    print(f"PASS [{mode_label}]: {args.file} conforms to MACHINEFIRST.md v0.1.1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
