from src.knowledge_base import KnowledgeBase
from src.syntax.literal import Literal
from src.syntax.sentence import CNFSentence, Sentence

class CNFKnowledgeBase(KnowledgeBase):

    def __init__(self, propositional_symbols: set[Literal], cnf_sentences: list[Sentence]):
        super().__init__(cnf_sentences, propositional_symbols)

    @classmethod
    def from_generic_knowledge_base(cls, knowledge_base: KnowledgeBase):
        # get the cnf version of all the sentences
        cnf_sentences: list[CNFSentence] = []

        for sentence in knowledge_base.sentences:
            cnf_sentences.extend(sentence.get_cnfs())

        # filter out invalid sentences
        valid_cnf_sentences = [sentence for sentence in cnf_sentences if not sentence.is_tautology()]

        return cls(knowledge_base.propositional_symbols, valid_cnf_sentences)