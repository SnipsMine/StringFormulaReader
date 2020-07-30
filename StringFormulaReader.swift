//  StringFormulaReader.swift
//  ScheikundigeFormules


/// Author: Micha Snippe
/// Date: 19-02-2020
/// Since: 14-11-2020
/// Version: 1.0.1
/// Copyright: Copyright © 2019 EMSDevelopment. All rights reserved.

import UIKit

/**
 This class takes a formula in string format and makes it possible to execute
*/
class StringFormulaReader{
    
    /// Actions that can be executed. Excl. functions
    let actions = ["*": multiply, "/": divide, "+": add, "-": subtract,
                   "^": power]
    
    /// The varaibles in the formula
    var variables: [String: AnyObject?]
    
    /// The executable formula
    var formula: [String]
    
    /// The string variant of formula
    var string_formula: String
    
    /// The answer after execution
    var answer: Double
    
    /// The answer for an if statement
    var answerBool: Bool
    
    /**
     This function initiates the class and sets default values for the global variables
     - Parameter formula: A formula in string format
    */
    init(formula: String){
        // Create the class variable
        self.answer = 0
        self.answerBool = false
        self.string_formula = formula
        self.formula = []
        self.variables = [:]
    }
    
    /**
     This function creates a executable formula from the string_formula
     - Requires: self.string_formula to be set
    */
    func create_formula(){
        // test area https://regex101.com/r/QYbGlh/2
        let regex = try! NSRegularExpression(pattern: #"([lL][oO][gG]\d*)|([iI][fF])|([\(\)\{\}+\-*\/^])(-?\d+)|([^0-9+\-*\/^\(\){}√∑=;\n<>=!]+\d*)|(.)"#)
        let range = NSRange(location: 0, length: self.string_formula.utf16.count)
        let matches = regex.matches(in: self.string_formula, range: range)
        //print(matches)
        
        for match in matches{
            for group in 1 ..< match.numberOfRanges{
                if (match.range(at: group).length != 0){
                    let lower_index = match.range(at: group).location
                    let higher_index = lower_index + match.range(at: group).length

                    let upper = self.string_formula.index(self.string_formula.startIndex, offsetBy: higher_index)
                    let lower = self.string_formula.index(self.string_formula.startIndex, offsetBy: lower_index)
                
                    let value = String(self.string_formula[lower..<upper])
                    self.formula.append(value)
                    
                    if group == 5{
                        self.variables[value] = 0 as AnyObject
                    }
                }
            }
        }
        // Link the brackets
        self.link_brackets()
    }
    
    func recreate_string_formula()->String{
        
        let formula = unlink_brackets(formula: self.formula)
        return formula.joined(separator: "")
    }
    
    /**
     This function will return a list of indexes of variables that are in a sum
     - Retruns: A list of integers that point to a variable in  self.variable
    */
    func var_in_sum()->[String]{
        var variableList: [String] = []
        
        var depth = 0
        var start_depth = 0
        for (index, item) in formula.enumerated(){
            var in_sum = false
            
            if item == "∑"{
                start_depth = Int(formula[index+1].replacingOccurrences(of: "{", with: "", options: .literal, range: nil))!

            }
            if item == String(format:"{%i", depth+1){
                depth += 1
            }else if item == String(format:"}%i", depth){
                depth -= 1
            }
            
            if depth >= start_depth && start_depth != 0{
                in_sum = true
            }else{
                in_sum = false
            }
            
            if self.variables.keys.contains(item) && in_sum{
                variableList.append(item)
            }
        }
        return variableList
    }
    
    func link_brackets(){
        var counter_curly_brackets = 0
        var counter_brackets = 0

        for (i, x) in self.formula.enumerated(){
            
            if (x == "("){
                counter_brackets += 1
                self.formula.remove(at: i)
                self.formula.insert(String(format: "(%i", counter_brackets), at:i)
            }
            else if x == ")"{
                self.formula.remove(at: i)
                self.formula.insert(String(format: ")%i", counter_brackets), at:i)
                counter_brackets -= 1
            }
            else if x == "{"{
                counter_curly_brackets += 1
                self.formula.remove(at: i)
                self.formula.insert(String(format: "{%i", counter_curly_brackets), at:i)
            }
            else if x == "}"{
                self.formula.remove(at: i)
                self.formula.insert(String(format: "}%i", counter_curly_brackets), at:i)
                counter_curly_brackets -= 1
            }
            
        }
        
    }
    
    func unlink_brackets(formula: [String])->[String]{
        var formula = formula
        var counter_curly_brackets = 1
        var counter_brackets = 1

        for (i, x) in formula.enumerated(){
            
            if (x == String(format: "(%i", counter_brackets)){
                counter_brackets += 1
                formula.remove(at: i)
                formula.insert("(", at:i)
            }
            else if x == String(format: ")%i", counter_brackets){
                formula.remove(at: i)
                formula.insert(")", at:i)
                counter_brackets -= 1
            }
            else if x == String(format: "{%i", counter_curly_brackets){
                counter_curly_brackets += 1
                formula.remove(at: i)
                formula.insert("{", at:i)
            }
            else if x == String(format: "}%i", counter_curly_brackets){
                formula.remove(at: i)
                formula.insert("}", at:i)
                counter_curly_brackets -= 1
            }
        }
        return formula
    }
    
    func execute(formula: [String] = []){
        var formula = formula
        if formula.isEmpty{
            formula = self.formula
        }
        let calculation_rules: [[String]] = [[#"(\{\d+)"#], [#"(\(\d+)"#], [#"(log\d*)"#] ,[#"(\^)"#, #"(\√)"#], [#"(\*)"#, #"(\/)"#], [#"(\+)"#, #"(\-)"#]]

        if !(self.variables.values.contains(where: {$0 == nil})) {
            for method in calculation_rules{
                
                var match = 0
                var range_formula =  NSRange(location: 0, length: formula.joined().utf16.count)

                for math in method{
                    let method_regex = try! NSRegularExpression(pattern: math)
                    match += method_regex.matches(in: formula.joined(), range: range_formula).count
                }
                
                while match > 0 && formula.count > 1{
                    
                    for (index, action) in formula.enumerated(){
                        
                        var matches:[NSTextCheckingResult] = []
                        for math in method{
                            let method_regex = try! NSRegularExpression(pattern: math)
                            let range_action = NSRange(location: 0, length: action.utf16.count)
                            matches.append(contentsOf: method_regex.matches(in: action, range: range_action))
                        }
                        
                        if matches.count > 0{
                            let match = matches[0].range(at: 1)
                            if match.length == action.length{
                                if method == calculation_rules[1]{
                                    formula = self.brackets(index:index, formula: formula)
                                    
                                }else if method == calculation_rules[0]{
                                    if formula[index-1] == "∑"{
                                        formula = self.sum(index: index, formula: formula)
                                    }
                                    else if formula[index-1] == "if"{
                                        formula = self.conditional(index: index, formula: formula)
                                    }
                                    
                                }else if action == "√"{
                                    formula = self.square_root(index: index, formula: formula)
                                    
                                }else if method == calculation_rules[2]{
                                    formula = self.logarithm(index: index, formula: formula)
                                }else{
                                    formula = self.actions[action]!(self)(index, formula)
                                    //formula.insert(index-1, self.answer)
                                }
                                range_formula =  NSRange(location: 0, length: formula.joined().utf16.count)
                                break
                            }
                        }
                    }
                    match -= 1
                
                }
            }
            
            if formula.count == 1{
                if self.variables.keys.contains(formula[0]){
                    formula[0] = String(self.variables[formula[0]] as! Double)
                }
                self.answer = Double(formula[0])!
            }
        }
        else{
            for v in self.variables{
                if v.value == nil{
                    print(String(format: "The variable %@ has no value", v.key))
                }
            }
        }
    }
    
    func remove_from_formula(start: Int, end: Int, formula: [String]) -> [String]{
        var formula = formula
        for _ in start ... end{
            formula.remove(at: start)
        }
        formula.insert(String(self.answer), at: start)
        
        return formula
    }
    
    func get_variable_value(key: String) -> Double{
        var value: Double
        if self.variables.keys.contains(key){
            value = self.variables[key] as! Double
        }else{
            value = Double(key)!
        }
        return value
    }
    
    func multiply(index: Int, formula: [String]) -> [String]{
        print("multiply")
        let value1 = self.get_variable_value(key: formula[index-1])
        let value2 = self.get_variable_value(key: formula[index+1])
        
        self.answer = value1 * value2
        
        let formula = self.remove_from_formula(start: index-1, end: index+1, formula: formula)
        
        return formula
    }
    
    func divide(index: Int, formula: [String]) -> [String]{
        print("divide")
        let value1 = self.get_variable_value(key: formula[index-1])
        let value2 = self.get_variable_value(key: formula[index+1])
        
        self.answer = value1 / value2
        
        let formula = self.remove_from_formula(start: index-1, end: index+1, formula: formula)
        
        return formula
    }
    
    func add(index: Int, formula: [String]) -> [String]{
        print("add")
        let value1 = self.get_variable_value(key: formula[index-1])
        let value2 = self.get_variable_value(key: formula[index+1])
        
        self.answer = value1 + value2
        
        let formula = self.remove_from_formula(start: index-1, end: index+1, formula: formula)
        
        return formula
    }
    
    func subtract(index: Int, formula: [String]) -> [String]{
        print("subtract")
        let value1 = self.get_variable_value(key: formula[index-1])
        let value2 = self.get_variable_value(key: formula[index+1])
        
        self.answer = value1 - value2
        
        let formula = self.remove_from_formula(start: index-1, end: index+1, formula: formula)
        
        return formula
    }
    
    func power(index: Int, formula: [String]) -> [String]{
        print("power")
        let value1 = self.get_variable_value(key: formula[index-1])
        let value2 = self.get_variable_value(key: formula[index+1])
        
        self.answer = pow(value1, value2)
        
        let formula = self.remove_from_formula(start: index-1, end: index+1, formula: formula)
        
        return formula
    }
    
    func square_root(index: Int, formula: [String]) -> [String]{
        print("square_root")
        let value1 = self.get_variable_value(key: formula[index+1])
        
        self.answer = sqrt(value1)
        
        let formula = self.remove_from_formula(start: index, end: index+1, formula: formula)
        
        return formula
    }

    func logarithm(index: Int, formula: [String]) -> [String]{
        print("Logarithm")
        let value1 = self.get_variable_value(key: formula[index+1])
        let base_string = formula[index].replacingOccurrences(of: "log", with: "", options: .literal, range: nil)
        
        var base: Double
        if base_string == ""{
            base = 10
        }
        else{
            base = Double(base_string)!
        }
        
        self.answer = log(value1) / log(base)
        
        let formula = self.remove_from_formula(start: index, end: index+1, formula: formula)
        
        return formula
    }
    
    func brackets(index: Int, formula: [String]) -> [String]{
        print("Brackets begin")
        // Find bracket number
        print(formula[index])
        let bracket_number = formula[index].replacingOccurrences(of: "(", with: "", options: .literal, range: nil)

        // find the start en end index of this bracket
        let start = formula.firstIndex(of: String(format:"(%@", bracket_number))
        let end = formula.firstIndex(of: String(format:")%@", bracket_number))

        let b_formula: [String] = Array(formula[start!+1..<end!])

        self.execute(formula: b_formula)

        print(formula[end!])

        // remove the items inside the brackets from the formula and add answer
        let formula = self.remove_from_formula(start: start!, end: end!, formula: formula)
        
        print("Brackets end")
        
        return formula
    }

    func sum( index: Int, formula: [String]) -> [String]{
        print("sum")
        print(formula[index])

        let bracket_number = Int(formula[index].replacingOccurrences(of: "{", with: "", options: .literal, range: nil))!
        
        
        var start = formula.firstIndex(of: String(format:"{%i", bracket_number))
        var end = formula.firstIndex(of: String(format:"}%i", bracket_number))
        
        var s_formula: [String] = Array(formula[start!+1..<end!])

        // variables in sum
        var variables: [String] = []
        
        for x in self.variables.keys{
            if s_formula.contains(x){
                variables.append(x)
            }
        }

        var answers: [Double] = []
        
        let function = try! NSRegularExpression(pattern: #"\{\d+"#)
        let range = NSRange(location: 0, length: s_formula.joined().utf16.count)
        
        // Look if there is another function in the sum formula
        if function.matches(in: s_formula.joined(), range: range).count > 0{
            start = formula.firstIndex(of: String(format:"{%i", bracket_number+1))
            end = formula.firstIndex(of: String(format:"}%i", bracket_number+1))
            s_formula = Array(formula[start!-1...end!])
            self.execute(formula: s_formula)

            answers.append(self.answer)
        }else{
            for x in 0..<(self.variables["n"] as! Int){
                s_formula = Array(formula[start!+1..<end!])
                for y in s_formula{
                    if variables.contains(y){
                        let i = s_formula.firstIndex(of: y)!
                        s_formula.remove(at: i)
                        let is_list = self.variables[y] as? [Double]
                        if is_list != nil{
                            s_formula.insert(String((self.variables[y] as! [Double])[x]), at: i)
                        }
                        else{
                            s_formula.insert(String((self.variables[y] as! Double)), at: i)
                        }
                    }
                }

                self.execute(formula: s_formula)
                answers.append(self.answer)
            }
            
            //print("{}={}".format("+".join([str(x) for x in answers]), sum(answers)))

            print(formula[end!])
        }
        self.answer = answers.reduce(0, +)
        let formula = self.remove_from_formula(start: start!-1, end: end!, formula: formula)

        return formula
    }

    func conditional(index: Int, formula: [String]) -> [String]{
        print("conditional")
        print(formula[index])

        let logic = ["<": self.smaller, "<=": self.smaller_or_equal, "=": self.equal,
                     ">=": self.larger_or_equal, ">": self.larger, "!=": self.not_equal]

        let bracket_number = Int(formula[index].replacingOccurrences(of: "{", with: "", options: .literal, range: nil))!
        
        let start = formula.firstIndex(of: String(format:"{%i", bracket_number))
        let end = formula.firstIndex(of: String(format:"}%i", bracket_number))
        let c_formula = formula[start!+1..<end!]

        var b_number = bracket_number
        var counter = 0
        var form: [[String]] = [[], [], [], []]
        var logical = ""
        for x in c_formula{
            if x.starts(with: "{"){
                b_number += 1
            }
            else if x.starts(with: "}"){
                b_number -= 1
            }
            if b_number == bracket_number{
                if x == ";"{

                    counter += 1
                    continue
                }

                if logic.keys.contains(x){
                    counter += 1
                    logical = x
                    continue
                }
            }
            form[counter].append(x)
        }

        for f in form[0..<2]{
            self.execute(formula: f)
        }

        let value1 = get_variable_value(key: form[0][0])
        let value2 = get_variable_value(key: form[1][0])

        logic[logical]!(value1, value2)

        print("The statement was", self.answerBool)

        if self.answerBool{
            self.execute(formula: form[2])
        }
        else{
            self.execute(formula: form[3])
        }
        print(formula[end!])
        let formula = self.remove_from_formula(start: start!-1, end: end!, formula: formula)

        return formula
    }
    
    func smaller(value1: Double, value2: Double){
        self.answerBool = value1 < value2
    }
    
    func smaller_or_equal(value1: Double, value2: Double){
        self.answerBool = value1 <= value2
    }
    
    func equal(value1: Double, value2: Double){
        self.answerBool = value1 == value2

    }

    func larger_or_equal(value1: Double, value2: Double){
        self.answerBool = value1 >= value2

    }

    func larger(value1: Double, value2: Double){
        self.answerBool = value1 > value2

    }

    func not_equal(value1: Double, value2: Double){
        self.answerBool = value1 != value2

    }

}
