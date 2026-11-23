# Census preregistration, version 1

Frozen before any stage-2 census is run on Harry's server. These definitions
respond to Daniel Fairbanks's second comment. Source pin:
`753431bfe28701f6f3937f664fcaf08daa139c03`; Mathlib pin:
`0df444a360eaa60ab8c11dca51a86af692955474`; Lean 4.33.1.

## Primary semantic categories

1. **Prop-valued predicates definitionally True.** For a stored definition,
   open all leading function binders in its declared type, apply its stored
   value to those fresh variables, confirm the result type is `Prop`, and
   test definitional equality of the resulting proposition with `True` under
   `.all` transparency. This is not a logical tautology test. For example,
   `fun n => n = n` is not counted merely because it has an easy proof.
   The same test is available on inspected constructor fields. Declaration
   sites and field sites are distinguished by their reported locations.
2. **Fields of unit type.** At an inspected structure-constructor argument,
   open the field's leading function binders and reduce the result type. It
   must have head `PUnit` or `Unit`. A field that *returns a type* equal to
   `PUnit` belongs to a separate auxiliary category, not this primary class.
   Thus a unit-valued field family and a unit-*type*-valued family are not
   silently conflated.
3. **Zero linear maps and zero measures.** After opening leading binders,
   the value's reduced type must have head `LinearMap`,
   `ContinuousLinearMap`, or `MeasureTheory.Measure`. Construct the zero
   value at that exact type via its `Zero` instance and test definitional
   equality under `.all` transparency. An arbitrary constant or scalar zero
   is not counted. Maps that are provably zero but not definitionally zero
   are outside this class.

The primary classes overlap where appropriate. They are supplemented, and
never replaced, by a clearly labelled syntactic census and auxiliary
unit-family counts. No class is labelled suspicious or invalid by definition.

## Denominators and coverage

The reference union starts at the five headline declarations and follows
stored types plus definition, theorem, and opaque bodies. Structural registry
edges are excluded, matching stage 1's reference mode. The semantic value
tests examine every **definition** discovered in that union, not theorem proof
values as though they were mathematical data.

Field inspection examines the reduced outer record of each definition and
record-valued fields recursively to depth 4. It uses structure metadata and
constructor argument positions. It does not claim to enumerate every
anonymous record embedded arbitrarily deeply in every proof body. That
wider field census remains open. Repeated sites in distinct declaration
values are counted as distinct sites, not as unique mathematical objects.

Report closure size, definitions attempted/completed/unknown, constructor
fields actually visited, and depth-limited definitions. Each definition has a
fresh MetaM state and a bounded heartbeat budget. Failed, timed-out, or
stuck tests are **unknown**, never confirmed nontrivial cases. A completed
traversal is not the assertion that every semantic test was decided.

Aggregate rows include counts and up to 12 example locations per category.
The `definitions/at-least-one-hit` row counts definitions containing at least
one classified site; it does not say their entire values are True or zero.
The `classified-sites` row's denominator is classified hit sites, so it is
not an estimate of the fraction of all fields that are trivial.

## Use roles: a separate question

The edge classifier separates stored binder domains, conclusion types,
definition/proof/opaque bodies, and structural registries. Multiple roles
can coexist. Binder domains include type parameters, instances, data, and
propositional hypotheses; position alone does not identify which one applies.

The semantic census does **not** infer that a classified value is a witness
discharging a hypothesis. Nor does it call every other occurrence ordinary.
A complete whole-closure split into witness-supplying and ordinary uses is
**not implemented in version 1**. Those counts must remain unestablished.
The named witness paths provide a bounded set for subsequent typed
application-site review. This limitation is a result boundary, not a zero
count. Publication should state it explicitly.

## Controls

Fresh process; import `Mathlib` without `Main`; assert the project headline
constant is absent. Control roots are fixed as `Nat.exists_infinite_primes`,
`Real.exp_add`, and `MeasureTheory.integral_add`. Apply exactly the same
reference traversal, semantic procedure, limits, category definitions, and
reporting to that union. If a root is missing at the pin, stop and amend the
preregistration before counting; do not silently substitute a favourable root.

Report actual control size. This selection spans elementary number theory,
analysis and measure theory; it is **not assumed to match** the headline
union's size or subject. A matched-size control remains open if the actual
sizes differ substantially. Report internal Mathlib-origin cohorts
separately; they share the proof closure and are not independent controls.

## Interpretation

A definitional-triviality count does not establish mathematical invalidity,
necessity, intention, or the correctness of the final statement. A difference
between unmatched cohorts is descriptive. Neither a p-value nor a verdict
should be manufactured from it. Semantic tests use Lean's metaprogramming
API; independent kernel results and the pending Comparator remain separate.
