from parser import VarDeclaration, PrintStatement, BinaryOperation


def generate_code(node, variables, counter):
    if isinstance(node, VarDeclaration):
        variables[node.name] = node.value.value
        return ""
    elif isinstance(node, PrintStatement):
        counter['print'] += 1
        print_id = counter['print']     # get the current print count
        if isinstance(node.expression, BinaryOperation):
            left = variables[node.expression.left.name]
            right = variables[node.expression.right.name]
            # Note that for division, the above implementation does not handle the remainder, 
            # and it assumes integer division. To support floating-point numbers and arithmetic, 
            # we'll need to extend the language and the code generator accordingly.
            operation = {
                '+': 'add',
                '-': 'sub',
                '*': 'imul',
                '/': 'idiv'
            }[node.expression.operator]
            return f"""
section .data
    result{print_id} dq 0
    format{print_id} db "%d", 10, 0

section .text
    extern printf

print{print_id}:
    sub rsp, 8
    mov rax, {left}
    {operation} rax, {right}
    mov [result{print_id}], rax
    mov rdi, format{print_id}
    mov rsi, [result{print_id}]
    xor rax, rax
    call printf
    xor eax, eax
    add rsp, 8
    ret
"""
        else:
            value = variables[node.expression.name]
            return f"""
section .data
    result dq {value}
    format db "%d", 10, 0

section .text
    global main
    extern printf

main:
    sub rsp, 8
    mov rdi, format
    mov rsi, [result]
    xor rax, rax
    call printf
    xor eax, eax
    add rsp, 8
    ret
"""
    else:
        raise NotImplementedError(f"Code generation not implemented for this node type: {node.__class__}")


def generate_assembly(syntax_tree):
    variables = {}
    assembly_code = ""
    counter = {'print': 0}
    print_calls = [] # to store print function calls
    for node in syntax_tree:
        assembly_code += generate_code(node, variables, counter)
        if isinstance(node, PrintStatement):
            print_calls.append(f"call print{counter['print']}")

    print_line = '\n '.join(print_calls)
    main_function = f"""
section .text
    global main
    extern printf

main:
    sub rsp, 8
    {print_line}
    xor eax, eax
    add rsp, 8
    ret
"""

    return main_function + assembly_code

