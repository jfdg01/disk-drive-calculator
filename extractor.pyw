import os

def extract_code():
    # Define the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "code.txt")

    # Get a list of all .py files in the directory except this script
    python_files = [
        file for file in os.listdir(current_dir)
        if file.endswith('.py') and file != os.path.basename(__file__)
    ]

    with open(output_file, 'w') as outfile:
        for py_file in python_files:
            file_path = os.path.join(current_dir, py_file)
            with open(file_path, 'r') as infile:
                lines = infile.readlines()

            # Filter out import statements
            code_lines = [
                line for line in lines
                if not line.strip().startswith(('import ', 'from '))
            ]

            # Write to the output file
            outfile.write(f"# Content from {py_file}\n")
            outfile.writelines(code_lines)
            outfile.write("\n\n")

    print(f"Code extracted to {output_file}")

if __name__ == "__main__":
    extract_code()
