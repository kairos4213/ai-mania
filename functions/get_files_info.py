import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_dir_path: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(
            os.path.join(abs_working_dir_path, directory)
        )

        valid_target_dir: bool = (
            os.path.commonpath([abs_working_dir_path, target_dir])
            == abs_working_dir_path
        )
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files_strs: list[str] = []
        for filename in os.listdir(target_dir):
            is_dir: bool = os.path.isdir(os.path.join(target_dir, filename))
            file_size: int = os.path.getsize(os.path.join(target_dir, filename))
            files_strs.append(f"{filename}: file_size={file_size}, is_dir={is_dir}")

        result = "Result for current directory:\n\t- "
        if directory != ".":
            result = f"Result for '{directory}':\n\t- "
        return result + "\n\t- ".join(files_strs)
    except Exception as error:
        return f"Error: {error}"
