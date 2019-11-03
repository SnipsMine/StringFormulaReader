
import re
import math


class StringFormulaReader(object):
    """This class will read a string with a formula and executes it"""

    def __init__(self, formula):
        # Create the class variable
        self.actions = {"*": self.multiply, "/": self.divide, "+": self.add, "-": self.subtract,
                        "^": self.power}
        self.variables = {}
        self.string_formula = formula
        self.formula = []
        self.answer = 0

        # Create the formula
        self.create_formula()

        # Link the brackets
        self.link_brackets()

        print(self.formula)

    def create_formula(self):

        # test area https://regex101.com/r/QYbGlh/1
        regex = re.compile(r"(log\d*)|([a-zA-Z]+)|(\d+)|([+\-*/^])|(.)")

        matches = re.finditer(regex, self.string_formula)

        for match in matches:

            if match.group(1) is not None:
                value = match.group(1)
                self.formula.append(value)

            # if the match is a variable
            elif match.group(2) is not None:
                value = match.group(2)
                self.formula.append(value)
                self.variables[value] = None

            # if the match is a number
            elif match.group(3) is not None:
                value = match.group(3)
                self.formula.append(float(value))

            # if the match is a action
            elif match.group(4) is not None:
                value = match.group(4)
                self.formula.append(self.actions[value])

            # if the match is anything else
            else:
                value = match.group(5)
                self.formula.append(value)

    def link_brackets(self):
        counter_curly_brackets = 0
        counter_brackets = 0

        for i, x in enumerate(self.formula):
            if x == "(":
                counter_brackets += 1
                self.formula.pop(i)
                self.formula.insert(i, "({}".format(counter_brackets))
            elif x == ")":
                self.formula.pop(i)
                self.formula.insert(i, "){}".format(counter_brackets))
                counter_brackets -= 1
            elif x == "{":
                counter_curly_brackets += 1
                self.formula.pop(i)
                self.formula.insert(i, "{%s" % counter_curly_brackets)
            elif x == "}":
                self.formula.pop(i)
                self.formula.insert(i, "}%s" % counter_curly_brackets)
                counter_curly_brackets -= 1

    def execute(self, formula=()):
        if formula == ():
            formula = self.formula

        calculation_rules = ["∑", r'\(\d+', r'log\d*', self.power, "√", self.multiply, self.divide,
                             self.add, self.subtract]

        if None not in self.variables.values():
            for method in calculation_rules:
                while re.search(str(method), str(formula)):
                    for index, action in enumerate(formula):
                        if re.search(str(method), str(action)):
                            if re.search(calculation_rules[1], str(action)):
                                self.brackets(formula, index)

                            elif action == '∑':
                                self.sum(formula, index)

                            elif action == "√":
                                self.square_root(index)
                                formula.pop(index+1)
                                formula.pop(index)

                                formula.insert(index, self.answer)

                            elif re.search(calculation_rules[2], str(action)):
                                self.logarithm(index)
                                formula.pop(index+1)
                                formula.pop(index)

                                formula.insert(index, self.answer)
                            else:
                                value1 = formula[index-1]
                                value2 = formula[index+1]

                                formula.pop(index+1)
                                formula.pop(index)
                                formula.pop(index-1)

                                if value1 in self.variables:
                                    value1 = self.variables[value1]
                                if value2 in self.variables:
                                    value2 = self.variables[value2]

                                action(value1, value2)
                                formula.insert(index-1, self.answer)
                            break

        else:
            print("there is a variable that has no value")

        if len(formula) == 1:
            self.answer = formula[0]

    def multiply(self, value1, value2):
        print("multiply")

        self.answer = value1 * value2
        print("{}*{}={}".format(value1, value2, self.answer))

    def divide(self, value1, value2):
        print("divide")

        self.answer = value1 / value2
        print("{}/{}={}".format(value1, value2, self.answer))

    def add(self, value1, value2):
        print("add")

        self.answer = value1 + value2
        print("{}+{}={}".format(value1, value2, self.answer))

    def subtract(self, value1, value2):
        print("subtract")

        self.answer = value1 - value2
        print(f"{value1}-{value2}={self.answer}")

    def power(self, value1, value2):
        print("power")

        self.answer = value1 ** value2
        print(f"{value1}^{value2}={self.answer}")

    def square_root(self, index):
        print("square_root")
        value1 = self.formula[index+1]
        self.answer = math.sqrt(value1)
        print(f"√{value1}={self.answer}")

    def logarithm(self, index):
        print("logarithm")
        value1 = self.formula[index+1]
        if value1 in self.variables:
            value1 = self.variables[value1]

        log_exponential = self.formula[index].lower().replace("log", "")
        if not log_exponential:
            log_exponential = 10
        self.answer = math.log(value1, float(log_exponential))

        print("log{}({})={}".format(log_exponential, value1, self.answer))

    def brackets(self, formula, index):
        print("Brackets begin")
        # Find bracket number
        print(formula[index])
        bracket_number = formula[index].replace("(", "")

        # find the start en end index of this bracket
        start = formula.index("({}".format(bracket_number))
        end = formula.index("){}".format(bracket_number))

        b_formula = formula[start+1:end].copy()

        self.execute(b_formula)

        print(formula[end])

        # remove the items inside the brackets from the formula
        for rm in range(start, end+1):
            formula.pop(start)

        # insert the answer in the formula
        formula.insert(start, self.answer)

        print("Brackets end")

    def sum(self, formula, index):
        print("sum")

        print("".join(formula[index:index+2]))
        bracket_number = int(formula[index+1].replace("{", ""))

        start = formula.index("{%s" % str(bracket_number))
        end = formula.index("}%s" % str(bracket_number))
        s_formula = formula[start+1:end]

        # variables in sum
        variables = [x for x in self.variables.keys() if x in s_formula]

        answers = []

        if "∑" in s_formula:
            start = formula.index("{%s" % str(bracket_number+1))
            end = formula.index("}%s" % str(bracket_number+1))
            s_formula = formula[start-1:end+1]
            self.execute(s_formula)

            answers.append(self.answer)
        else:
            for x in range(self.variables["n"]):
                s_formula = formula[start+1:end]
                for y in s_formula:
                    if y in variables:
                        i = s_formula.index(y)
                        s_formula.pop(i)
                        if isinstance(self.variables[y], (list, tuple)):
                            s_formula.insert(i, self.variables[y][x])
                        else:
                            s_formula.insert(i, self.variables[y])

                self.execute(s_formula)
                answers.append(self.answer)

            print("sum")
            print("{}={}".format("+".join([str(x) for x in answers]), sum(answers)))

            print(formula[end])

        for rm in range(start-1, end+1):
            formula.pop(start-1)

        formula.insert(start-1, sum(answers))


def main():
    formula1 = StringFormulaReader("x*3/5+20+2^(z*((5+3)*3))")
    formula1.variables["x"] = 5
    formula1.variables["z"] = 10
    formula1.execute()

    mean = StringFormulaReader("∑{x}/n")
    mean.variables["x"] = [4, 5, 3, 6, 2, 6, 3, 6]
    mean.variables["n"] = len(mean.variables["x"])
    mean.execute()

    standard_deviation = StringFormulaReader("√(∑{(w-∑{w}/n)^2}/n)")
    standard_deviation.variables["w"] = [4, 5, 3, 6, 2, 6, 3, 6]
    standard_deviation.variables["n"] = len(standard_deviation.variables["w"])
    standard_deviation.execute()

    logarithm = StringFormulaReader("log(x)")
    logarithm.variables["x"] = 100
    logarithm.execute()

    print("standard deviation =", round(standard_deviation.answer, 4))
    print("Mean =", round(mean.answer, 4))
    print("Formula 1 =", round(formula1.answer, 4))
    print("Logarithm = ", round(logarithm.answer, 4))


if __name__ == "__main__":
    exit(main())
