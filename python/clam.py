import sys
import subprocess
from lexer import lex
from tree_parser import parse
from generator import generate_assembly
 

def compile_clam_file(input_file: str, output_file: str):
    with open(input_file, 'r') as f:
        source_code = f.read()

    tokens = lex(source_code)
    syntax_tree = parse(tokens)
    assembly_code = generate_assembly(syntax_tree)

    assembly_file = input_file.replace('.clam', '.s')
    with open(assembly_file, 'w') as f:
        f.write(assembly_code)
    
    obj_file = input_file.replace('.clam', '.o')
    subprocess.run(['nasm', '-f', 'elf64', assembly_file, '-o', obj_file])
    
    subprocess.run(['gcc', '-no-pie', obj_file, '-o', output_file])


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: python clam_compiler.py <input_file.clam> <output_binary>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    compile_clam_file(input_file, output_file)
