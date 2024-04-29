# Propositional Logic Inference Engine

Propositional Logic Inference Engine written in Python that supports Truth Table checking (TT), Backward Chaining (BC) and Forward Chaining (FC). 

It should take Horn-form Knowledge Base and Query that determines if the Query can be satisified by the Knowledge Base.

Truth Table checking works with all knowledge bases. Forward Chaining and Backward Chaining only work with a Horn Knowledge Base.

## Command Line Requirements

- Able to run on Windows 10
- Accessible through DOS (.bat) entry
- Support command as "iengine \<filename> \<method>" eg. "iengine test1.txt FC"
- Method types are TT, FC, BC
- Support command as "python iengine.py \<filename> \<method>" eg. "python iengine.py FC"
  
## Output Requirements

- For all methods it outputs YES or NO to denote whether the query is satisfied but have different individual outputs
- For TT, it should produce an output as "\<YES/NO>: \<number_of_models_of_KB>" eg. "YES: 3"
- For FC or BC, it should produce an output as "\<YES/NO>: \<list_of_propositional_symbols>" eg. "YES: a, b, p2, p3, p1, c, e, f, d"
- The list of propositional symbols should be separated by ", " (comma and space)
- There is a space after the colon

## Marking (100 marks)

- TT, working perfectly (25 marks)
- FC, working perfectly (20 marks)
- BC, working perfectly (20 marks)
- Testing, at least 16 test cases covering different scenarios. Results have been checked and documented (10 marks)
- Report, clear and sufficient information about the programs and solutions, and about your teamwork (10 marks)
- Research, shows initiative to researching the problem and solutions or carrying out extensive tests to provide interesting data about the algorithms, or optimisations, etc., a section of the report explains these well (15 marks)
- Poor programming practice (Up to -10 marks)
- Poor teamwork (Up to -20 marks)
- Failure to demonstrate weekly progress (Up to -40 marks)

**Since the work is completed in pairs the report is expected to be of a very high quality with multiple and detailed research initiatives**

## Note about General Knowledge Base Research Initiative

- One option for additional research is to allow the program to work with general Knowledge Bases instead of a Horn Knowledge base
- This will allow the Truth Table checking algorithm to deal with general knowledge bases and a generic theorem prover such as resolution-based
- If this option is chosen, the following syntax is required:
  - ~ for negation (¬) 
  - & for conjunction (∧)
  - || for disjunction (∨)
  - => for implication (⇒)
  - <=> for biconditional (⇔) 