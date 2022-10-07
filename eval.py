from dataclasses import replace
import math
from pickle import FALSE


def unary_operation(operator, operand):
    operand = float(operand)
    try:
        if operator == 'sin':
            return math.sin(operand)
        if operator == 'cos':
            return math.cos(operand)
        if operator == 'tan':
            return math.tan(operand)
        if operator == 'abs':
            return math.abs(operand)
        if operator == 'ln':
            return math.log(operand)
        if operator == 'exp':
            return math.exp(operand)
        if operator == 'sqrt':
            return math.sqrt(operand)
    except Exception as ex:
        return False


def calAdvExp(expressionstr: str):
    unary_operator = ['sin', 'abs', 'tan', 'cos', 'ln', 'exp', 'sqrt']
    expressionstr = expressionstr.split(' ')
    index = 0
    while len(expressionstr) != 1:
        index = 0
        isSimple = True
        while index < len(expressionstr):
            if index == 0:
                isSimple = True
            if expressionstr[index] == ')':
                isSimple = False
                first_p_index = index
                valid = False
                while first_p_index != -1:
                    if expressionstr[first_p_index] == '(':
                        valid = True
                        break
                    first_p_index -= 1
                if not valid:
                    return False
                inner_value = calSimpleExp(
                    " ".join(expressionstr[first_p_index+1:index]))
                if not inner_value:
                    return False
                prev = expressionstr[0:first_p_index]
                if index+1 < len(expressionstr):
                    next = expressionstr[index+1:]
                else:
                    next = list()
                expressionstr = list()
                if len(prev) > 0:
                    expressionstr.extend(prev)
                expressionstr.append(str(inner_value))
                if len(next) > 0:
                    expressionstr.extend(next)
                if len(prev) > 0:
                    if unary_operator.__contains__(prev[-1]):
                        new_index = len(prev)
                        res = unary_operation(
                            expressionstr[new_index - 1], expressionstr[new_index])
                        if str(res) == 'False':
                            return False
                        expressionstr[new_index-1:new_index+1] = [str(res)]
                index = 0
            else:
                index += 1
        if isSimple:
            if openPcontain(expressionstr):
                return False
            return calSimpleExp(" ".join(expressionstr))
    return expressionstr[0]


def openPcontain(expression):
    for char in expression:
        if char == '(':
            return True
    return False


def calSimpleExp(expressionstr: str):
    global expression
    expression = expressionstr.split(' ')
    if not power():
        return False
    if not division():
        return False
    if not multiplication():
        return False
    if not minus():
        return False
    if not add():
        return False
    if len(expression) == 1:
        return expression[0]
    else:
        return False


def add():
    global expression
    index = 0
    while index != len(expression):
        if expression[index] == '+':
            if index - 1 >= 0 and index + 1 < len(expression):
                prev = expression[0:index-1]
                if index + 2 < len(expression):
                    next = expression[index+2:]
                else:
                    next = list()
                new_val = 0
                try:
                    new_val = float(expression[index-1]) + \
                        float(expression[index+1])
                except Exception as ex:
                    return False
                expression = list()
                if len(prev) > 0:
                    expression.extend(prev)
                expression.append(str(new_val))
                if len(next) > 0:
                    expression.extend(next)
                index = 0
            else:
                return False
        else:
            index += 1
    return expression


def minus():
    global expression
    index = 0
    while index != len(expression):
        if expression[index] == '-':
            if index - 1 >= 0 and index + 1 < len(expression):
                prev = expression[0:index-1]
                if index + 2 < len(expression):
                    next = expression[index+2:]
                else:
                    next = list()
                new_val = 0
                try:
                    new_val = float(expression[index-1]) - \
                        float(expression[index+1])
                except Exception as ex:
                    return False
                expression = list()
                if len(prev) > 0:
                    expression.extend(prev)
                expression.append(str(new_val))
                if len(next) > 0:
                    expression.extend(next)
                index = 0
            else:
                return False
        else:
            index += 1
    return expression


def multiplication():
    global expression
    index = 0
    while index != len(expression):
        if expression[index] == '*':
            if index - 1 >= 0 and index + 1 < len(expression):
                prev = expression[0:index-1]
                if index + 2 < len(expression):
                    next = expression[index+2:]
                else:
                    next = list()
                new_val = 0
                try:
                    new_val = float(expression[index-1]) * \
                        float(expression[index+1])
                except Exception as ex:
                    return False
                expression = list()
                if len(prev) > 0:
                    expression.extend(prev)
                expression.append(str(new_val))
                if len(next) > 0:
                    expression.extend(next)
                index = 0
            else:
                return False
        else:
            index += 1
    return expression


def division():
    global expression
    index = 0
    while index != len(expression):
        if expression[index] == '/':
            if index - 1 >= 0 and index + 1 < len(expression):
                prev = expression[0:index-1]
                if index + 2 < len(expression):
                    next = expression[index+2:]
                else:
                    next = list()
                new_val = 0
                try:
                    new_val = float(expression[index-1]) / \
                        float(expression[index+1])
                except Exception as ex:
                    return False
                expression = list()
                if len(prev) > 0:
                    expression.extend(prev)
                expression.append(str(new_val))
                if len(next) > 0:
                    expression.extend(next)
                index = 0
            else:
                return False
        else:
            index += 1
    return expression


def power():
    global expression
    index = 0
    while index != len(expression):
        if expression[index] == '^':
            if index - 1 >= 0 and index + 1 < len(expression):
                prev = expression[0:index-1]
                if index + 2 < len(expression):
                    next = expression[index+2:]
                else:
                    next = list()
                new_val = 0
                try:
                    new_val = float(expression[index-1]
                                    ) ** float(expression[index+1])
                except Exception as ex:
                    return False
                expression = list()
                if len(prev) > 0:
                    expression.extend(prev)
                expression.append(str(new_val))
                if len(next) > 0:
                    expression.extend(next)
                index = 0
            else:
                return False
        else:
            index += 1
    return expression


if __name__ == '__main__':
    expression = input()
    expression = expression.replace('(', '( ')
    expression = expression.replace(')', ' )')
    expression = expression.replace('sin', 'sin ')
    expression = expression.replace('cos', 'cos ')
    expression = expression.replace('tan', 'tan ')
    expression = expression.replace('ln', 'ln ')
    expression = expression.replace('sqrt', 'sqrt ')
    expression = expression.replace('exp', 'exp ')
    expression = expression.replace('abs', 'abs ')
    answer = calAdvExp(expression)
    if str(answer) == 'False':
        print('INVALID')
    else:
        print("%.2f" % float(answer))
