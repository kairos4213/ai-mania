import os
from google.genai import types

schema_write_file: types.FunctionDeclaration = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file with provided content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write file",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Contents of file being written",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory: str, file_path: str, content: str):
    try:
        abs_working_dir: str = os.path.abspath(working_directory)
        abs_file_path: str = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        with open(abs_file_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as error:
        return f"Error: {error}"
