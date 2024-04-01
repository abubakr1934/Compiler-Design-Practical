from typing import List
import re


l: List[int] = []
with open("input.txt", "r") as f:
    k = f.readlines()
    l.append(k)
# print(k)
l = [i.strip() for i in l[0]]
# print(l)

OPERATORS = ["+", "-", "/", "*", "<", ">"]


def eliminate_dead_code(l):
    lhs = []
    rhs = []
    combined = []
    for i in l:
        l, r = i.split("=")
        lhs.append(l.strip())
        rhs.append(r.strip())
        combined.append([l.strip(), r.strip()])
    return combined


combined = eliminate_dead_code(l)
print(combined)
print("Original")
for _ in combined:
    print(f"{_[0]} = {_[1]}")

print()
new_combined = []
for i in range(len(combined)):
    a = combined[i][0]
    flag = 0
    for j in range(len(combined)):
        if i == j:
            continue
        k = combined[j][1]
        for k_ in k:
            if k_ == a:
                flag = 1
                break

    if flag or i == len(combined) - 1:
        new_combined.append(combined[i])

# print(new_combined)
print("After removing dead code")
for _ in new_combined:
    print(f"{_[0]} = {_[1]}")
print()

props = []


def evaluate_expression(expr):
    output = ""
    i = 0
    while i < len(expr):
        if expr[i] == " ":
            i += 1
            continue
        if expr[i].isalpha():
            s = ""
            j = i
            while j < len(expr) and expr[j].isalpha():
                output += expr[j]
                j += 1
            i = j
        elif expr[i] in "+-/*":
            output += " " + expr[i] + " "
            i += 1
        else:
            s = ""
            while i < len(expr) and not expr[i].isalpha():
                s += expr[i]
                i += 1
            if s[-1] in "+-/*":
                las = s[-1]
                s = s.strip("+/-*")
                ans = eval(s)
                output += str(ans)
                output += " " + las + " "
            else:
                ans = eval(s)
                output += str(ans)
            i += 1
    # pattern = re.compile("[a-zA-Z]")
    # result = re.sub(pattern, "0", expr)
    # print(result)
    # print(eval(result))
    return output


# print(f"Ans:- {evaluate_expression("x+2+3")}")


def constant_propogation(new_combined):
    for i in range(len(new_combined)):
        l, r = new_combined[i][0], new_combined[i][1]
        flag = 0
        flag = 0
        for j in range(len(new_combined)):
            string = ""
            if i == j:
                continue
            for k in range(len(new_combined[j][1])):
                if new_combined[j][1][k] == l:
                    flag = 1
                    string += r
                else:
                    string += new_combined[j][1][k]
            if flag:
                new_combined[j][1] = string
                props.append(new_combined[j])
            else:
                props.append(new_combined[j])


kk = {}
ops = []
ops1 = []
for c in new_combined:
    if c[1] not in kk:
        kk[c[1]] = c[0]
        ops1.append(c)
        continue
    else:
        if kk[c[1]] not in ops:
            # print("Hell:- " + kk[c[1]], c[0])
            ops1.append([c[0], kk[c[1]]])
            c[0] = kk[c[1]]
        else:
            ops1.append(c)
    ops.append(c[0])


print("Common subexpression elimination")
for i in ops1:
    print(f"{i[0]} = {i[1]}")
print()
constant_propogation(ops1)
props = [tuple(i) for i in props]
d = {k: 1 for k in props}
# print(props)
print("\nPropogation")
props = [i for i in d.keys()]
# print(props)
lhss = l[-1].split("=")[0].strip()
# print(lhss)
left_expr = None
for i in props:
    if i[0] == lhss:
        left_expr = i
        break
# print(left_expr)

final_exp = left_expr[1]
final_eval = evaluate_expression(final_exp)
print(f"{left_expr[0]} = {final_eval}")