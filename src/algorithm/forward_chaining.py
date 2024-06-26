from src.horn_knowledge_base import HornKnowledgeBase
from src.inference_algorithm import InferenceAlgorithm
from src.query import HornKnowledgeBaseQuery
from src.result.chaining_result import ChainingResult
from src.syntax.literal import PositiveLiteral
from src.syntax.sentence import Sentence


class ForwardChaining(InferenceAlgorithm):

    def __init__(self):
        super().__init__("FC")

    # NOTE: Because we use a queue and the symbols are ordered by the order that appear left to right in the string
    # the results may be different from the provided implementation

    # ? I'm not sure what ordering they use but maybe it's alphabetical?

    # uses horn kb
    def run(
        self, knowledge_base: HornKnowledgeBase, query: HornKnowledgeBaseQuery
    ) -> ChainingResult:
        # gets the counts of symbols in the body of each sentence
        count = self.init_count(knowledge_base)

        # the agenda is a list of symbols that we need to check
        agenda: list[PositiveLiteral] = list(knowledge_base.facts)

        # wanted result
        wanted = query.positive_literal

        # entailed symbols
        entailed = set()

        # while there are symbols in the agenda
        while len(agenda) > 0:
            # get the first symbol in the agenda
            p = agenda.pop(0)

            # skip if in entailed
            if p in entailed:
                continue

            # we have entailed the consequent
            entailed.add(p)

            # we found the wanted symbol
            if wanted == p:
                return ChainingResult(self.name, True, entailed | set(agenda))

            # for every sentence in the kb
            for clause in knowledge_base.rules:

                # if the symbol is in the body of the sentence
                if p in clause.body:
                    # decrement the count of the symbol in the body
                    count[clause] -= 1

                    # if all the symbols in the body are in the entailed symbols
                    if count[clause] == 0:

                        # add the head of the sentence to the agenda
                        agenda.append(clause.head)

        # we couldn't find it
        return ChainingResult(self.name, False, entailed | set(agenda))

    # init count
    def init_count(self, knowledge_base: HornKnowledgeBase) -> dict[Sentence, int]:
        # dict for sentence to count of symbols in body lookup eg. A & B => C; count = 2
        count = {}

        # for every clause count the number of symbols in the body
        for clause in knowledge_base.rules:
            # add the count to the dict
            count[clause] = len(clause.body)

        return count
