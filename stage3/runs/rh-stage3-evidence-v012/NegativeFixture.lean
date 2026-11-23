import Lean
-- Deliberate invalid inference. Expected exit is nonzero, with a type error.
-- This is a fixture and must never be imported by a project probe.
example : False := True.intro
