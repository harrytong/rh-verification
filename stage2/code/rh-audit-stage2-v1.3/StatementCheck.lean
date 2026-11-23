import Main

set_option pp.fullNames true
set_option pp.universes true

#print RiemannHypothesis
#check riemannHypothesis
example : RiemannHypothesis := riemannHypothesis

-- An explicit spelling of the RH statement, independent of the alias's name.
example : ∀ s : Complex, riemannZeta s = 0 →
    (¬∃ n : Nat, s = -2 * ((n : Complex) + 1)) →
    s ≠ 1 → s.re = 1 / 2 := riemannHypothesis

#print RiemannZetaZerosOnLine
#print DirichletLNonvanishingRightOfHalf
#print DirichletLZerosOnLine
#print PrimitiveDirichletLZerosOnLine
example : RiemannZetaZerosOnLine := riemannZeta_eq_zero_re
example : DirichletLNonvanishingRightOfHalf := LFunction_ne_zero_of_half_lt_re
example : DirichletLZerosOnLine := LFunction_eq_zero_re
example : PrimitiveDirichletLZerosOnLine := LFunction_eq_zero_re_of_isPrimitive

#print axioms riemannHypothesis
#print axioms riemannZeta_eq_zero_re
#print axioms LFunction_ne_zero_of_half_lt_re
#print axioms LFunction_eq_zero_re
#print axioms LFunction_eq_zero_re_of_isPrimitive

-- Only reached after all commands above have been elaborated without an error.
-- The runner also requires process exit status 0.
#eval IO.println "RH_STAGE2_STATEMENT_COMMANDS_REACHED_END"
