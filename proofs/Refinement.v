(* ARC-MONO-2026-REFINEMENT-01 *)
(* Theorem: One-Way Forward Safety Refinement (Rust_Impl <= Coq_Spec) *)
(* Master Hash Anchor: A-77-DELTA-SHIELD-LOCKED *)

Require Import Coq.Init.Datatypes.
Require Import Coq.ZArith.BinInt.
Require Import ArcstoneSpec.Projection.
Require Import ArcstoneExtracted.ArcstoneExtracted_Types.

Section RefinementProof.

Theorem one_way_forward_simulation :
  forall (st : ConcreteState),
    evaluate_d_robust st = true ->
    abstract_safe st.(r_obs) st.(r_cap).
Proof.
  intros st H_eval.
  unfold evaluate_d_robust in H_eval.
  repeat (apply andb_true_iff in H_eval as [H_eval ?]).
  repeat (apply andb_true_iff in H_eval as [H_eval ?]).
  unfold abstract_safe.
  split.
  - apply Nat.leb_le. assumption.
  - split; assumption.
Qed.

Theorem fail_closed_trip_preservation :
  forall (st : ConcreteState),
    st.(r_cap).(is_valid) = false ->
    evaluate_d_robust st = false.
Proof.
  intros st H_invalid.
  unfold evaluate_d_robust.
  rewrite H_invalid.
  destruct (Nat.leb (raw_signal (r_obs st)) (threshold (r_obs st))); auto.
  destruct (is_explicit (r_cap st)); auto.
Qed.

End RefinementProof.
