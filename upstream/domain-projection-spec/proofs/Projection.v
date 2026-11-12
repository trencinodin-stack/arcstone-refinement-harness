(* Upstream Abstract Specification: Domain Projection & Invariant I1 *)
(* Master Anchor: A-77-DELTA-SHIELD-LOCKED *)

Require Import Coq.Init.Datatypes.
Require Import Coq.ZArith.BinInt.

Section AbstractSafety.

Record Capability := {
  is_explicit : bool;
  is_valid : bool;
  action_id : nat
}.

Record Observation := {
  raw_signal : nat;
  noise_bound : nat;
  threshold : nat
}.

Definition abstract_safe (obs : Observation) (c : Capability) : Prop :=
  (obs.(raw_signal) <= obs.(threshold))%nat /\
  c.(is_explicit) = true /\
  c.(is_valid) = true.

Definition abstract_eval (obs : Observation) (c : Capability) : bool :=
  Nat.leb obs.(raw_signal) obs.(threshold) &&
  c.(is_explicit) &&
  c.(is_valid).

Theorem abstract_eval_sound : forall obs c,
  abstract_eval obs c = true -> abstract_safe obs c.
Proof.
  intros obs c H.
  unfold abstract_eval in H.
  apply andb_true_iff in H as [H1 Hc].
  apply andb_true_iff in H1 as [Hsig Hexp].
  unfold abstract_safe.
  split; [apply Nat.leb_le, Hsig | split; assumption].
Qed.

End AbstractSafety.
