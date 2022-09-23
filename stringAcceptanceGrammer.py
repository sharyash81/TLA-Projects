from collections import defaultdict
import copy
import itertools
from re import L


class SingleProduction:
    def __init__(self, left, right):
        self.grammer = (left, right)
        self.terminals = list()
        self.fillterminals()

    def fillterminals(self):
        right = self.grammer[1]
        if right != '#':
            i = 0
            while i < (len(right)):
                if right[i] == "<":
                    i += 3
                    continue
                self.terminals.append(right[i])
                i += 1


class Grammer:
    def __init__(self):
        self.variables = list()
        self.productions = defaultdict(set)
        self.productions_without_null = defaultdict(set)
        self.productions_chomsky = defaultdict(set)
        self.termianls = set()
        self.START_VARIABLE = ''

    def add_production(self, production: SingleProduction):
        left = production.grammer[0]
        right = production.grammer[1]
        self.productions[left].add(right)
        self.termianls.update(set(production.terminals))

    def remove_nullable_variables(self):
        self.productions_without_null = copy.deepcopy(self.productions)
        nullable_variables = list()
        for key in self.productions.keys():
            for item in self.productions[key]:
                if item == "#":
                    self.productions_without_null[key].remove(item)
                    if len(self.productions_without_null[key]) == 0:
                        self.productions_without_null.pop(key)
                    nullable_variables.append(key)
        for key in self.productions.keys():
            for item in self.productions[key]:
                if nullable_variables.__contains__(item):
                    nullable_variables.append(key)
        self.productions = copy.deepcopy(self.productions_without_null)
        for variable in nullable_variables:
            if not self.productions.keys().__contains__(variable):
                self.__change_items(False, variable)
            else:
                self.__change_items(True, variable)
        self.__remove_self_loop(1)
        


    def __remove_self_loop(self , i : int ):
        if i == 0 :
            for key in self.productions_chomsky.keys():
                for item in self.productions_chomsky[key]:
                    if item == key :
                        self.productions_chomsky[key].remove(item)
        elif i == 1 : 
            for key in self.productions_without_null.keys():
                for item in self.productions_without_null[key]:
                    if item == key :
                        self.productions_without_null[key].remove(item)

        
    def __change_items(self, flag: bool, variable):
        if not flag:
            for key in self.productions:
                for item in self.productions[key]:
                    tmp = item.replace(variable, '')
                    self.productions_without_null[key].remove(item)
                    self.productions_without_null[key].add(tmp)
        else:
            new_dic = dict()
            for key in self.productions_without_null:
                new_set = list()
                for item in self.productions_without_null[key]:
                    original_list = self.__create_list(item)
                    indices = [i for i, x in enumerate(
                        original_list) if x == variable]
                    if len(indices) > 0:
                        remove_combination = self.__combinations(indices)
                        tmp_list = copy.deepcopy(original_list)
                        for items in remove_combination:
                            for index in sorted(items, reverse=True):
                                del original_list[index]
                            if len(list(original_list)) > 0 and ''.join(list(original_list)) != key:
                                new_set.append(''.join(list(original_list)))
                            original_list = copy.deepcopy(tmp_list)
                    else:
                        new_set.append(''.join(list(item)))
                new_dic[key] = set(new_set)
            self.productions_without_null = new_dic

    def __combinations(self, indices: list):
        subset = list()
        for i in range(0, len(indices)+1):
            subset.extend([set(comb)
                          for comb in itertools.combinations(indices, i)])
        return subset

    def __create_list(self, str: str):
        output = list()
        i = 0
        while i < len(str):
            if str[i] == '<':
                tmp = str[i]
                while str[i]!='>':
                    i+=1
                    tmp+=str[i]
                output.append(tmp)
            else:
                output.append(str[i])
            i += 1
        return output

    def remove_unit_productions(self):
        self.productions_chomsky = copy.deepcopy(self.productions_without_null)
        unit_product = self.__has_unit_product()
        while unit_product:
            self.productions_chomsky[unit_product[0]].remove(unit_product[1])
            if unit_product[0] != unit_product[1]:
                self.productions_chomsky[unit_product[0]].update(
                    self.productions_chomsky[unit_product[1]])
            unit_product = self.__has_unit_product()

    def __has_unit_product(self):
        for key in self.productions_chomsky:
            for item in self.productions_chomsky[key]:
                if variables.__contains__(item):
                    return (key, item)
        return False

    def convert_to_chomsky(self):
        if self.__is_not_chomsky():
            for terminal in self.termianls:
                new_key = "<T"+str(terminal)+">"
                if self.productions_chomsky.keys().__contains__(new_key):
                    self.productions_chomsky[new_key].add(terminal)
                else:
                    new_pair = {new_key: set()}
                    self.productions_chomsky.update(new_pair)
                    self.productions_chomsky[new_key].add(terminal)

            for key in self.variables:
                for item in self.productions_chomsky[key]:
                    if self.termianls.__contains__(item):
                        continue
                    self.productions_chomsky[key].remove(item)
                    i = 0
                    new_item = ""
                    while i < len(item):
                        if item[i] == '<':
                            while item[i] != '>':
                                new_item += item[i]
                                i += 1
                            new_item += '>'
                        else:
                            new_item += "<T"+item[i]+">"
                        i += 1
                    self.productions_chomsky[key].add(new_item)

        exception = self.__is_not_chomsky()
        counter = 0
        while exception:
            index = self.__end_var_pos(exception[1])
            new_value = exception[1][index:]
            new_key = "<V"+str(counter)+">"
            counter += 1
            if not self.productions_chomsky.keys().__contains__(new_key):
                new_pair = {new_key: set()}
                self.productions_chomsky.update(new_pair)
            self.productions_chomsky[new_key].add(new_value)
            self.productions_chomsky[exception[0]].remove(exception[1])
            self.productions_chomsky[exception[0]].add(
                exception[1][0:index]+new_key)
            exception = self.__is_not_chomsky()

    def __end_var_pos(self, item):
        i = 0 
        while item[i]!='>':
            i+=1
        i+=1
        return i

    def __is_not_chomsky(self):
        for key in self.productions_chomsky.keys():
            for item in self.productions_chomsky[key]:
                if not self.__has_just_two_var(item) and not self.termianls.__contains__(item):
                    return (key, item)
        return False

    def __has_just_two_var(self,item):
        tmp = self.__create_list(item)
        if len(tmp) == 2 and not any(item in tmp for item in self.termianls):
            return True
        return False

    def __count_variable(self, item):
        counter = 0
        for c in item:
            if c == '<':
                counter += 1
        return counter

    def __find_var(self, item: str):
        if self.__count_variable(item) == 0:
            return []
        vars = item.split('<')
        vars.pop(0)
        for i in range(len(vars)):
            vars[i] = '<'+vars[i]
        return vars

    def CYK(self, string: str):
        n = len(string)+1
        dp = [[set() for j in range(n)] for i in range(n)]
        for i in range(1, n):
            for key in self.productions_chomsky:
                for item in self.productions_chomsky[key]:
                    if item == string[i-1]:
                        dp[i][i].add(key)

        for l in range(2, n):
            for i in range(1, n-l+1):
                j = i+l-1
                for k in range(i, j):
                    for key in self.productions_chomsky:
                        for item in self.productions_chomsky[key]:
                            vars = self.__find_var(item)
                            if len(vars) == 0:
                                continue
                            if dp[i][k].__contains__(vars[0]) and dp[k+1][j].__contains__(vars[1]):
                                dp[i][j].add(key)
        if dp[1][n-1].__contains__(self.START_VARIABLE):
            return 'Accepted'
        return 'Rejected'


if __name__ == '__main__':
    global variables
    variables = list()
    variables_num = int(input())
    grammer = Grammer()
    for i in range(variables_num):
        complete_productions = input().split('->')
        left = "".join(complete_productions[0].split())
        variables.append(left)
        all_right = "".join(complete_productions[1].split()).split('|')
        if (i == 0) :
            grammer.START_VARIABLE = left
        for right in all_right:
            grammer.add_production(SingleProduction(left, right))

    grammer.variables = variables
    string = input()
    # print(grammer.productions)
    grammer.remove_nullable_variables()
    # print(grammer.productions_without_null)
    grammer.remove_unit_productions()
    # print(grammer.productions_chomsky)
    grammer.convert_to_chomsky()
    # print(grammer.productions_chomsky)
    print(grammer.CYK(string))
