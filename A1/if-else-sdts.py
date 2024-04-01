def generate_3_address_code(input_construct):
    lines = input_construct.split('\n')
    code = []
    address = 1
    temp_count = 1

    for line in lines:
        line = line.strip()
        if line.startswith("if"):
            conditions = line.split('(')[1].split('&&')
            condition1 = conditions[0].strip()
            condition2 = conditions[1].strip().split(')')[0].strip()
            code.append(f"{address}) if {condition1} goto {address + 2}")
            code.append(f"{address + 1}) goto {address + 9}")
            code.append(f"{address + 2}) if {condition2} goto {address + 4}")
            code.append(f"{address + 3}) goto {address + 9}")
            address += 4
        elif line.startswith("else"):
            code.append(f"{address}) goto {address + 8}")
            address += 1
        elif line.startswith("{") or line.startswith("}"):
            continue
        else:
            operands = line.split('=')
            result = operands[0].strip()
            expression = operands[1].strip().replace(';', '')
            temp_var = f"T{temp_count}"
            code.append(f"{address}) {temp_var} = {expression}")
            code.append(f"{address + 1}) {result} = {temp_var}")
            temp_count += 1
            address += 2

    code.append(f"{address}) END")

    return code

# Input your if-else construct here
input_construct = """if (a<5 && b>c)
{
    c= b+d;
    d= i+j;
}
else
{
    d= a+ b;
    k= x+y;
}"""

three_address_code = generate_3_address_code(input_construct)
for instruction in three_address_code:
    print(instruction)