# Propositional Logic Inference Engine

Propositional Logic Inference Engine written in Python that supports Truth Table checking (TT), Backward Chaining (BC) and Forward Chaining (FC). 

It should take Horn-form Knowledge Base and Query that determines if the Query can be satisified by the Knowledge Base.

Truth Table checking works with all knowledge bases. Forward Chaining and Backward Chaining only work with a Horn Knowledge Base.

It also implements an unoptimised version of the DPLL algorithm.

## Output Requirements

- For all methods it outputs YES or NO to denote whether the query is satisfied but have different individual outputs
- For TT, it should produce an output as "\<YES/NO>: \<number_of_models_of_KB>" eg. "YES: 3"
- For FC or BC, it should produce an output as "\<YES/NO>: \<list_of_propositional_symbols>" eg. "YES: a, b, p2, p3, p1, c, e, f, d"
- The list of propositional symbols should be separated by ", " (comma and space)
- There is a space after the colon

## General Knowledge Base Notation
  - ~ for negation (¬) 
  - & for conjunction (∧)
  - || for disjunction (∨)
  - => for implication (⇒)
  - <=> for biconditional (⇔) 