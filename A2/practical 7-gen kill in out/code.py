import pandas as pd

blocks = []

with open("input.txt", "r") as f:
    k = f.readlines()
k.append("\n")
# print(k)
temp = []
for i in k:
    if i == "\n":
        blocks.append(temp)
        temp = []
    else:
        temp.append(i)


for t in blocks:
    for y in range(len(t)):
        t[y] = t[y].strip("\n")


class Expression:
    def __init__(self, number, expression):
        self.number = number
        self.expression = expression

    def __str__(self):
        return f"{self.number}) {self.expression}"


class Blocks:
    def __init__(self, block_number, list_of_Expressions):
        self.lof_exprs = list_of_Expressions
        self.block_number = block_number

    def __str__(self):
        output = f"Printing block number: {self.block_number}\n"
        for i in self.lof_exprs:
            k = i
            output += str(k) + "\n"
        output += "\n"
        return output


expressions = []
blocks_class = []
number = 1
for i in range(len(blocks)):
    exprs = []
    for j in range(len(blocks[i])):
        exprs.append(Expression(number, blocks[i][j]))
        number += 1
    expressions.append(exprs)
    blocks_class.append(Blocks(i + 1, exprs))


DAG = {k: [] for k in blocks_class}
DAG[blocks_class[0]].extend([blocks_class[1]])
DAG[blocks_class[1]].extend([blocks_class[2], blocks_class[3]])
DAG[blocks_class[2]].extend([blocks_class[3], blocks_class[4]])
DAG[blocks_class[3]].extend([blocks_class[1], blocks_class[5]])
DAG[blocks_class[4]].extend([blocks_class[2]])
DAG[blocks_class[5]] = []


OUTPUT = {}
OUTPUT["Blocks"] = [f"B{i.block_number}" for i in blocks_class]
OUTPUT["GEN"] = [0] * len(blocks_class)
OUTPUT["KILL"] = [0] * len(blocks_class)
OUTPUT["Predecessor"] = [0] * len(blocks_class)
OUTPUT["IN"] = [set() for _ in range(len(blocks_class))]
OUTPUT["OUT"] = [0] * len(blocks_class)

# print(OUTPUT)

gen_array = []

for i in range(len(blocks_class)):
    temp_arr = []
    for j in blocks_class[i].lof_exprs:
        temp_arr.append(j.number)
    gen_array.append(temp_arr)

# print(gen_array)
OUTPUT["GEN"] = [set(i) for i in gen_array]

kill_arr = []
for i in range(len(blocks_class)):
    l_expr = blocks_class[i].lof_exprs
    lhs = []
    temp_kill = []
    for j in l_expr:
        e = j.expression.split("=")
        lhs.append(e[0].strip())
    for j in range(len(blocks_class)):
        if i == j:
            continue
        lexpr = blocks_class[j].lof_exprs
        for k in lexpr:
            t = k.expression.split("=")
            if t[0].strip() in lhs:
                temp_kill.append(k.number)
    kill_arr.append(temp_kill)

# print(kill_arr)
OUTPUT["KILL"] = [set(i) for i in kill_arr]

precedence_arr = []

for i in range(len(blocks_class)):
    curr = blocks_class[i]
    temp_prec = []
    for j in range(len(blocks_class)):
        if i == j:
            continue
        for it in DAG[blocks_class[j]]:
            if it.block_number == curr.block_number:
                temp_prec.append(blocks_class[j].block_number)
    precedence_arr.append(temp_prec)


OUTPUT["Predecessor"] = precedence_arr
OUTPUT["OUT"] = [set(i) for i in OUTPUT["GEN"]]

df = pd.DataFrame(OUTPUT)
print(f"Iteration: {0}")
print(df)

print()

iteration = 1
change = True
while change:
    change = False
    # prev_state = OUTPUT
    for i in range(len(blocks_class)):
        precs = OUTPUT["Predecessor"][i]
        temp_set = set()
        for p in precs:
            temp_set = temp_set.union(OUTPUT["OUT"][p - 1])
            # OUTPUT["IN"][i] = OUTPUT["IN"][i].union(OUTPUT["OUT"][p - 1])
            # print(OUTPUT["OUT"][p - 1])
        OUTPUT["IN"][i] = temp_set
        # print(f"Block: {i+1} and Set: {temp_set}")
        oldotp = OUTPUT["OUT"][i]
        OUTPUT["OUT"][i] = (OUTPUT["IN"][i] - OUTPUT["KILL"][i]).union(OUTPUT["GEN"][i])
        if oldotp != OUTPUT["OUT"][i]:
            change = True
    if change:
        print(f"Iteration: {iteration}")
        dff = pd.DataFrame(OUTPUT)
        print(dff)
        print()
        iteration += 1

    if not change:
        break
        # if OUTPUT == prev_state:
        # break
# print(OUTPUT["IN"])
print(f"Iteration: {iteration}")
dff = pd.DataFrame(OUTPUT)
print(dff)
