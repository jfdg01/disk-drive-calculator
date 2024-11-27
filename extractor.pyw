import os
import glob

def extract_code():
    # Define the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "code.txt")

    # Manually defined list of included files or directories
    # Update this list with patterns such as 'test/*.py' or 'scripts/example.py'
    root = 'source/'
    disk_related = root + 'disk_related/'

    include_patterns = [
        disk_related + "*.py",  # Example: include all .py files in the 'source/disk_related/' folder
    ]

    # Get a list of all .py files in the current directory except this script
    python_files = [
        file for file in os.listdir(current_dir)
        if file.endswith('.py') and file != os.path.basename(__file__)
    ]

    # Add files from include_patterns if include patterns is not empty
    if include_patterns:
        for pattern in include_patterns:
            included_files = glob.glob(os.path.join(current_dir, pattern))
            python_files.extend(
                os.path.relpath(file, current_dir) for file in included_files
            )

    # Remove duplicates and ensure only .py files are included
    python_files = list(set(file for file in python_files if file.endswith('.py')))

    # Open the output file in write mode (overwrites existing content)
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
