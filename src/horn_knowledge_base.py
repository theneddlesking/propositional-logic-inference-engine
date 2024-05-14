from src.knowledge_base import KnowledgeBase
from src.syntax.literal import PositiveLiteral
from src.syntax.operator import Operator
from src.syntax.sentence import AtomicSentence, Expression, HornClause, Sentence

class HornKnowledgeBase(KnowledgeBase):

    def __init__(self, facts: list[PositiveLiteral], rules: list[HornClause], propositional_symbols: dict[str, PositiveLiteral], sentences: list[Sentence]):
        self.facts: list[PositiveLiteral] = facts
        self.rules = rules
        super().__init__(sentences, propositional_symbols)

    @classmethod
    def from_generic_knowledge_base(cls, knowledge_base: KnowledgeBase):
        facts = []
        rules = []

        for sentence in knowledge_base.sentences:
            # convert atomic sentences to positive literals
            if isinstance(sentence, AtomicSentence):
                # get literal from kb dict
                literal = knowledge_base.propositional_symbols.get(sentence.atom.name)

                if literal is None:
                    raise ValueError(f"Symbol {sentence.atom.name} not found in propositional symbols", str(sentence))
                
                # must be a positive literal
                if literal.negated:
                    raise ValueError(f"Symbol {sentence.atom.name} must be a positive literal", str(sentence))

                facts.append(literal)

            # convert expressions to horn clauses
            if isinstance(sentence, Expression):
                # check to see if the operator is an implication
                if sentence.operator != Operator.IMPLICATION:
                    raise ValueError("HornKnowledgeBase can only contain Horn Clauses (requires =>)", str(sentence))
                
                # check to see if the right hand side is an atomic sentence
                if not isinstance(sentence.rhs, AtomicSentence):
                    raise ValueError("HornKnowledgeBase can only contain Horn Clauses (requires atomic sentence on the right side)", str(sentence))
                
                # recursively check if the left hand side is a conjunction of positive literals
                def check_conjunction(sentence: Sentence):
                    if isinstance(sentence, AtomicSentence):
                        return True

                    # must be an expression
                    sentence: Expression

                    if sentence.operator != Operator.CONJUNCTION:
                        return False
                    
                    return check_conjunction(sentence.lhs) and check_conjunction(sentence.rhs)

                if not check_conjunction(sentence.lhs):
                    raise ValueError("HornKnowledgeBase can only contain Horn Clauses (requires conjunction of positive literals on the left side)", str(sentence))

                # convert the left hand side to a list of positive literals
                lhs = []
                def convert_to_list(sentence: Sentence):
                    if isinstance(sentence, AtomicSentence):
                        # get literal from kb dict
                        literal = knowledge_base.propositional_symbols.get(sentence.atom.name)

                        if literal is None:
                            raise ValueError(f"Symbol {sentence.atom.name} not found in propositional symbols", str(sentence))

                        # must be a positive literal
                        if literal.negated:
                            raise ValueError(f"Symbol {sentence.atom.name} must be a positive literal", str(sentence))
                        
                        lhs.append(literal)
                        return

                    sentence: Expression
                    convert_to_list(sentence.lhs)
                    convert_to_list(sentence.rhs)

                # converts the left hand side to a list of positive literals as lhs
                convert_to_list(sentence.lhs)

                rules.append(HornClause(lhs, sentence.rhs.atom, knowledge_base.propositional_symbols))

        return cls(facts, rules, knowledge_base.propositional_symbols, knowledge_base.sentences)

    def __str__(self):
        facts = ", ".join([str(fact) for fact in self.facts])

        rules = "\n".join([str(rule) for rule in self.rules])

        original = super().__str__()

        return f"{original}\nFacts:\n{facts}\nRules:\n{rules}"
