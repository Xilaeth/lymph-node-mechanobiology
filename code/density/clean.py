import os

lst = os.listdir("after")
n = len(lst)

def extract_content_up_to_line(input_file, output_file, target_content):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    stop_line_index = None
    for index, line in enumerate(lines):
        if target_content in line:
            stop_line_index = index
            break

    if stop_line_index is None:
        print(f"Content '{target_content}' not found in the file.")
        return

    extracted_lines = lines[:stop_line_index - 1]
    
    with open(output_file, 'w') as output:
        output.writelines(extracted_lines)

for i in lst: 
    print("file: ", i)
    input_file = f"after/{i}"
    output_file = f"after/{i}"
    target_content = 'VERTICES' 

    extract_content_up_to_line(input_file, output_file, target_content)
