# Write a program to generate three address code for the given language construct using SDTS (only for for loop).

# read for loop from the for_loop.txt file
def read_for_loop():
    with open("for_loop.txt", "r") as file:
        return file.read()
    

class ParseTreeNode:
    def __init__(self, data,attr=None):
        self.data = data
        self.children = []
        self.parent = None
        self.attributes = attr

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.data)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret




def get_tokens(for_loop):
    index_of_start_of_initialization  = for_loop.index("(")
    index_of_end_of_initialization = for_loop.index(")")
    initialization = for_loop[index_of_start_of_initialization+1:index_of_end_of_initialization]
    intialization,condition,increment = initialization.split(";")
    # simplify the increment
    if increment[-2:] == "++":
        increment = increment[:-2] + f"={increment[0]}+1"
    elif increment[-2:] == "--":
        increment = increment[:-2] + f"={increment[0]}-1"

    statement = for_loop[for_loop.index("{")+1:for_loop.index("}")]
    statements = statement.split(";")
    statements = list(map(lambda statement:statement.strip(),statements))
    statements = list(filter(lambda statement:statement!="",statements))

    return intialization,condition,increment,statements


def generate_parse_tree(for_loop):
    initialization,condition,increment,statements = get_tokens(for_loop)
    root = ParseTreeNode("For Loop","root")

    # add intialization
    ini = ParseTreeNode(initialization, "intialization")
    expr,assignment = ini.data.split("=")
    ini.add_child(ParseTreeNode(expr))
    ini.add_child(ParseTreeNode("="))
    ini.add_child(ParseTreeNode(assignment))
    root.add_child(ini)
    root.add_child(ParseTreeNode('M','incr_addr'))
    # add condition
    con = ParseTreeNode(condition,"condition")
    opr = None
    for i in con.data:
        if i in ['<','>','=']:
            opr = i
            break
    expr1,expr2 = con.data.split(opr)
    con.add_child(ParseTreeNode(expr1,"id"))
    con.add_child(ParseTreeNode(opr,"relop"))
    con.add_child(ParseTreeNode(expr2,"id"))
    root.add_child(con)
    root.add_child(ParseTreeNode('M','incr_addr'))

    # add increment
    inc = ParseTreeNode(increment,"increment")
    expr,assignment = inc.data.split("=")
    opr=None
   
    for i in assignment:
        if i in ['+','-','*','/']:
            opr = i
            break
    assign = ParseTreeNode(assignment,"assignment")

    nested_expr1,nested_expr2 = assignment.split(opr)
    inc.add_child(ParseTreeNode(expr,"id"))
    inc.add_child(ParseTreeNode("=", "assign"))
    assign.add_child(ParseTreeNode(nested_expr1,"id"))
    assign.add_child(ParseTreeNode(opr,"op"))
    assign.add_child(ParseTreeNode(nested_expr2,"id"))
    inc.add_child(assign)
    root.add_child(inc)
    root.add_child(ParseTreeNode('M','incr_addr'))

    for statement in statements:
        statement_node = ParseTreeNode(statement,"statement")
        expr,assignment = statement_node.data.split("=")
        opr=None
        for i in assignment:
            if i in ['+','-','*','/']:
                opr = i
                break
        statement_node.add_child(ParseTreeNode(expr,"id"))
        statement_node.add_child(ParseTreeNode("=", "assign"))
        assign = ParseTreeNode(assignment,"assignment")
        nested_expr1,nested_expr2 = assignment.split(opr)
        assign.add_child(ParseTreeNode(nested_expr1,"id"))
        assign.add_child(ParseTreeNode(opr,"op"))
        assign.add_child(ParseTreeNode(nested_expr2,"id"))
        statement_node.add_child(assign)
        root.add_child(statement_node)
    return root

# inorder traversal of parse tree, and generate three address code
address = {"A":1}
def generate_three_address_code(node: ParseTreeNode, statements, three_address_code):
    if len(node.children) == 0:
        return three_address_code
    for child in node.children:
        three_address_code=generate_three_address_code(child, statements,three_address_code)
    if node.attributes == "intialization":
        three_address_code.append(f"{address['A']}. {node.children[0].data} = {node.children[2].data}")
        address['A'] += 1
    elif node.attributes == "condition":
        three_address_code.append(f"{address['A']}. if {node.children[0].data} {node.children[1].data} {node.children[2].data} goto {address['A'] + 4}")
        address['A'] += 1
        three_address_code.append(f"{address['A']}. goto {address['A'] + len(statements) + 4}")
        address['A'] += 1
    elif node.attributes == "increment":
        three_address_code.append(f"{address['A']}. {node.children[0].data} = {node.children[2].children[0].data} {node.children[2].children[1].data} {node.children[2].children[2].data}")
        address['A'] += 1
        three_address_code.append(f"{address['A']}. goto {2}")
        address['A'] += 1
    elif node.attributes == "statement":
        three_address_code.append(f"{address['A']}. {node.children[0].data} = {node.children[2].children[0].data} {node.children[2].children[1].data} {node.children[2].children[2].data}")
        address['A'] += 1
    elif node.attributes == "root":
        three_address_code.append(f"{address['A']}. goto {4}")
        address['A'] += 1
    return three_address_code



if __name__ == "__main__":
    for_loop = read_for_loop()
    print("For Loop: ")
    print(for_loop)
    parse_tree = generate_parse_tree(for_loop)
    print("Parse Tree: ")
    print(parse_tree)
    _,_,_,statements = get_tokens(for_loop)
    three_address_code=generate_three_address_code(parse_tree,statements=statements,three_address_code=[])
    print("Three Address Code: ")
    for code in three_address_code:
        print(code)