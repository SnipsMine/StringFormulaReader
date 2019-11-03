
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
        regex = re.compile(r"([a-zA-Z]+)|(\d+)|([+\-*/^])|(.)")

        matches = re.finditer(regex, self.string_formula)

        for match in matches:

            # if the match is a variable
            if match.group(1) is not None:
                value = match.group(1)
                self.formula.append(value)
                self.variables[value] = None

            # if the match is a number
            elif match.group(2) is not None:
                value = match.group(2)
                self.formula.append(float(value))

            # if the match is a action
            elif match.group(3) is not None:
                value = match.group(3)
                self.formula.append(self.actions[value])

            # if the match is anything else
            else:
                value = match.group(4)
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

        rekenregels = ["∑", r'\(\d+', self.power, "√", self.multiply, self.divide,
                       self.add, self.subtract]

        if None not in self.variables.values():
            for methode in rekenregels:
                while re.search(str(methode), str(formula)):
                    for index, action in enumerate(formula):
                        if isinstance(action, str) and action.startswith("("):
                            self.brackets(formula, index)

                        elif action == methode:
                            if action == '∑':
                                self.sum(formula, index)

                            elif action == "√":
                                self.square_root(index)
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
                            # print(formula)
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

    def brackets(self, formula, index):
        print("Brackets begin")
        # Find bracket number
        print(formula[index])
        bracket_number = formula[index].replace("(", "")

        # find the start en end index of this bracked
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
        print(self.formula)

        print("Brackets end")

    def sum(self, formula, index):
        print("sum")

        print("".join(formula[index:index+2]))
        bracket_number = int(formula[index+1].replace("{", ""))

        start = formula.index("{%s" % str(bracket_number))
        end = formula.index("}%s" % str(bracket_number))
        s_formula = formula[start+1:end]

        # variables in sum
        print(s_formula)
        variables = [x for x in self.variables.keys() if x in s_formula]

        while "∑" in s_formula:
            start2 = formula.index("{%s" % str(bracket_number+1))
            end2 = formula.index("}%s" % str(bracket_number+1))
            s2_formula = formula[start2-1:end2+1]
            self.execute(s2_formula)

            for rm in range(start2-1, end2+1):
                formula.pop(start2-1)

            formula.insert(start2-1, self.answer)
            return

        anwsers = []
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
            anwsers.append(self.answer)
        print("{}={}".format("+".join([str(x) for x in anwsers]), sum(anwsers)))

        print(formula[end])
        for rm in range(start-1, end+1):
            formula.pop(start-1)

        formula.insert(start-1, sum(anwsers))


def main():
    x = StringFormulaReader("x*3/5+20+2^(z*((5+3)*3))")
    x.variables["x"] = 5
    x.variables["z"] = 10
    #x.execute()
    print(x.answer)

    y = StringFormulaReader("∑{x}/n")
    y.variables["x"] = [3, 5, 7, 4, 6]
    y.variables["n"] = len(y.variables["x"])
    #y.execute()
    print(y.answer)

    z = StringFormulaReader("√(∑{(w-(∑{x}/n))*(w-(∑{x}/n))}/n)")
    z.variables["w"] = [4, 5, 3, 6, 2, 6, 3, 6]
    z.variables["x"] = z.variables["w"]
    z.variables["n"] = len(z.variables["w"])
    z.execute()
    print(z.answer)


if __name__ == "__main__":
    exit(main())
