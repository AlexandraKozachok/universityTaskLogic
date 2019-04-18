class Alexa_boolean:
    
    special_symbols_dict = {'(' : 10,')': -10,'not': 4,'and': 3,'*': 3,'->':2,'+': 1, 'or': 1}
    BRACES_LIST = ['(',')']
    AND_LIST = ['and','*']
    OR_LIST = ['or','+']
    NOT_LIST = ['not']
    IMPLICATION_LIST = ['->']
    
    def __init__(self, xString):
        self.formula_string = xString
        self.formula_list0 = Alexa_boolean.parts_as_list(x_string)
        self.formula_list, self.level_lst = Alexa_boolean.aslist(self.formula_list0, Alexa_boolean.special_symbols_dict)
        self.function = Alexa_boolean.getasab(self.formula_list, self.level_lst)
        self.vars_list = Alexa_boolean.get_vars(self.formula_list, self.level_lst)
        self.vars_boolean = [False for x in self.vars_list]
        self.vars_boolean_len = len(self.vars_boolean)
        self.tautology = True
        flag_do = True
        while flag_do:
            var_dict = dict(zip(self.vars_list, self.vars_boolean))
            self.tautology = Alexa_boolean.execute_formula(self.function, var_dict)
            flag_do, self.vars_boolean = Alexa_boolean.nxt(self.vars_boolean, self.vars_boolean_len)
            flag_do = (flag_do and self.tautology)
    
            
    @property
    def isTautology(self):
        return self.tautology
    
    @staticmethod
    def prefix(arg_string):
        pos = 0
        arg_string = arg_string.strip()
        length = len(arg_string)
        term = ''
        if 0 < length:
            symbol = arg_string[pos]
            isalpha_flag = (symbol.isalpha() or symbol.isdigit())
            pos += 1
            if symbol in Alexa_boolean.BRACES_LIST:
                    pass
            else:
                while pos < length:
                    symbol = arg_string[pos] 
                    term += symbol
                    if symbol in Alexa_boolean.BRACES_LIST:
                        break
                    elif (symbol.isalpha() or symbol.isdigit()) == isalpha_flag:
                        pass
                    else:break
                    pos  += 1
        return (arg_string[:pos].strip(), arg_string[pos:].strip())

    @staticmethod
    def parts_as_list(arg_string):
        formula_list = []
        emergency = 0
        while 64 > emergency:
            emergency += 1
            x, y = Alexa_boolean.prefix(arg_string)
            if 0 < len(x):
                formula_list.append(x)
                arg_string = y
            else:break
        return formula_list
    
    @staticmethod
    def aslist(arg_formula_list, arg_special_symbols_dict):
        emergency = 0
        f_set = set(arg_special_symbols_dict.keys())
        pos = 0
        level = 0
        level_lst = []
        length = len(arg_formula_list)
        formula_list = []
        flag = False
        flag_f = False
        while (1024 > emergency) and (pos < length):
            emergency += 1
            term = arg_formula_list[pos]
            term_level = 0
            flag = True
            flag_f = False
            if term in f_set:
                flag_f = True
                if '(' == term:
                    level += 10
                    flag = False
                elif ')' == term:
                    level -= 10
                    flag = False
                else:
                    term_level = arg_special_symbols_dict[term]
            else:pass
            if flag:
                if flag_f:
                    level_lst.append((level + term_level))
                else:
                    level_lst.append(0)
                formula_list.append(term)
            else:pass
            pos += 1
        return (formula_list, level_lst)
    
    @staticmethod
    def asab(arg_formula, arg_level):
        temp_max = max(arg_level)
        pos = 0
        length = len(arg_formula)
        formula_list = []
        level_list = []
        emergency = 0
        while (1024 > emergency) and (pos < length):
            emergency += 1
            term = arg_formula[pos]
            term_level = arg_level[pos]
            if temp_max == term_level:
                if term in Alexa_boolean.NOT_LIST:
                    pos += 1
                    term = arg_formula[pos]
                    formula_list.append(('not', term))
                    level_list.append(0)
                else:
                    term_temp = term
                    pos += 1
                    term = arg_formula[pos]
                    formula_list.append((term_temp, formula_list.pop(), term))
                    level_list.pop()
                    level_list.append(0)
            else:
                formula_list.append(term)
                level_list.append(term_level)
            pos += 1
        return (formula_list, level_list)
    
    @staticmethod
    def getasab(arg_formula, arg_level):
        while True:
            arg_formula, arg_level = Alexa_boolean.asab(arg_formula, arg_level)
            if 2 > len(arg_level):
                break
            else:pass
        return arg_formula[0]
    
    @staticmethod
    def get_vars(arg_formula, arg_level):
        vars_list = []
        length = len(arg_formula)
        pos = 0
        while pos < length:
            if 0 == arg_level[pos]:
                if arg_formula[pos] not in vars_list:
                    vars_list.append(arg_formula[pos])
                else:pass
            else:pass
            pos += 1
        return vars_list

    @staticmethod
    def nxt(bool_list, arg_length):
        arg_bool_list = bool_list
        pos = 0
        flag_next = True
        while (pos < arg_length) and flag_next:
            if True == arg_bool_list[pos]:
                arg_bool_list[pos] = False
                pos += 1
            else:
                arg_bool_list[pos] = True
                flag_next = False
        return (not(flag_next), arg_bool_list)
    
    @staticmethod
    def execute_formula(arg_formula, arg_var_dict):
        if isinstance(arg_formula, tuple):
            fun = arg_formula[0]
            if fun in Alexa_boolean.NOT_LIST:
                return not(Alexa_boolean.execute_formula(arg_formula[1], arg_var_dict))
            elif fun in Alexa_boolean.AND_LIST:
                return ((Alexa_boolean.execute_formula(arg_formula[1], arg_var_dict)) and (Alexa_boolean.execute_formula(arg_formula[2], arg_var_dict)))
            elif fun in Alexa_boolean.OR_LIST:
                return ((Alexa_boolean.execute_formula(arg_formula[1], arg_var_dict)) or (Alexa_boolean.execute_formula(arg_formula[2], arg_var_dict)))
            elif fun in Alexa_boolean.IMPLICATION_LIST:
                return (not(Alexa_boolean.execute_formula(arg_formula[1], arg_var_dict)) or (Alexa_boolean.execute_formula(arg_formula[2], arg_var_dict)))
            else:
                print("ERROR ! unknown function")
                return False
        else:
            return arg_var_dict[arg_formula]



        
if __name__ == '__main__':
    ch = '1'
    while '1' == ch :
        x_string = str(input("""Введіть вираз (наприклад, \"a -> (b -> (a and b)) or not(c)\" ) : \n"""))
        if r'"' == x_string[0]:
            x_string = x_string[1:-1]
        else:pass
    
        A = Alexa_boolean(x_string)
        if A.isTautology: 
            print("""Даний вираз є тавтологія""")
        else:
            print("""Даний вираз НЕ є тавтологія""")
        del A
        ch = str(input("""Для продовження тестування введіть 1, для закінчення будь-який інший символ : """))
            
