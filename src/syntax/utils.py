class Utils:
    @staticmethod
    def is_proposition_symbol(string: str) -> bool:
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
    def is_true_false(string: str) -> bool:
        return string == "True" or string == "False"