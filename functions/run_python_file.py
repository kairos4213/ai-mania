import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
):
    try:
        if args is None:
            args = []

        abs_working_dir: str = os.path.abspath(working_directory)
        abs_file_path: str = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        cmd = ["python", abs_file_path]
        if args != []:
            cmd.extend(args)

        completed_process = subprocess.run(
            cmd, cwd=abs_working_dir, capture_output=True, text=True, timeout=30
        )

        outputString = ""
        if completed_process.returncode != 0:
            outputString += "Process exited with code X"
        if completed_process.stderr is None or completed_process.stdout is None:
            outputString += "No output produced"
        else:
            outputString += f"STDOUT: {completed_process.stdout}"
            outputString += f"STDERR: {completed_process.stderr}"

        return outputString
    except Exception as error:
        return f"Error: executing Python file: {error}"
