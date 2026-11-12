(* ARC-MONO-2026-REFINEMENT-01 *)
(* Theorem: One-Way Forward Safety Refinement (Rust_Impl <= Coq_Spec) *)
(* Master Hash Anchor: A-77-DELTA-SHIELD-LOCKED *)

Require Import Coq.Init.Datatypes.
Require Import Coq.Bool.Bool.
Require Import Coq.Arith.PeanoNat.
Require Import DPP.Invariants.
Require Import DPP.Projection.
Require Import ArcstoneExtracted.ArcstoneExtracted_Types.

Import DPP.Invariants.
Import DPP.Projection.

Section RefinementProof.

(** Theorem 1: One-Way Forward Safety Simulation *)
Theorem one_way_forward_simulation :
  forall (st : ConcreteState),
    evaluate_d_robust st = true ->
    (project st.(r_obs) st.(r_cap) st.(r_threshold)).(passed_airlock) = true.
Proof.
  intros st H_eval.
  unfold evaluate_d_robust in H_eval.
  unfold project. simpl.
  apply andb_true_iff in H_eval as [H1 _].
  apply andb_true_iff in H1 as [H2 _].
  apply andb_true_iff in H2 as [H3 _].
  apply andb_true_iff in H3 as [H4 _].
  exact H4.
Qed.

(** Theorem 2: Preservation of Invariant I1 across the Simulation Boundary *)
Theorem simulation_preserves_I1 :
  forall (st : ConcreteState),
    evaluate_d_robust st = true ->
    st.(r_cap).(is_explicit) = true /\ st.(r_cap).(is_valid) = true.
Proof.
  intros st H_eval.
  apply one_way_forward_simulation in H_eval.
  apply projection_preserves_I1 in H_eval.
  exact H_eval.
Qed.

(** Theorem 3: Fail-Closed Trip Preservation on Invalid Capability *)
Theorem fail_closed_trip_preservation :
  forall (st : ConcreteState),
    st.(r_cap).(is_valid) = false ->
    mechanical_stop_tripped (project st.(r_obs) st.(r_cap) st.(r_threshold)) = true.
Proof.
  intros st H_invalid.
  apply trip_guarantee_on_invalid_cap.
  exact H_invalid.
Qed.

End RefinementProof.
