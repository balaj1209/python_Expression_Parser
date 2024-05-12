import tkinter as tk
from tkinter import *


class ExpressionParser:
    def __init__(self):
        """
        Initialize the Expression Parser class with a dictionary of numeric operators
        and their precedence
        """
        self.numeric_operators = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    def tokenize(self, expression):
        """
        Tokenize the input expression
        Returns:
        List of tokens extracted from the expression
        """
        tokens = []
        current_token = ''

        for char in expression:
            if char.isdigit() or char == '.':
                current_token += char
            elif char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
            else:
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
                tokens.append(char)

        if current_token:
            tokens.append(current_token)

        return tokens

    def validate_numeric(self, tokens):
        """
        Validate if the expression contains valid numeric operations
        """
        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                if not stack:
                    return "Invalid parenthesis"
                stack.pop()
        if stack:
            return "Parenthesis is missing"
        if tokens[0] in self.numeric_operators or tokens[-1] in self.numeric_operators:
            return "Invalid expression"
        return True
    
    def validate_alphabetic(self, tokens):
        """
        Validate if the expression contains valid alphabetic operations
        """
        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                if not stack:
                    return "Invalid parenthesis"
                stack.pop()
        if stack:
            return "Parenthesis is missing"
        if tokens[0].isalpha() and len(tokens) == 1:
            return "Invalid expression: Only one variable"
        return True

    def evaluate_numeric(self, tokens):
        """
        Evaluate the numeric expression
        """
        stack = []
        operators = []
        i = -1
        while i < len(tokens):
            token = tokens[i]
            if token.replace('.', '', 1).isdigit():
                num = float(token)
                if num.is_integer():  # Check if the number is an integer
                    num = int(num)  # Convert to integer if it is
                stack.append(num)
            elif token in self.numeric_operators:
                while operators and operators[-1] != '(' and self.numeric_operators[operators[-1]] >= self.numeric_operators[token]:
                    self.apply_operator(stack, operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators[-1] != '(':
                    self.apply_operator(stack, operators.pop())
                operators.pop()  
            i += 1
        while operators:
            self.apply_operator(stack, operators.pop())
        return stack[-1]

    def evaluate_alphabetic(self, tokens):
        """
        Evaluate the alphabetic expression
        """
        return "Valid expression"

    def evaluate_alphanumeric(self, tokens):
        """
        Evaluate the alphanumeric expression
        """
        numerical_tokens = [ord(token.lower()) - ord('a') + 1 if token.isalpha() else token for token in tokens]
        return self.evaluate_numeric(numerical_tokens)

    def apply_operator(self, stack, operator):
        """
        Apply the operator to the operands on the stack
        """
        b = stack.pop()
        a = stack.pop()
        if operator == '+':
            stack.append(a + b)
        elif operator == '-':
            stack.append(a - b)
        elif operator == '*':
            stack.append(a * b)
        elif operator == '/':
            stack.append(a / b)

    def evaluate(self, expression):
        """
        Evaluate the given expression
        """
        tokens = self.tokenize(expression)
        validation_numeric = self.validate_numeric(tokens)
        if validation_numeric is not True:
            return "Numeric Validation Error: " + validation_numeric
        validation_alphabetic = self.validate_alphabetic(tokens)
        if validation_alphabetic is not True:
            return "Alphabetic Validation Error: " + validation_alphabetic

        if tokens[0].isdigit():
            result = self.evaluate_numeric(tokens)
        elif tokens[0].isalpha():
            result = self.evaluate_alphabetic(tokens)
        else:
            result = self.evaluate_alphanumeric(tokens)

        return result

def evaluate_expression():
    """
    Evaluate the expression provided by the user
    """
    expression = input_box.get("1.0", "end-1c")
    expression_parser = ExpressionParser()
    result = expression_parser.evaluate(expression)
    result_box.delete("1.0", "end")
    result_box.insert("1.0", result)

# Create the GUI window
root = tk.Tk()
root.title("Parser")
root.geometry("1800x1800")
root.config(bg="#FFF8DC")

# Header
tk.Label(root, text="//-+-*--EXPRESSION PARSER-+-*--//", width=30,
         height=2, borderwidth=4, relief="ridge", font=("Arial", 25, "bold"), bg="#FFF8DC").place(x=480, y=75)

# Input label and box
tk.Label(root, text="Enter the Expression:", font=("Arial", 12, "bold"), bg="#FFF8DC").place(x=350, y=263)
input_box = tk.Text(root, height=1.5, width=50)
input_box.place(x=520, y=260)

# Evaluate button
evaluate_button = tk.Button(root, text="Evaluate",font=("Arial", 11, "bold"), command=evaluate_expression, bg="#8B8878", fg="white", pady=6, padx=30)
evaluate_button.place(x=1000, y=260)

# Result label and box
tk.Label(root, text="Result:", font=("Arial", 12, "bold"), bg="#FFF8DC").place(x=450, y=450)
result_box = tk.Text(root, height=7, width=50)
result_box.place(x=520, y=450)

# Quit button
quit_button = tk.Button(root, text="Quit",font=("Arial", 11, "bold"), command=root.destroy, bg="#8B8878", fg="white", pady=6, padx=35)
quit_button.place(x=980, y=580)

# Run the GUI main loop
root.mainloop()
