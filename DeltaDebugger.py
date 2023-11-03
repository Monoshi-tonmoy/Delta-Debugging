import difflib
import subprocess

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


def run_java():
    with open("input.txt", 'r') as input_file:
        input_data = input_file.read().strip()
    input_args=input_data.split()
    a = int(input_args[0])
    b = int(input_args[1])
    print(f"a:{a}, b:{b}, string:{input_args[2]}")
    java_command = [
        'C:\\Program Files\\Java\\jdk-21\\bin\\java.exe',
        'file1v1',
        str(a), 
        str(b),
        input_args[2] 
    ]

    process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(process.communicate())
    stdout, stderr = process.communicate()

    if stderr:
        print("Error:", stderr)
        return 0
    else:
        print("Program ran successfully", stdout)
        return 1




def testing(changes):
    global total_line_changes
    global diff
    print(total_line_changes)
    print(diff)
    
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
    
    subprocess.run(["C:\\Program Files\\Java\\jdk-21\\bin\\javac.exe", "file1v1.java"])
    test_output=run_java()
    
    print(test_output)
    


def dd(changes):
    if len(changes) == 1:
        return [changes[0]]

    split_point = len(changes) // 2
    c1, c2 = changes[:split_point], changes[split_point:]

    testing(changes)
    '''if testing(diff, c1):
        pass
        return dd(c2)
    elif testing(diff, c2):
        pass
        return dd(diff,c1,total_line_changes)
    else:
        # If both subsets fail, try interference by merging results
        result1 = dd(diff,c1 + c2,total_line_changes)
        result2 = dd(diff, c2 + c1, total_line_changes)
        return result1 + result2'''

def line_changes(diff, changes):
    global total_line_changes

    for change in changes:
        total_line_changes.append(change['line_number'])
    
    return total_line_changes    

    
def main():
    Baseline, Configured= read_code_files()
    diff, changes=difference(Baseline, Configured)
    total_line_changes=line_changes(diff, changes)
    dd(changes)
    #print(changes)

if __name__ == "__main__":
    main()