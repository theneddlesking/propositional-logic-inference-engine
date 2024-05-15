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
            # facts
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

            # rules
            # convert expressions to horn clauses
            if isinstance(sentence, Expression):
                # get the rule from the expression
                rule = HornClause.from_expression(sentence, knowledge_base.propositional_symbols)

                rules.append(rule)

        return cls(facts, rules, knowledge_base.propositional_symbols, knowledge_base.sentences)

    def __str__(self):
        facts = ", ".join([str(fact) for fact in self.facts])

        rules = "\n".join([str(rule) for rule in self.rules])

        original = super().__str__()

        return f"{original}\nFacts:\n{facts}\nRules:\n{rules}"
