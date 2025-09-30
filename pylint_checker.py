import subprocess
import sys
import ast

def run_pylint(file_path):
    """Run pylint with specific options on the given file."""
    try:
        result = subprocess.run(
            ['pylint', '--disable=C,E0401', file_path],
            capture_output=True,
            text=True,
            check=True
        )
        print("Pylint Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Pylint Errors:")
        print(e.stdout)
    except FileNotFoundError:
        print("pylint is not installed. Please install it using 'pip install pylint'.")

def analyze_functions(file_path):
    """Analyze the file for functions that return None or are empty."""
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    print("\nAnalysis of Functions:")
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            if not node.body:
                print(f"Function '{func_name}' is empty.")
            else:
                for stmt in node.body:
                    if isinstance(stmt, ast.Return) and stmt.value is None:
                        print(f"Function '{func_name}' explicitly returns None.")
                        break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pylint_checker.py <file_path>")
    else:
        file_path = sys.argv[1]
        print(f"Running pylint and analyzing functions in: {file_path}")
        run_pylint(file_path)
        analyze_functions(file_path)
