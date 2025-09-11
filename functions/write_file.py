import os

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    full_abs_path = os.path.abspath(full_path)
    working_dir_abs_path = os.path.abspath(working_directory)

    # Safer path check
    if os.path.commonpath([full_abs_path, working_dir_abs_path]) != working_dir_abs_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    file_dir = os.path.dirname(full_abs_path)
    os.makedirs(file_dir, exist_ok=True)

    try:
        with open(full_abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
