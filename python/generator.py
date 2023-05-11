from parser import VarDeclaration, PrintStatement, BinaryOperation


def generate_code(node, variables):
    if isinstance(node, VarDeclaration):
        variables[node.name] = node.value.value
        return ""
    elif isinstance(node, PrintStatement):
        if isinstance(node.expression, BinaryOperation):
            left = variables[node.expression.left.name]
            right = variables[node.expression.right.name]
            return f"""
section .data
    result dq 0
    format db "%d", 10, 0

section .text
    global main
    extern printf

main:
    sub rsp, 8
    mov rax, {left}
    add rax, {right}
    mov [result], rax
    mov rdi, format
    mov rsi, [result]
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
    for node in syntax_tree:
        assembly_code += generate_code(node, variables)
    return assembly_code

