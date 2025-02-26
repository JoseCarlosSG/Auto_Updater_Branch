import os
import re
import sys
import subprocess

def execute_command(command):
    """Executes a shell command and returns its output and status."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def find_class_and_save(file_path, class_name, identifier):
    """Finds and saves the specified class from the file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        class_start = None
        class_end = None

        if identifier:
            # Find identifier position
            id_pattern = re.compile(rf"'''{re.escape(identifier)}'''")
            for i, line in enumerate(lines):
                if id_pattern.search(line):
                    class_start = max(i - 2, 0)  # The class is two lines above
                    break
        else:
            # If no identifier, assume class is at the end
            class_start = len(lines) - 1
        
        # Find where the class ends (next class or EOF)
        if class_start is not None:
            for i in range(class_start, len(lines)):
                if lines[i].startswith("class ") and i != class_start:
                    class_end = i
                    break
            class_end = class_end if class_end else len(lines)  # If no new class found, take EOF

        class_content = lines[class_start:class_end]

        # Save class to a separate file
        backup_file = f"{class_name}_backup.py"
        with open(backup_file, "w", encoding="utf-8") as file:
            file.writelines(class_content)
        
        print(f"Class '{class_name}' saved to {backup_file}")
        return True

    except Exception as e:
        print(f"Error processing file: {e}")
        return False

def update_branch(branch_name):
    """Performs git pull, resolves conflicts by keeping master changes, and pushes the branch."""
    print("Fetching latest changes from master...")
    stdout, stderr, code = execute_command("git pull origin master")

    if code == 0:
        print(f"Branch '{branch_name}' updated successfully.")
        execute_command(f'git commit -m "{branch_name}: Updating branch"')
    else:
        print("Merge conflicts detected. Resolving...")
        execute_command("git checkout --theirs .")  # Keep master changes
        execute_command("git add .")
        execute_command(f'git commit -am "{branch_name}: Updating branch"')
    
    print("Pushing changes...")
    execute_command("git push")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <class_name> <file_path> <branch_name> [identifier]")
        sys.exit(1)

    class_name = sys.argv[1]
    file_path = sys.argv[2]
    branch_name = sys.argv[3]
    identifier = sys.argv[4] if len(sys.argv) > 4 else None

    if find_class_and_save(file_path, class_name, identifier):
        update_branch(branch_name)
