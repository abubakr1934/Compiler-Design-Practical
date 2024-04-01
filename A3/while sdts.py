from typing import List
import pandas as pd


class Expression:
    def _init_(self, operator=None, left_expr=None, right_expr=None, value=None):
        self.operator = operator
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.value = value

    def _str_(self):
        return (
            f"{self.operator=} | {self.left_expr=} | {self.right_expr=} | {self.value=}"
        )

    def generate_3addr_code(self):
        if self.operator is None:
            return self.value
        elif self.operator == "+":
            return f"T{self.value}=T{self.left_expr.generate_3addr_code()}+T{self.right_expr.generate_3addr_code()}"
        elif self.operator == "-":
            return f"T{self.value}=T{self.left_expr.generate_3addr_code()}-T{self.right_expr.generate_3addr_code()}"
        elif self.operator == "*":
            return f"T{self.value}=T{self.left_expr.generate_3addr_code()}*T{self.right_expr.generate_3addr_code()}"
        elif self.operator == "/":
            return f"T{self.value}=T{self.left_expr.generate_3addr_code()}/T{self.right_expr.generate_3addr_code()}"
        elif self.operator == "<":
            return f"if (T{self.left_expr.generate_3addr_code()}<T{self.right_expr.generate_3addr_code()}) goto {self.value}"


def build(string, start, end):
    if start >= end:
        return Expression(value=int(string[start:end]))

    operator_indices = [i for i in range(start, end) if string[i] in "+-*/<"]
    if not operator_indices:  # no operator found
        return Expression(value=(string[start:end]))

    op_index = min(operator_indices)  # choose the first operator
    root = Expression(operator=string[op_index])
    root.left_expr = build(string, start, op_index)
    root.right_expr = build(string, op_index + 1, end)
    return root


# Example usage:
lines = []
with open("input.txt", "r") as f:
    lines = f.readlines()

expression_string = lines[0].strip()
start = expression_string.index("(") + 1
end = expression_string.index(")")
root = build(expression_string, start, end)

# output = ""


# print(root.generate_3addr_code())
def inorder(root):
    # global output
    if root is None:
        return
    # output += "("
    inorder(root.left_expr)
    print(root)
    # output += root.value
    inorder(root.right_expr)
    # output += ")"


OPERATORS = ["+", "-", "*", "/", "<", ">", "="]


def go_get_tokens(s):
    d = {}
    for i in range(len(s)):
        if s[i] in OPERATORS:
            if s[i] not in d:
                d[s[i]] = []
            d[s[i]].append((s[:i], s[i + 1 :]))
    if "=" in d:
        return ["=", d["="]]
    elif "/" in d:
        return ["/", d["="]]
    elif "*" in d:
        return ["", d[""]]
    elif "+" in d:
        return ["+", d["+"]]
    elif "-" in d:
        return ["-", d["-"]]


class Statement:
    def _init_(self, L):
        self.list_of_statements = L


class Assignment:
    def _init_(self, e1, e2):
        self.operator = "="
        self.left_expr = e1
        self.right_expr = e2

    def _str_(self):
        return f"{self.operator=} | {self.left_expr=} | {self.right_expr=}"


def parse_statements(statements):
    assigns = []
    for i in statements:
        tokens = go_get_tokens(i)
        op, l = tokens
        left = build(l[0][0], 0, len(l[0][0]))
        right = build(l[0][1], 0, len(l[0][1]))
        assignment = Assignment(left, right)
        assigns.append(assignment)
    return assigns


# inorder(root)
# print(output)
statemenst = []
lines = [_.strip() for _ in lines]
open = lines.index("{") + 1
end = lines.index("}")
# print(lines[open:end])
assignments = parse_statements(lines[open:end])
# print(assignments)
# for i in assignments:
#     print("*** Statement ****")
#     print()
#     print("Left")
#     inorder(i.left_expr)
#     print(f"Operator: {i.operator}")
#     print("Right")
#     inorder(i.right_expr)
#     print()
#
statement_object = Statement(assignments)


class WhileExpression:
    def _init_(self, expressions, statement):
        self.t1 = "while"
        self.m1 = None
        self.expression = expressions
        self.statements = statement


while_expression = WhileExpression(root, statement_object)
print(while_expression)


three_address_codes = []


def statement_tac(statement):
    variables = 1
    for s in statement:
        # print(s)
        left_val = s.left_expr.value
        right_val = ""
        right_val += (
            s.right_expr.left_expr.value
            + s.right_expr.operator
            + s.right_expr.right_expr.value
        )
        right_val = right_val.strip(";")
        # print(left_val)
        # print(right_val)
        three_address_codes.append(f"T{variables} = {right_val}")
        three_address_codes.append(f"{left_val} = T{variables}")
        variables += 1


START = 0


def expression_tac(expression):
    exp = ""
    # print(expression.left_expr)
    # print(expression.right_expr)
    exp += (
        expression.left_expr.value + expression.operator + expression.right_expr.value
    )
    three_address_codes.append(f"if ({exp}) then goto :- {START + 2}")
    three_address_codes.append("goto :- ")


expression_tac(while_expression.expression)
statement_tac(while_expression.statements.list_of_statements)
three_address_codes.append(f"goto :- {START}")
END = len(three_address_codes)
three_address_codes[1] = f"goto :- {START + END}"
three_address_codes.append("END")
# print(three_address_codes)
# for s in three_address_codes:
#     print(s)

d = {"TAC": three_address_codes}
df = pd.DataFrame(d)
s = "10*5-4/5"
r2 = build(s, 0, len(s))
print(df)
inorder(r2)