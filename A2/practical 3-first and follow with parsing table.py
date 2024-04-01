first = {}
follow = {}

productions = {
    'A': ['SB', 'B'],
    'S': ['a', 'Bc','ε'],
    'B': ['b', 'd'],
}


first = {}
def calculate_first(symbol):
    if symbol in first:
        return first[symbol]
    first_set = set()
    for production in productions[symbol]:
        if production[0].islower():
            first_set.add(production[0])
        elif production[0].isupper():
            first_set |= calculate_first(production[0])
            if 'ε' in first_set:
                first_set |= calculate_first(production[1:])
                first_set.discard('ε')

    first[symbol] = first_set
    return first_set

for symbol in productions.keys():
    calculate_first(symbol)



for symbol, first_set in first.items():
    print("FIRST({}): {}".format(symbol, first_set))




follow['A'] = {'$'}
start_symbol = 'A'
follow[start_symbol] = {'$'}




from collections import defaultdict
# from tabulate import tabulate

class Grammar:
    def __init__(self, productions):
        self.productions = productions
        self.start_symbol = list(self.productions.keys())[0]
        self.first = self.calculate_first()
        self.follow = self.calculate_follow()

    def calculate_first(self):
        first = defaultdict(set)
        for nt, rhs in reversed(self.productions.items()):
            for alt in rhs:
                for s in alt:
                    if s.isupper():
                        if 'ε' not in first[s]:
                            first[nt].update(first[s])
                            if 'ε' in first[nt]:
                                first[nt].remove('ε')
                            break
                        first[nt].update(first[s])
                    elif s != 'ε':
                        first[nt].add(s)
                        if 'ε' in first[nt]:
                            first[nt].remove('ε')
                        break
                    else:
                        first[nt].add('ε')
        return first

    def calculate_follow(self):
        follow = defaultdict(set)
        follow[self.start_symbol].add('$')
        while True:
            old_follow = dict(follow)
            for nt, rhs in self.productions.items():
                for alt in rhs:
                    for i, s in enumerate(alt):
                        if s.isupper():  # Nonterminal
                            if i+1 < len(alt):
                                follow[s].update(self.first[alt[i+1]])
                                if 'ε' in self.first[alt[i+1]]:
                                    follow[s].update(follow[nt])
                                    follow[s].discard('ε')
                            else:
                                follow[s].update(follow[nt])
            if old_follow == follow:
                break
        return follow

    def print_parsing_table(self):
        terminals = set()
        non_terminals = set()
        for nt, rhs in self.productions.items():
            non_terminals.add(nt)
            for alt in rhs:
                for s in alt:
                    if not s.isupper() and s != 'ε':
                        terminals.add(s)
        terminals = sorted(list(terminals))
        non_terminals = sorted(list(non_terminals))
        print(f"Non terminals: {non_terminals}")
        print(f"Terminals: {terminals}")

        matrix = []
        for nt in non_terminals:
            row = []
            for t in terminals:
                if t in self.first[nt]:
                    for prod in self.productions[nt]:
                        if prod[0] == t:
                            row.append(f"{nt} -> {prod}")
                            break
                    else:
                        row.append(' ')
                else:
                    row.append(' ')
            matrix.append(row)

        # table = tabulate(matrix, headers=terminals, showindex=non_terminals, tablefmt='grid')
        # print(table)

    def print_sets(self):
        print("FIRST sets:")
        for nt, first_set in self.first.items():
            print(f"{nt}: {sorted(first_set)}")

        print("\nFOLLOW sets:")
        for nt, follow_set in self.follow.items():
            print(f"{nt}: {sorted(follow_set)}")


def main():
    productions = {
        'A': ['SB', 'B'],
        'S': ['a', 'Bc','ε'],
        'B': ['b', 'd'],
    }
    grammar = Grammar(productions)
    grammar.print_sets()
    grammar.print_parsing_table()

if __name__ == "__main__":
    main()



