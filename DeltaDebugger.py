import difflib
import subprocess
import jpype
total_line_changes=[]
diff=[]
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
def run_java_code():
    # Compile the Java file.
    subprocess.run(["javac", "file1v1.java"])
    # Get the Java class object for the Java file.
    java_class = jpype.JClass("file1v1")
    # Create an instance of the Java class.
    java_instance = java_class()
    # Call the `fun()` method on the Java instance, passing in the three input arguments.
    try:
        java_instance.fun(2, 0, "division")
        result = 1
    except Exception as e:
        print(e)
        result = 0
    return result
def testing(changes):
    global total_line_changes
    global diff
    print(total_line_changes)
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
            new_code.append(diff[i][2:])
        elif i in rest and diff[i].startswith('+ '):
            continue
        elif diff[i].startswith('? '):
            continue
        else:
            new_code.append(diff[i][2:])
    modified_code = '\n'.join(new_code)
    with open("file1v1.java",'w',encoding='utf-8') as file:
        file.write(modified_code)
    test_output=run_java_code()
    return test_output
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
    if testing(c1)==1 or testing(c2)==1:
        if testing(c1):
            r=dict_union(r,c1)
        else:
            r=dict_union(r,c2)
    if testing(c1) == 0:
        return dd(c1, r)
    elif testing(c2) == 0:
        return dd(c2, r)
    else:
        result1 = dd(c1, c2 + r)
        result2 = dd(c2, c1 + r)
        return result1 + result2
def line_changes(diff, changes):
    global total_line_changes
    for change in changes:
        total_line_changes.append(change['line_number'])
    return total_line_changes
def main():
    Baseline, Configured= read_code_files()
    diff, changes=difference(Baseline, Configured)
    print(changes)
    total_line_changes=line_changes(diff, changes)
    r=[]
    dd(changes,r)
if __name__ == "__main__":
    # Start the Java Virtual Machine (JVM).
    jpype.startJVM()
    main()
    # Stop the JVM.
    jpype.shutdownJVM()