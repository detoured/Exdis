import subprocess
import sys
async def run_command(message, id, shells):
        command = message.content + "\necho __EXDIS_COMMAND_DONE__\n"

        shells[id].stdin.write(command.encode())
        shells[id].stdin.flush()

        output = []

        while True:
            line = shells[id].stdout.readline()

            if not line:
                break

            if line.strip() == b"__EXDIS_COMMAND_DONE__":
                break

            output.append(line)

        result = b"".join(output)
        if result:
            await message.channel.send(f"```{result.decode('utf-8').replace("```","``")}```")
        else:
            await message.add_reaction("✅")

def find_shell_type():
        linux = ["echo", "$SHELL"]
        windows = ["echo", "%ComSpec%"]
        linux_shell = execute_echo_shell(linux)
        windows_shell = execute_echo_shell(windows)

        if linux_shell != None:
            return linux_shell
        if windows_shell != None:
            return windows_shell

        #shell not found
        sys.exit(1)
        

def execute_echo_shell(command):
    echo_arg = command[1]
    result = subprocess.run(" ".join(command), shell=True,capture_output=True)
    clean_output = str((result.stdout).decode("utf-8")).strip()
    if clean_output != echo_arg:
        return [clean_output]
    return None

    

def create_shell(shell_path):
    shell = subprocess.Popen(
    shell_path,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=True
    )
    
    return shell


    