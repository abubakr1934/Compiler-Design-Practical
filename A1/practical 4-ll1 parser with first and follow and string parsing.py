def first(string):
    first_ = set()
    if string in non_terminals:
        alternatives = productions_dict[string]
        for alternative in alternatives:
            first_2 = first(alternative)
            first_ = first_ | first_2
    elif string in terminals:
        first_ = {string}
    elif string == '' or string == '#':
        first_ = {'#'}
    else:
        first_2 = first(string[0])
        if '#' in first_2:
            i = 1
            while '#' in first_2:
                first_ = first_ | (first_2 - {'#'})
                if string[i:] in terminals:
                    first_ = first_ | {string[i:]}
                    break
                elif string[i:] == '':
                    first_ = first_ | {'#'}
                    break
                first_2 = first(string[i:])
                first_ = first_ | first_2 - {'#'}
                i += 1
        else:
            first_ = first_ | first_2
    return first_

def follow(nT):
    follow_ = set()
    prods = productions_dict.items()
    if nT == starting_symbol:
        follow_ = follow_ | {'$'}
    for nt, rhs in prods:
        for alt in rhs:
            for char in alt:
                if char == nT:
                    following_str = alt[alt.index(char) + 1:]
                    if following_str == '':
                        if nt == nT:
                            continue
                        else:
                            follow_ = follow_ | follow(nt)
                    else:
                        follow_2 = first(following_str)
                        if '#' in follow_2:
                            follow_ = follow_ | follow_2 - {'#'}
                            follow_ = follow_ | follow(nt)
                        else:
                            follow_ = follow_ | follow_2
    return follow_

terminals = ['$', 'a', 'b', 'p', 'c']
non_terminals = ['S', 'A', 'B', 'C']
starting_symbol = 'S'
productions = ['S->A|BC', 'A->a|b', 'B->p|#', 'C->c']

productions_dict = {}
for nT in non_terminals:
    productions_dict[nT] = []
for production in productions:
    nonterm_to_prod = production.split("->")
    alternatives = nonterm_to_prod[1].split("|")
    for alternative in alternatives:
        productions_dict[nonterm_to_prod[0]].append(alternative)

FIRST = {}
FOLLOW = {}
for non_terminal in non_terminals:
    FIRST[non_terminal] = set()
for non_terminal in non_terminals:
    FOLLOW[non_terminal] = set()

for non_terminal in non_terminals:
    FIRST[non_terminal] = FIRST[non_terminal] | first(non_terminal)

FOLLOW[starting_symbol] = FOLLOW[starting_symbol] | {'$'}
for non_terminal in non_terminals:
    FOLLOW[non_terminal] = FOLLOW[non_terminal] | follow(non_terminal)

print("{: ^20}{: ^20}{: ^20}".format('Non Terminals', 'First', 'Follow'))
for non_terminal in non_terminals:
    print("{: ^20}{: ^20}{: ^20}".format(non_terminal, str(FIRST[non_terminal]), str(FOLLOW[non_terminal])))










def generate_LL1_table(productions):
    ll1_table = {}
    for non_terminal in non_terminals:
        ll1_table[non_terminal] = {}
        for terminal in terminals:
            ll1_table[non_terminal][terminal] = []

    for production in productions:
        non_terminal, production_body = production.split("->")
        production_body = production_body.split("|")
        first_set = first(production_body[0])
        for terminal in first_set:
            ll1_table[non_terminal][terminal].append(production_body[0])

        if '#' in first_set:
            follow_set = follow(non_terminal)
            for terminal in follow_set:
                ll1_table[non_terminal][terminal].append(production_body[0])
    return ll1_table

ll1_table = generate_LL1_table(productions)

print("LL(1) Parsing Table:")
for non_terminal in non_terminals:
    print(non_terminal, ll1_table[non_terminal])







def validate_string(input_string):
    stack = ["$", starting_symbol]
    buffer = list(input_string)
    buffer.append("$")

    print("Stack\t\tBuffer\t\tAction")
    print("-----\t\t------\t\t------")

    while True:
        print(f"{' '.join(stack)}\t\t{' '.join(buffer)}\t\t", end="")

        top = stack[-1]
        front = buffer[0]

        if top == front == "$":
            print("String accepted")
            break

        elif top in terminals:
            if top == front:
                stack.pop()
                buffer.pop(0)
                print("Match")
            else:
                print("String rejected")
                break

        elif top in non_terminals:
            if front in FIRST[top]:
                production = productions_dict[top][0]
                stack.pop()
                if production != "#":
                    stack.extend(list(reversed(production)))
                print(f"Expand using {top} -> {production}")

            elif "#" in FIRST[top] and buffer[0] in FOLLOW[top]:
                stack.pop()
                stack.append("#")
                print(f"Expand using {top} -> #")

            else:
                print("String rejected")
                break

        else:
            print("Error: Invalid entry in the stack")
            break

validate_string("a$")
print()
validate_string("apc$")



    