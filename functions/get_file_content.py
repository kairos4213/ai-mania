import os
from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir_path: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(
            os.path.join(abs_working_dir_path, file_path)
        )

        valid_target_file: bool = (
            os.path.commonpath([abs_working_dir_path, target_file])
            == abs_working_dir_path
        )
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            contents: str = f.read(MAX_CHARS)
            if f.read(1):
                contents += (
                    f'[...File "{target_file}" truncated at {MAX_CHARS} characters]'
                )

        return contents
    except Exception as error:
        return f"Error: {error}"
