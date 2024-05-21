from src.knowledge_base import KnowledgeBase
from src.syntax.literal import Literal
from src.syntax.sentence import Sentence

class CNFKnowledgeBase(KnowledgeBase):

    def __init__(self, propositional_symbols: set[Literal], cnf_sentences: list[Sentence]):
        super().__init__(cnf_sentences, propositional_symbols)

    @classmethod
    def from_generic_knowledge_base(cls, knowledge_base: KnowledgeBase):
        # get the cnf version of all the sentences
        cnf_sentences = []

        for sentence in knowledge_base.sentences:
            cnf_sentences.append(sentence.get_cnf())

        return cls(knowledge_base.propositional_symbols, cnf_sentences)