from src.algorithm_result import AlgorithmResult
from src.inference_algorithm import InferenceAlgorithm
from src.knowledge_base import KnowledgeBase
from src.query import Query
from src.result.chaining_result import ChainingResult
from src.syntax.literal import Literal
from src.syntax.sentence import AtomicSentence, Expression, Sentence

# TODO implement the ForwardChaining class
class ForwardChaining(InferenceAlgorithm):

    def __init__(self):
        super().__init__("FC")

    # Horn Clause implication form is always A & B & C => D with all positive literals, there cannot be any negative literals
    # more info: https://stackoverflow.com/questions/45123756/why-do-we-call-a-disjunction-of-literals-of-which-none-is-positive-a-goal-clause
    
    # NOTE: I'm not sure if the horn query is always a single positive literal, but I'm assuming it is for now
    # this is something to verify

    # ? Is the query always a single positive literal?

    # NOTE: Because we use a queue and the symbols are ordered by the order thet appear left to right in the string
    # the results may be different from the provided implementation

    # ? I'm not sure what ordering they use but maybe it's alphabetical?
    
    def run(self, knowledge_base: KnowledgeBase, query: Query) -> AlgorithmResult:
        count = self.init_count(knowledge_base)
        inferred = {}

        # agenda is the list of symbols that are true
        agenda: list[Literal]= self.init_agenda(knowledge_base)

        # keep track of entailed symbols
        entailed = list(agenda)

        while len(agenda) > 0:
            # get the first of the agenda as the symbol
            true_symbol = agenda.pop(0)

            # assumes that query sentence is atomic with a single symbol not true or false
            sentence: AtomicSentence = query.sentence

            # get the atom
            atom: Literal = sentence.atom

            # check if the current symbol is the query we are looking for
            if true_symbol == atom:

                # we found that q is true
                return ChainingResult(self.name, True, entailed)
            
            # if we haven't inferred the symbol yet then let's do it
            if true_symbol not in inferred:

                # add the current symbol to inferred so we don't check it again
                inferred[true_symbol] = True

                # check each sentence in the knowledge base for the symbol in the body
                for sentence in knowledge_base.sentences:

                    # only check if the symbol is in the sentence
                    if sentence.symbol_in_sentence(true_symbol):

                        # decrement count[sentence] because we have inferred a symbol
                        count[sentence] -= 1

                        # if we have inferred all the symbols in the sentence, then we can infer the conclusion
                        if count[sentence] == 0:
                            # add the conclusion (because it has been inferred)

                            # atomic sentence means that the conclusion is a single symbol
                            # eg. A;
                            if isinstance(sentence, AtomicSentence):
                                # add the symbol to the agenda
                                agenda.append(sentence.atom)

                            else:
                                # otherwise, we need to infer the conclusion as the atom of the RHS
                                # eg. A => B;

                                # get the positive symbol
                                atom = self.get_positive_symbol(sentence)

                                agenda.append(atom)

                                # we have inferred the conclusion
                                entailed.append(atom)


        # we couldn't find it
        return ChainingResult(self.name, False, inferred)
    
    def get_positive_symbol(self, sentence: Expression) -> Literal:
        # the conclusion is always one symbol on the RHS
        rhs: AtomicSentence = sentence.rhs
        return rhs.atom

    # init agenda
    def init_agenda(self, knowledge_base: KnowledgeBase) -> list[Literal]:
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
                # get lhs eg. A & B => C; lhs = A & B
                lhs = sentence.lhs

                # checks to see if the symbol is in the LHS of the sentence eg. from A & B check every symbol, A, B, C etc.
                for symbol in symbols.values():

                    # if it is in the sentence
                    if lhs.symbol_in_sentence(symbol):

                        # increment the count (number of symbols required to infer the conclusion)
                        count[sentence] = count.get(sentence, 0) + 1
            else:
                # init count to 1
                count[sentence] = 1

        return count