import os, subprocess, sys

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    full_abs_path = os.path.abspath(full_path)
    working_dir_abs_path = os.path.abspath(working_directory)

    if not full_abs_path.startswith(working_dir_abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_abs_path):
        return f'Error: File "{file_path}" not found.'

    if not full_abs_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            [sys.executable, full_abs_path] + args,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory
        )

        output_parts = []
        if result.stdout.strip():
            output_parts.append(f'STDOUT:\n{result.stdout.strip()}')
        if result.stderr.strip():
            output_parts.append(f'STDOUT:\n{result.stderr.strip()}')
        if result.returncode != 0:
            output_parts.append(f'Process exited with code {result.returncode}')

        if not output_parts:
            return "No output produced"

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: excuting python file: {e}"
