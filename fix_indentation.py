import subprocess
import sys
import os
import glob

def run_autopep8(input_path):
    """Run autopep8 --in-place on the given file or all .py files in a directory."""
    if os.path.isfile(input_path):
        # If input is a file, format it
        _format_file(input_path)
    elif os.path.isdir(input_path):
        # If input is a directory, format all .py files recursively
        python_files = glob.glob(os.path.join(input_path, '**', '*.py'), recursive=True)
        if not python_files:
            print(f"No Python files found in directory: {input_path}")
        for file_path in python_files:
            _format_file(file_path)
    else:
        print(f"Invalid input: {input_path} is neither a file nor a directory.")

def _format_file(file_path):
    """Helper function to format a single file using autopep8."""
    try:
        subprocess.run(['autopep8', '--in-place', file_path], check=True)
        print(f"Formatted {file_path} using autopep8.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running autopep8 on {file_path}: {e}")
    except FileNotFoundError:
        print("autopep8 is not installed. Please install it using 'pip install autopep8'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_indentation.py <file_or_directory_path>")
    else:
        input_path = sys.argv[1]
        run_autopep8(input_path)
