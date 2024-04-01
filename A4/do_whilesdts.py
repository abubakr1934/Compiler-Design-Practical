class ThreeAddressGenerator:
    def __init__(self):
        self.temp_count = 1
        self.code = []

    def new_temp(self):
        temp = f"T{self.temp_count}"
        self.temp_count += 1
        return temp

    def generate_code(self, condition, true_statements, false_statements):
        code = []
        code.append("START")
        for statement in true_statements:
            code.extend(self.parse_statement(statement))
        code.append(f"if {condition} goto {len(code) + 2}")
        code.append(f"goto {len(code) + 3}")
        for statement in false_statements:
            code.extend(self.parse_statement(statement))
        code.append("END")
        return code

    def parse_statement(self, statement):
        code = []
        tokens = statement.split()
        if tokens[0] == 'if':
            code.append(f"if {''.join(tokens[1:])} goto {len(code) + 2}")
            code.append("goto X")
        elif tokens[0] == 'goto':
            code.append(f"{tokens[0]} {tokens[1]}")
        elif len(tokens) >= 3 and tokens[1] == '=':
            temp = self.new_temp()
            code.append(f"{temp}={''.join(tokens[2:])}")
            code.append(f"{tokens[0]}={temp}")
        else:
            code.append(statement)
        return code

if __name__ == "__main__":
    generator = ThreeAddressGenerator()
    condition = "(x>10)"
    true_statements = [
        "y = x * 2",
        "z = y - 5"
    ]
    false_statements = [
        "z = x + 5",
        "y = z * 2"
    ]
    code = generator.generate_code(condition, true_statements, false_statements)
    for line in code:
        print(line)
