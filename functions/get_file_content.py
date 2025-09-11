import os
from config import MAX_CHARACTERS


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    full_abs_path = os.path.abspath(full_path)
    working_dir_abs_path = os.path.abspath(working_directory)

    if not full_abs_path.startswith(working_dir_abs_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(full_abs_path, 'r', encoding='utf-8') as file_object:
        try:
            with open(full_abs_path, 'r', encoding='utf-8') as f:
                content = f.read()

                if (len(content) > MAX_CHARACTERS):
                    return f'{content[:MAX_CHARACTERS]} [...File "{file_path}" truncated at 10000 characters]'

                return content

        except Exception as e:
            return f'Error: {e}'
