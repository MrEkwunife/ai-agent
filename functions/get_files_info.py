import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    absolute_path = os.path.abspath(working_directory)
    full_abs_path = os.path.abspath(full_path)

    if not full_abs_path.startswith(absolute_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_abs_path):
        return f'Error: "{directory}" is not a directory'

    try:
        content_info_dir = []

        for item in os.listdir(full_abs_path):
            new_path = os.path.join(full_abs_path, item)
            content_info_dir.append(f'- {item}: file_size={os.path.getsize(new_path)} bytes, is_dir={os.path.isdir(new_path)}')

        return "\n".join(content_info_dir)
    except Exception as e:
        return f'Error: {e}'
