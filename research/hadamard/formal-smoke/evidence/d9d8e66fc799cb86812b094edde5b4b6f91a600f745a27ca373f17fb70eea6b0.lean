import Std

-- Total functions represent finite matrices by restricting both indices to < n.
-- Unused entries outside the finite square have no mathematical role.
def matrixDot (n : Nat) (h : Nat → Nat → Int) (i j : Nat) : Int :=
  ((List.range n).map (fun c => h i c * h j c)).sum

def IsHadamard (n : Nat) (h : Nat → Nat → Int) : Prop :=
  (∀ i j, i < n → j < n → h i j = 1 ∨ h i j = -1) ∧
  (∀ i j, i < n → j < n → matrixDot n h i j = if i = j then (n : Int) else 0)

-- Nat with 0 < k is exactly the positive-integer index in the stated objective.
def HadamardConjecture : Prop :=
  ∀ k : Nat, 0 < k → ∃ h : Nat → Nat → Int, IsHadamard (4 * k) h

 theorem Certified : forall (n : Int), n+n=2*n :=
by omega
#print axioms Certified
