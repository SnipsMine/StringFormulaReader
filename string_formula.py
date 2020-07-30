"""ScheikundigeFormules


Author: Micha Snippe
Date: 19-02-2020
Since: 14-11-2020
Version: 1.0.1
"""

import re
import math


class StringFormulaReader:
    """This class will read a string with a formula and executes it"""

    def __init__(self, formula):
        """
        This function initiates the class and sets default values for the global variables
        - Parameter formula: A formula in string format
        """
        # Create the class variable
        # Actions that can be executed. Excl. functions
        self.actions = {"*": self.multiply, "/": self.divide, "+": self.add, "-": self.subtract,
                        "^": self.power}
        
        # The varaibles in the formula
        self.variables = {}

        # The string variant of formula
        self.string_formula = formula

        # The executable formula
        self.formula = []

        # The answer after execution
        self.answer = 0

        # Create the formula
        self.create_formula()

        print(self.formula)

    def create_formula(self):
        """
        This function creates a executable formula from the string_formula
        - Requires: self.string_formula to be set
        """
        # test area https://regex101.com/r/QYbGlh/2
        regex = re.compile(r"([lL][oO][gG]\d*)|([iI][fF])|([a-zA-Z]+\d*)|(\d+)|([+\-*/^])|(.)")

        matches = re.finditer(regex, self.string_formula)

        for match in matches:

            if match.group(1) is not None:
                value = match.group(1)
                self.formula.append(value)

            elif match.group(2) is not None:
                value = match.group(2)
                self.formula.append(value)

            # if the match is a variable
            elif match.group(3) is not None:
                value = match.group(3)
                self.formula.append(value)
                self.variables[value] = None

            # if the match is a number
            elif match.group(4) is not None:
                value = match.group(4)
                self.formula.append(float(value))

            # if the match is a action
            elif match.group(5) is not None:
                value = match.group(5)
                self.formula.append(self.actions[value])

            # if the match is anything else
            else:
                value = match.group(6)
                self.formula.append(value)

        # Link the brackets
        self.link_brackets()

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
        """
        This function executes the formula recursivly if nessasery
        """
        # if no formula given use the self formula
        if formula == ():
            formula = self.formula

        # set de reken volgorde. Ca: eerst functies('{') daarna haakjes('(') enz.
        calculation_rules = [r"\{\d+", r'\(\d+', r'log\d*', self.power, "√", self.multiply,
                             self.divide, self.add, self.subtract]

        # If all variables are filled in
        if None not in self.variables.values():
            
            # loop thru all the calculation rules
            for method in calculation_rules:
                
                # Do this while the current method is in the formula
                while re.search(str(method), str(formula)):
                    
                    # loop thru the formula
                    for index, action in enumerate(formula):
                        
                        # if the action in the formula is equal to the current method 
                        if re.search(str(method), str(action)):

                            # if the action in the formula is a haakje
                            if re.search(calculation_rules[1], str(action)):
                                self.brackets(formula, index)

                            # if the cation in the formula is a function
                            elif re.search(calculation_rules[0], str(action)):
                                # is the function a sum
                                if formula[index-1] == "∑":
                                    self.sum(formula, index)

                                # is the funtion an if statenment
                                elif formula[index-1] == "if":
                                    self.conditional(formula, index)

                            # is the action a wortel
                            elif action == "√":
                                self.square_root(index)
                                formula.pop(index+1)
                                formula.pop(index)

                                formula.insert(index, self.answer)

                            # is the current action a logaritme
                            elif re.search(calculation_rules[2], str(action)):
                                self.logarithm(index)
                                formula.pop(index+1)
                                formula.pop(index)

                                formula.insert(index, self.answer)
                            # anders zit de action in de self.actions lijst
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

                                # Action is a function that is in the formula list based on the self.actions list
                                action(value1, value2)
                                formula.insert(index-1, self.answer)
                            break

        else:
            for var in self.variables:
                if self.variables[var] is None:
                    print(f"The variable {var} has no value")

        # Set the anwser if formula only has 1 item left
        if len(formula) == 1:
            if formula[0] in self.variables:
                formula[0] = self.variables[formula[0]]
            self.answer = formula[0]

    def multiply(self, value1, value2):
        """
        Multiplyes two numbers together
        Paramaters:
        - value1: een float/int
        - value2: een float/int
        """
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
        """
        Subtracts two numbers together
        Paramaters:
        - value1: een float/int
        - value2: een float/int
        """
        print("subtract")

        self.answer = value1 - value2
        print(f"{value1}-{value2}={self.answer}")

    def power(self, value1, value2):
        """
        Takes value 1 to the power of value 2
        Paramaters:
        - value1: een float/int
        - value2: een float/int
        """
        print("power")

        self.answer = value1 ** value2
        print(f"{value1}^{value2}={self.answer}")

    def square_root(self, index):
        """
        Returns the root of the number after the root sign
        Paramaters:
        - index: the location in self.formula that has the root sign
        """
        print("square_root")
        value1 = self.formula[index+1]
        self.answer = math.sqrt(value1)
        print(f"√{value1}={self.answer}")

    def logarithm(self, index):
        """
        Takes the log of the number after the log. If the log has an number behind it bv: log12
        the 12th log wil be used instead of the 10th log
        Paramaters:
        - index: the location in self.formula that has the log 
        """
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
        """
        Executes the formula within the brackets
        Paramaters:
        - formula: The currently executed formula.
        - index: the location of the opening bracket in the formula
        """
        print("Brackets begin")
        # Find bracket number
        print(formula[index])
        bracket_number = formula[index].replace("(", "")

        # find the start en end index of this bracket
        start = formula.index("({}".format(bracket_number))
        end = formula.index("){}".format(bracket_number))

        # Create a secundary formula using the start and end positions
        b_formula = formula[start+1:end].copy()

        # Execute this new formula. Recursion!!!
        self.execute(b_formula)

        print(formula[end])

        # remove the items inside the brackets from the formula
        for rm in range(start, end+1):
            formula.pop(start)

        # insert the answer in the formula
        formula.insert(start, self.answer)

        print("Brackets end")

    def sum(self, formula, index):
        """
        Calculates the formula n number of times and adding up all the anwsers.
        With n the amount of variables given.
        Parameters:
        - formula: The current formula
        - index: the location of the sum in the formula
        """
        print("sum")

        print("".join(formula[index]))
        # Get current bracked number
        bracket_number = int(formula[index].replace("{", ""))

        start = formula.index("{%s" % str(bracket_number))
        end = formula.index("}%s" % str(bracket_number))

        # Create a secundary formula from the new start and end points 
        s_formula = formula[start+1:end]

        # variables in sum
        variables = [x for x in self.variables.keys() if x in s_formula]

        answers = []

        # Check if there is another fuction in the new formula
        if re.search(r"{\d+", str(s_formula)):
            # Get new start and end. And create a new tetrary formula
            start = formula.index("{%s" % str(bracket_number+1))
            end = formula.index("}%s" % str(bracket_number+1))
            s_formula = formula[start-1:end+1]

            # Execute the tetrary formula
            self.execute(s_formula)

            answers.append(self.answer)
        else:
            # loop thru the secondary formula n times
            for x in range(self.variables["n"]):
                s_formula = formula[start+1:end]

                # Change the variable afkorting to the n'th value 
                for y in s_formula:
                    if y in variables:
                        i = s_formula.index(y)
                        s_formula.pop(i)
                        if isinstance(self.variables[y], (list, tuple)):
                            s_formula.insert(i, self.variables[y][x])
                        else:
                            s_formula.insert(i, self.variables[y])

                # Execute the secudary formula
                self.execute(s_formula)
                answers.append(self.answer)

            print("sum")
            print("{}={}".format("+".join([str(x) for x in answers]), sum(answers)))

            print(formula[end])

        # Remove all the items within the start and end values
        for rm in range(start-1, end+1):
            formula.pop(start-1)

        # Insert the anwser of the sum in the formula
        formula.insert(start-1, sum(answers))

    def conditional(self, formula, index):
        """
        Performs a if statement and retruns different anwsers based on the check
        formula: the current formula
        index: the location of the if statement in the formula
        """
        print("conditional")

        # The logic operation posible
        logic = {"<": self.smaller, "<=": self.smaller_or_equal, "=": self.equal,
                 ">=": self.larger_or_equal, ">": self.larger, "!=": self.not_equal}

        # Get current bracket number and create the secondary formula
        bracket_number = int(formula[index].replace("{", ""))
        start = formula.index("{%s" % str(bracket_number))
        end = formula.index("}%s" % str(bracket_number))
        c_formula = formula[start+1:end]

        # Splits the if statement on the three parts( the condition part 1, the logical,
        #                                             the condition part 2, if true, if false)
        b_number = bracket_number
        counter = 0
        form = [[], [], [], []]
        logical = ""
        for x in c_formula:
            if isinstance(x, str) and x.startswith("{"):
                b_number += 1
            elif isinstance(x, str) and x.startswith("}"):
                b_number -= 1
            if b_number == bracket_number:
                if x == ";":

                    counter += 1
                    continue

                if x in logic.keys():
                    counter += 1
                    logical = x
                    continue

            form[counter].append(x)

        # Executet part 1 and part 2 of the condition to for the check
        for f in form[0:2]:
            self.execute(f)

        value1 = form[0][0]
        value2 = form[1][0]

        # Check if the condition if true or false
        logic[logical](value1, value2)

        print("The statement was", self.answer)

        # Execute the correct part based on the conditions outcome
        if self.answer:
            self.execute(form[2])
        else:
            self.execute(form[3])

        # Remove the if function from the formula
        for rm in range(start-1, end+1):
            formula.pop(start-1)

        # Insert the anwser
        formula.insert(start-1, self.answer)

    def smaller(self, value1, value2):
        """
        Checks if the value 1 is smaler than value 2
        """
        self.answer = value1 < value2

    def smaller_or_equal(self, value1, value2):
        """
        Checks if the value 1 is smaler or equal than value 2
        """
        self.answer = value1 <= value2

    def equal(self, value1, value2):
        """
        Checks if the value 1 is equal to value 2
        """
        self.answer = value1 == value2

    def larger_or_equal(self, value1, value2):
        """
        Checks if the value 1 is grater or equal to value 2
        """
        self.answer = value1 >= value2

    def larger(self, value1, value2):
        """
        Checks if the value 1 is grater than value 2
        """
        self.answer = value1 > value2

    def not_equal(self, value1, value2):
        """
        Checks if the value 1 is not equal to value 2
        """
        self.answer = value1 != value2


def main():
    formula1 = StringFormulaReader("E/ε*l")
    formula1.variables["E"] = 10
    formula1.variables["ε"] = 5
    formula1.variables["l"] = 2
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

    conditional = StringFormulaReader("if{x<if{x>y*2;x;y};x;y}")
    conditional.variables["x"] = 10
    conditional.variables["y"] = 11
    conditional.execute()

    theoretical_mass = StringFormulaReader(
                                            "if{d1>0;"
                                                "if{d2>0;"
                                                    "if{m1*d1/M1>m2*d2/M2;"
                                                        "(m2*d2/M2)*(fs/fg)*Mg;"
                                                        "(m1*d1/M1)*(fs/fg)*Mg"
                                                    "};"
                                                    "if{m1*d1/M1>m2/M2;"
                                                        "(m2/M2)*(fs/fg)*Mg;"
                                                        "(m1*d1/M1)*(fs/fg)*Mg"
                                                    "}"
                                                "};"
                                                "if{d2>0;"
                                                    "if{m1/M1>m2*d2/M2;"
                                                        "(m2*d2/M2)*(fs/fg)*Mg;"
                                                        "m1/M1*(fs/fg)*Mg"
                                                    "};"
                                                    "if{m1/M1>m2/M2;"
                                                        "(m2/M2)*(fs/fg)*Mg;"
                                                        "(m1/M1)*(fs/fg)*Mg"
                                                    "}"
                                                "}"
                                            "}"
                                           )
    theoretical_mass.variables["m1"] = 100  # mass 1
    theoretical_mass.variables["M1"] = 20  # molarity 1
    theoretical_mass.variables["d1"] = 0  # density 1

    theoretical_mass.variables["m2"] = 19  # mass 2
    theoretical_mass.variables["M2"] = 40  # molarity 2
    theoretical_mass.variables["d2"] = 1.09  # density 2

    theoretical_mass.variables["fs"] = 1  # reactie verhouding stof
    theoretical_mass.variables["fg"] = 1  # reactie verhouding gewild

    theoretical_mass.variables["Mg"] = 50  # molarity of the product

    theoretical_mass.execute()

    print("standard deviation =", round(standard_deviation.answer, 4))
    print("Mean =", round(mean.answer, 4))
    print("Formula 1 =", round(formula1.answer, 4))
    print("Logarithm = ", round(logarithm.answer, 4))
    print("Conditional = ", conditional.answer)
    print("Theoretical mass =", round(theoretical_mass.answer, 4))


if __name__ == "__main__":
    exit(main())
