from functions.get_file_content import get_file_content

print("Result for file 'main.py':")
print(get_file_content("calculator", "main.py"))

print("Result for 'calculator.py':")
print(get_file_content("calculator", "pkg/calculator.py"))

print("Result for '/bin/cat':")
print(get_file_content("calculator", "/bin/cat"))

print("Result for 'does_not_exist.py':")
print(get_file_content("calculator", "pkg/does_not_exist.py"))
