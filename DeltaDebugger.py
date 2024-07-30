import difflib
import subprocess
import jpype
import os

total_line_changes = []
diff = []
rand_name = 0

def modify_file(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        with open(file_name, 'w') as file:
            modified = False
            for line in lines:
                if not modified and line.__contains__("public static void main"):
                    file.write("public static void main(String[] args) {\n\n    new file1v1().fun(Integer.parseInt(args[0]), Integer.parseInt(args[1]), args[2]);\n\n}\n\n}\n")
                    modified = True
                elif modified:
                    break
                else:
                    file.write(line)

    except FileNotFoundError:
        print("File not found!")
    except IOError:
        print("Error reading/writing the file.")
        
def add_return_before_main(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        code_block = "public static void main(String[] args) {"
        has_return = any('return 0;' in line for line in lines)

        if not has_return:
            index_of_main = next(i for i, line in enumerate(lines) if code_block in line)
            index_of_closing_brace = index_of_main
            while index_of_closing_brace >= 0:
                if lines[index_of_closing_brace].strip() == '}':
                    lines[index_of_closing_brace] = "    return 0;}\n"
                    break
                index_of_closing_brace -= 1

            with open(filename, 'w') as file:
                file.writelines(lines)

    except FileNotFoundError:
        print("File not found!")
    except IOError:
        print("Error reading/writing the file.")

def remove_return_zero(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        has_return_0 = any('return 0;' in line for line in lines)
        has_return_1 = any('return 1;' in line for line in lines)

        if has_return_0 and has_return_1:
            lines = [line for line in lines if 'return 1;' not in line]

            with open(filename, 'w') as file:
                file.writelines(lines)

    except FileNotFoundError:
        print("File not found!")
    except IOError:
        print("Error reading/writing the file.")

def read_code_files():
    with open("Baseline.txt", 'r', encoding='utf-8') as file:
        Baseline = file.readlines()
    with open("Configured.txt",'r', encoding='utf-8') as file:
        Configured = file.readlines()
    return Baseline, Configured

def difference(Baseline, Configured):
    global diff
    differ = difflib.Differ()
    diff = list(differ.compare(Baseline, Configured))
    changes = []

    for line, i in zip(diff, range(len(diff))):
        code = line[2:]
        if line.startswith(' '):
            continue
        elif line.startswith('- '):
            change = {
                'type': 'deletion',
                'line_number': i,
                'code': code,
            }
            changes.append(change)
        elif line.startswith('+ '):
            change = {
                'type': 'addition',
                'line_number': i,
                'code': code,
            }
            changes.append(change)
    return diff, changes

def run_java_code(file_name):
    file_literal = file_name.replace(".java", "")
    replace_string_in_file(file_name, "file1v1", file_literal)
    subprocess.run(["javac", file_name])
    try:
        java_class = jpype.JClass(file_literal)
    except Exception as e:
        return 1
    java_instance = java_class()
    try:
        java_instance.fun(5, 0, "division")
        result = 1
    except Exception as e:
        print(e)
        result = 0
    return result

def testing(changes):
    global total_line_changes
    global diff
    new_code, new_line_change, rest = [], [], []
    for change in changes:
        new_line_change.append(change['line_number'])
    rest = list(set(total_line_changes) - set(new_line_change))
    for i in range(len(diff)):
        if i in new_line_change and diff[i].startswith('+ '):
            new_code.append(diff[i][2:])
        elif i in new_line_change and diff[i].startswith('- '):
            continue
        elif i in rest and diff[i].startswith('- '):
            if diff[i][2:] == "        int bcbc = 1;\n":
                continue
            new_code.append(diff[i][2:])
        elif i in rest and diff[i].startswith('+ '):
            continue
        elif diff[i].startswith('? '):
            continue
        else:
            new_code.append(diff[i][2:])
    modified_code = '\n'.join(new_code)
    global rand_name
    file_name = "file1v" + str(rand_name) + ".java"
    rand_name += 1
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(modified_code)
    modify_file(file_name)
    add_return_before_main(file_name)
    remove_return_zero(file_name)
    test_output = run_java_code(file_name)
    return test_output

def process_minimum_set(minimum_set):
    return minimum_set[0]

def dict_union(dict1, dict2):
    union_set = set(frozenset(d.items()) for d in dict1).union(set(frozenset(d.items()) for d in dict2))
    union_list = [dict(union_item) for union_item in union_set]
    sorted_union_list = sorted(union_list, key=lambda x: x['line_number'])
    return sorted_union_list

def dd(changes, r):
    if len(changes) == 1:
        return [changes[0]]
    split_point = len(changes) // 2
    c1, c2 = changes[:split_point], changes[split_point:]
    
    if testing(c1) == 1:
        r = dict_union(r, c1)
    elif testing(c2) == 1:
        r = dict_union(r, c2)

    if testing(c1) == 0:
        print(f"changes giving errors:\n............... {c1}...........................")
        return dd(c1, r)
    elif testing(c2) == 0:
        print(f"changes giving errors:\n............... {c2}...........................")
        return dd(c2, r)
    else:
        print(f"Both changes giving errors change1={c1} and change={c2} ")
        result1 = dd(c1, dict_union(c1, r))
        result2 = dd(c2, dict_union(c2, r))
        return dict_union(result1, result2)
    
def line_changes(diff, changes):
    global total_line_changes
    for change in changes:
        total_line_changes.append(change['line_number'])
    return total_line_changes

def replace_string_in_file(file_name, str1, str2):
    try:
        with open(file_name, 'r') as file:
            filedata = file.read()

        new_filedata = filedata.replace(str1, str2)

        with open(file_name, 'w') as file:
            file.write(new_filedata)

    except FileNotFoundError:
        print("File not found!")
    except IOError:
        print("Error reading/writing the file.")

def main():
    Baseline, Configured = read_code_files()
    diff, changes = difference(Baseline, Configured)
    total_line_changes = line_changes(diff, changes)
    r = []
    split_point = len(changes) // 2
    c1, c2 = changes[:split_point], changes[split_point:]
    minimum_set = dd(changes, r)
    print("\n\n\nHere we are getting the minimum set of changes\n")
    print(minimum_set)
    
if __name__ == "__main__":
    jpype.startJVM()
    main()
    jpype.shutdownJVM()
