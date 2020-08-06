# StringFormulaReader
A class that reads a formula embedded in a string and is capable of executing it.

This project contains the string formula reader class for two languages swift 5 and python 3. Each is developed seperatly so there can be some differences between the classes.

## Usage python
To use this the python class add it to your current repository and import the reader.

The reader takes 1 argument this argument must have be a string. This string must contain the formula you want to execute and must folow the formating rules layed out in the chapter format. When the reader is initialized just run the execute function. The anwser is saved in the anwser variable.  
**Simple Example:**
```python3
from string_formula_reader import StringFormulaReader

# Initialize the reader
reader = StringFormulaReader("1+2")

# Execute the formula
reader.execute()

# Print the anwser
print(reader.anwser) # Prints 3
```
  
When you want to use variables in your formula you first need to give them a value. To do this you get the variables variable van de reader and with the variable you want to set as the key.  
**Variable Example:**
```python3
from string_formula_reader import StringFormulaReader

# Initialize the reader
reader = StringFormulaReader("a+b")

# Set value a
reader.variables["a"] = 3

# Set value b
reader.variables["b"] = 3

# Execute the formula
reader.execute()

# Print the anwser
print(reader.anwser) # Prints 6
```
## Format
To make sure the reader can read the given formula you sould keep to these formating rules. In the explanation below the variables will be used but in practice variables can be substituted with numbers.

### Add, subtract, multiply, devide, power
The add format is simple a varialbe should be besids the sign.
```
"a+b" or "a-b" or "a*b" or "a/b, or a^b"
```

### Root
Currently the only root that can be used is the second power root. This might change in the future. To add a root to your formula use the rood sign and on the right side a variable.
```
"√a"
```

### Log
To take the log of a value you type "log" folowed by a variable, with the default log being the 10 log. If you want another log just add the number behind the log eg "log15". If you want to use a number instead of a variable you sould put the number in brackeds
```
"loga" or "log15a" or "log15(15)"
```
