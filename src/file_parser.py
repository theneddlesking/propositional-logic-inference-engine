from enum import Enum
from src.algorithm_result import AlgorithmResult
from src.knowledge_base import KnowledgeBase
from src.model import Model
from src.query import Query
from src.result.chaining_result import ChainingResult
from src.result.truth_table_checking_result import TruthTableCheckingResult
from src.syntax.literal import Literal

class FileType(Enum):
    STANDARD = 1
    CHAINING_TEST = 2
    TRUTH_TABLE_CHECKING_TEST = 3

class FileParser:

    @staticmethod
    def parse_kb_and_query(file_path: str) -> tuple[KnowledgeBase, Query]:
        with open(file_path, 'r') as file:
            # get the lines from the file
            lines = file.readlines()

            def remove_whitespace(s: str) -> str:
                return s.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
            
            # needs at least 4 lines
            if len(lines) < 4:
                raise ValueError('File must have at least 4 lines')

            # first line must be "TELL"
            if lines[0].strip() != 'TELL':
                raise ValueError('First line must be "TELL"')
            
            # third line must be "ASK"
            if lines[2].strip() != 'ASK':
                raise ValueError('Third line must be "ASK"')
            
            # second line is the knowledge base
            knowledge_base = KnowledgeBase.from_string(remove_whitespace(lines[1]))

            # fourth line is the query
            query = Query.from_string(remove_whitespace(lines[3]), knowledge_base.propositional_symbols)

            # return the knowledge base and query
            return knowledge_base, query

    @staticmethod
    def get_file_type(file_path: str) -> FileType:
        # number of lines
        number_of_lines = 0

        with open(file_path, 'r') as file:
            # get the lines from the file
            lines = file.readlines()

            # get the number of lines
            number_of_lines = len(lines)

        # less than 3 lines is invalid
        if number_of_lines < 3:
            raise ValueError('File must have at least 3 lines')

        # standard file
        if number_of_lines == 4:
            return FileType.STANDARD
        
        # horn kb test file
        if number_of_lines == 9:
            return FileType.CHAINING_TEST
        
        # general kb test file
        return FileType.TRUTH_TABLE_CHECKING_TEST
        
    @staticmethod
    def parse_test(file_path: str, file_type: FileType, algorithm_name: str) -> tuple[AlgorithmResult, str, str]:
        # can't use horn kb for anything other than FC or BC
        if algorithm_name != "FC" and algorithm_name != "BC" and file_type == FileType.CHAINING_TEST:
            raise ValueError('Chaining test file can only be used with FC or BC')
        
        # can't use general kb for anything other than TT and DPLL
        if (algorithm_name != "TT" and algorithm_name != "DPLL") and file_type == FileType.TRUTH_TABLE_CHECKING_TEST:
            raise ValueError('Truth table checking test file can only be used with TT and DPLL')

        with open(file_path, 'r') as file:
            # get the lines from the file
            lines = file.readlines()

            # get name
            name = lines[5].strip()

            # get description
            description = lines[6].strip()

            # result line is line 8 if FC or generic
            # but is line 9 if BC
            line_number = 9 if algorithm_name == "BC" else 8

            result_line = lines[line_number - 1].strip()

            # if colon is last character then there are no symbols which could be possible
            if result_line[-1] == ":":
                # the space gets trimmed off so we need to add it back for the split
                result_line += " "

            # line needs YES: or NO: in it
            if result_line.find("YES: ") == -1 and result_line.find("NO: ") == -1:
                raise ValueError('Expected result line must contain "YES" or "NO"')
            
            # found if YES is in the line
            found = result_line.find("YES: ") != -1

            # split at ": " for other output
            split = result_line.split(": ")

            # get expected result for horn kb
            if file_type == FileType.CHAINING_TEST:
                # get the set of symbols
                entailed = set(split[1].split(", "))

                # remove any empty strings
                entailed = {symbol for symbol in entailed if symbol != ""}

                # convert to literals
                entailed = {Literal(symbol) for symbol in entailed}

                return ChainingResult(algorithm_name, found, entailed), name, description
        
            # get expected result for general kb
            if file_type == FileType.TRUTH_TABLE_CHECKING_TEST:
                # number of models
                number_of_models = int(split[1])

                # if there was none found then number of models is 0
                if not found:
                    # check that number of models match
                    if number_of_models != 0:
                        raise ValueError('Number of models does not match expected number of models')

                    return TruthTableCheckingResult([], found), name, description
                
                # get models from table
                models = []

                # table could be eg.
                # a     | b     | c     | d     |
                # True  | True  | False | True  |
                # True  | True  | True  | False |
                # True  | True  | True  | True  |

                def line_to_arr(line: str):
                    return line.strip().replace(" ", "").split("|")[:-1]

                # get the symbols without any spaces
                symbols = line_to_arr(lines[8])

                # get the values
                model_value_arrs = [line_to_arr(line) for line in lines[9:]]

                # create models
                for model_values in model_value_arrs:
                    model = {}

                    for i in range(len(symbols)):
                        model[symbols[i]] = model_values[i] == "True"

                    # create model
                    model = Model(model)

                    models.append(model)
                
                result = TruthTableCheckingResult(models, found), name, description

                # check that number of models match
                if len(models) != number_of_models:
                    raise ValueError('Number of models does not match expected number of models')
            
                return result

            raise ValueError("File type not supported")