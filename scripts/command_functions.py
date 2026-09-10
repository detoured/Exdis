import subprocess

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

def create_shell():
    shell = subprocess.Popen(
    ["/bin/bash"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=True
    )
    
    return shell


    