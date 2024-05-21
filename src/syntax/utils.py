from src.syntax.operator import Operator


# TODO refactor to remove Utils
class Utils:
    @staticmethod
    def is_propositional_symbol(string: str) -> bool:
        if len(string) == 0:
            return False

        # is letter or letter and number
        # eg. A, b, p2, P3
        first_letter_is_char = string[0].isalpha()
        if not first_letter_is_char:
            return False
        
        # length must be 1 or 2
        if len(string) > 2:
            return False
        
        # if length is 2, second char must be a number
        if len(string) == 2:
            second_char_is_num = string[1].isdigit()
            if not second_char_is_num:
                return False
            
        return True
    
    @staticmethod
    def is_negated_propositional_symbol(string: str) -> bool:
        # doesn't start with negation
        print("BRO wtf is this shit " + string)
        if string[0] != Operator.NEGATION.value:
            return False
        
        # everything after the negation should be a proposition symbol
        return Utils.is_propositional_symbol(string[1:])
    
    @staticmethod
    def is_true_false(string: str) -> bool:
        return string == "True" or string == "False"
    
    @staticmethod
    def find_matching_bracket(string: str, bracket_index: int) -> int:
        # initialize the index to the leftmost bracket index
        closing_bracket_index = bracket_index

        # amount of brackets within the string that we encounter
        inner_bracket_count = 0

        # loop through each character in the string
        for i in range(bracket_index, len(string)):
            # keep incrementing the closing bracket index
            closing_bracket_index += 1

            char = string[i]

            # if it's a closing bracket, decrement the amount of inner brackets
            # then check if we found the matching original opening bracket
            # if it's an opening bracket, increment the amount of inner brackets
            if char == Operator.CLOSING_BRACKET.value:
                inner_bracket_count -= 1

                if inner_bracket_count == 0:
                    return closing_bracket_index
            if char == Operator.OPENING_BRACKET.value:
                inner_bracket_count += 1
        # there either was no closing bracket or no matching one
        raise ValueError("No corresponding closing bracket found")
