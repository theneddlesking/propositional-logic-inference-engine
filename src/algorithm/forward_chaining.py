from src.algorithm_result import AlgorithmResult
from src.inference_algorithm import InferenceAlgorithm
from src.knowledge_base import KnowledgeBase
from src.query import Query
from src.result.chaining_result import ChainingResult
from src.syntax.proposition_symbol import PropositionSymbol
from src.syntax.sentence import AtomicSentence, Expression, Sentence

# TODO implement the ForwardChaining class
class ForwardChaining(InferenceAlgorithm):
    def __init__(self):
        super().__init__("FC")

    # TODO make this work only with horn kb because it is forward chaining
    # TODO we also need a query specific for horn kb because it has to be a single proposition symbol
    def run(self, knowledge_base: KnowledgeBase, query: Query) -> AlgorithmResult:
        count = self.init_count(knowledge_base)
        inferred = {}

        agenda: list[PropositionSymbol]= self.init_agenda(knowledge_base)

        while len(agenda) > 0:
            # get the first of the agenda as the symbol
            p = agenda.pop(0)

            # assumes that query sentence is atomic with a single symbol not true or false
            sentence: AtomicSentence = query.sentence

            # get the atom
            atom: PropositionSymbol = sentence.atom

            # check if p is the query we are looking for
            if p == atom:
                # we found q
                return ChainingResult(self.name, True, len(inferred))
            
            # does inferred have p?
            if p not in inferred:
                # add p to inferred
                inferred[p] = True

                # for each sentence in kb
                for sentence in knowledge_base.sentences:

                    # if p in sentence
                    if sentence.symbol_in_sentence(p):

                        # decrement count[sentence]
                        count[sentence] -= 1

                        if count[sentence] == 0:
                            # add conclusion
                            if isinstance(sentence, AtomicSentence):
                                # add the symbol to the agenda
                                agenda.append(sentence.atom)
                            else:
                                # add the conclusion to the agenda
                                sentence: Expression

                                # assumes that the conclusion is always one symbol on the RHS
                                rhs: AtomicSentence = sentence.rhs

                                # add the symbol to the agenda
                                agenda.append(rhs.atom)

        # we couldn't find it
        return ChainingResult(self.name, False, len(inferred))

    # init agenda
    def init_agenda(self, knowledge_base: KnowledgeBase) -> list[PropositionSymbol]:
        agenda = []

        for sentence in knowledge_base.sentences:
            # if sentence is an atomic sentence
            if isinstance(sentence, AtomicSentence):
                # add only the symbol to the agenda
                agenda.append(sentence.atom)

        return agenda
    
    # init count
    def init_count(self, knowledge_base: KnowledgeBase) -> dict[Sentence, int]:
        count = {}

        symbols = knowledge_base.propositional_symbols

        # for every top level sentence, count the number of symbols in the sentence
        for sentence in knowledge_base.sentences:
            if isinstance(sentence, Expression):
                # get number of symbols on LHS
                lhs = sentence.lhs

                # checks to see if the symbol is in the sentence
                for symbol in symbols.values():
                    if lhs.symbol_in_sentence(symbol):
                        count[sentence] = count.get(symbol, 0) + 1
            else:
                # otherwise is atomic
                sentence: AtomicSentence

                # init count to 1
                count[sentence] = 1

        return count