import difflib
import subprocess
import jpype
<<<<<<< HEAD
import os

total_line_changes=[]
diff=[]
rand_name = 0
=======

total_line_changes=[]
diff=[]

>>>>>>> c387f21f024f13015ff452f548054d1d4427431a

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
                    # Skip writing the rest of the file after the modification
                    break
                else:
                    file.write(line)

<<<<<<< HEAD
=======
        if modified:
            print("Modification successful!")
        else:
            print("Line not found in the file.")
>>>>>>> c387f21f024f13015ff452f548054d1d4427431a

    except FileNotFoundError:
        print("File not found!")
    except IOError:
        print("Error reading/writing the file.")
        
<<<<<<< HEAD
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

    
=======

>>>>>>> c387f21f024f13015ff452f548054d1d4427431a
def read_code_files():
    with open("Baseline.txt", 'r', encoding='utf-8') as file:
        Baseline = file.readlines()
    with open("Configured.txt",'r', encoding='utf-8') as file:
        Configured=file.readlines()
    return Baseline, Configured

def difference(Baseline, Configured):
    global diff
    differ = difflib.Differ()
    diff = list(differ.compare(Baseline, Configured))
    changes = []
<<<<<<< HEAD

=======
    #del diff[43]
    #diff[43]="  }\n"
    
>>>>>>> c387f21f024f13015ff452f548054d1d4427431a
    for line,i in zip(diff,range(len(diff))):
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

<<<<<<< HEAD
def run_java_code(file_name):
    file_literal = file_name.replace(".java", "")
    replace_string_in_file(file_name, "file1v1", file_literal)
    # Compile the Java file.
    # os.remove("file1v1.class")
    subprocess.run(["javac", file_name])
    # Get the Java class object for the Java file.
    try:
        java_class = jpype.JClass(file_literal)
    except Exception as e:
        return 1
=======
def run_java_code():
    # Compile the Java file.
    subprocess.run(["javac", "file1v1.java"])
    # Get the Java class object for the Java file.
    java_class = jpype.JClass("file1v1")
>>>>>>> c387f21f024f13015ff452f548054d1d4427431a
    # Create an instance of the Java class.
    java_instance = java_class()
    # Call the `fun()` method on the Java instance, passing in the three input arguments.
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
    new_code,new_line_change, rest=[],[],[]
    for change in changes:
        new_line_change.append(change['line_number'])
    rest=list(set(total_line_changes)-set(new_line_change))
    for i in (range(len(diff))):
        if i in new_line_change and diff[i].startswith('+ '):
            new_code.append(diff[i][2:])
        elif i in new_line_change and diff[i].startswith('- '):
            continue
        elif i in rest and diff[i].startswith('- '):
            if diff[i][2:]=="        int bcbc = 1;\n":
                continue
            new_code.append(diff[i][2:])
        elif i in rest and diff[i].startswith('+ '):
            continue
        elif diff[i].startswith('? '):
            continue
        else:
            new_code.append(diff[i][2:])
    modified_code = '\n'.join(new_code)
<<<<<<< HEAD
    global rand_name
    file_name = "file1v"+ str(rand_name) +".java"
    rand_name += 1
    with open(file_name,'w',encoding='utf-8') as file:
        file.write(modified_code)
    modify_file(file_name)
    add_return_before_main(file_name)
    remove_return_zero(file_name)
    test_output=run_java_code(file_name)
    return test_output

def process_minimum_set(minimum_set):
    return minimum_set[0]
=======
    with open("file1v1.java",'w',encoding='utf-8') as file:
        file.write(modified_code)
    modify_file("file1v1.java")
    test_output=run_java_code()
    return test_output

>>>>>>> c387f21f024f13015ff452f548054d1d4427431a

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
    
<<<<<<< HEAD
=======
    #print(c2)
    #testing(c2)
>>>>>>> c387f21f024f13015ff452f548054d1d4427431a
    if testing(c1)==1:
        r=dict_union(r,c1)
    elif testing(c2)==1:
        r=dict_union(r,c2)

    if testing(c1) == 0:
<<<<<<< HEAD
        print(f"changes giving errors:\n............... {c1}...........................")
        return dd(c1, r)
    elif testing(c2) == 0:
        print(f"changes giving errors:\n............... {c2}...........................")
        return dd(c2, r)
    else:
        print(f"Both changes giving errors change1={c1} and change={c2} ")
=======
        return dd(c1, r)
    elif testing(c2) == 0:
        print("hello")
        return dd(c2, r)
    else:
>>>>>>> c387f21f024f13015ff452f548054d1d4427431a
        result1 = dd(c1, dict_union(c1,r))
        result2 = dd(c2, dict_union(c2,r))
        return dict_union(result1,result2)
    
    
def line_changes(diff, changes):
    global total_line_changes
    for change in changes:
        total_line_changes.append(change['line_number'])
    return total_line_changes


<<<<<<< HEAD
def replace_string_in_file(file_name, str1, str2):
    try:
        with open(file_name, 'r') as file:
            filedata = file.read()

        # Perform string replacement
        new_filedata = filedata.replace(str1, str2)

        with open(file_name, 'w') as file:
            file.write(new_filedata)


    except FileNotFoundError:
        print("File not found!")
    except IOError:
        print("Error reading/writing the file.")

=======
>>>>>>> c387f21f024f13015ff452f548054d1d4427431a
def main():
    Baseline, Configured= read_code_files()
    diff, changes=difference(Baseline, Configured)
    
<<<<<<< HEAD
    total_line_changes=line_changes(diff, changes)
    r=[]
    split_point = len(changes) // 2
    c1, c2 = changes[:split_point], changes[split_point:]
    minimum_set=dd(changes,r)
    
    
    print("\n\n\nHere we are getting the minimum set of changes\n")
=======
    #print(diff)
    '''print(diff)
    del diff[43]
    #print(len(diff))
    diff[43]="  }\n"
    print(diff)
    print(changes)'''
    total_line_changes=line_changes(diff, changes)
    r=[]
    #dd(changes,r)
    minimum_set=dd(changes,r)
    print(len(minimum_set))
>>>>>>> c387f21f024f13015ff452f548054d1d4427431a
    print(minimum_set)
    
    
if __name__ == "__main__":
    # Start the Java Virtual Machine (JVM).
    jpype.startJVM()
    main()
<<<<<<< HEAD
    # print(run_java_code())
=======
>>>>>>> c387f21f024f13015ff452f548054d1d4427431a
    # Stop the JVM.
    jpype.shutdownJVM()