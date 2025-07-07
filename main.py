import sys
import os

tunnelid = "QXJ4ZGdoU0ZyZXNzb29qTVJncWxreWJXVmE5Z3JrMWQ="
system_os = "Ubuntu 24.4 LTS (Long Term Support)"
kernel = "Linux plinux_6.8"
whoami = "root"
cwd = "/home/root"

fs = {
    "/home": ["root"],
    "/home/root": ["file.txt", "docs", "secrets"],
    "/home/root/docs": [],
    "/home/root/secrets": ["top_secret.txt"]
}

print("\U0001F512 Welcome to PLinux Tunnel CLI")
tunnel = input("Enter your session tunnel ID: ")
if tunnel != tunnelid:
    print("\u274C Tunnel ID don't match!")
    sys.exit()

print(f"\u2705 Tunnel match success. Welcome {whoami}!\nType 'help' for command list.")

def list_dir(path):
    return fs.get(path, [])

def change_dir(current, new_path):
    if new_path == "..":
        return os.path.dirname(current) if current != "/" else "/"
    elif new_path.startswith("/"):
        return new_path if new_path in fs else current
    else:
        temp_path = os.path.join(current, new_path)
        return temp_path if temp_path in fs else current

while True:
    cmd = input(f"{whoami}@plinux:{cwd}# ").strip()

    if cmd.lower() == "exit":
        print("\U0001F44B Quitting PLinux...")
        break

    elif cmd == "help":
        print("""Available Commands:
  whoami
  uname -r
  uname -a
  tunnel --show
  pwd
  ls
  cd [dir]
  mkdir [dir]
  rmdir [dir]
  touch [file]
  cp [src] [dst]
  mv [src] [dst]
  rm [file]
  chmod +x [file]
  chmod -x [file]
  clear
  echo [text]
  cat [file]
  neofetch
  ping [host]
  ifconfig / ip a
  history
  run [script.sh]
  ptpkg install [pkg]
  ptpkg remove [pkg]
  sudo apt-get update
  exit
""")

    elif cmd == "whoami":
        print(whoami)

    elif cmd == "uname -r":
        print(kernel)

    elif cmd == "uname -a":
        print(f"{kernel} {system_os} #1 SMP")

    elif cmd == "tunnel --show":
        print(tunnelid)

    elif cmd == "pwd":
        print(cwd)

    elif cmd == "ls":
        files = list_dir(cwd)
        print("  ".join(files) if files else "")

    elif cmd.startswith("cd "):
        path = cmd[3:]
        new_dir = change_dir(cwd, path)
        if new_dir == cwd:
            print("No such directory")
        else:
            cwd = new_dir

    elif cmd.startswith("mkdir "):
        dir_name = cmd[6:]
        new_path = os.path.join(cwd, dir_name)
        if new_path not in fs:
            fs[new_path] = []
            fs[cwd].append(dir_name)
            print(f"Directory '{dir_name}' created.")
        else:
            print("Directory already exists.")

    elif cmd.startswith("rmdir "):
        dir_name = cmd[6:]
        full_path = os.path.join(cwd, dir_name)
        if full_path in fs and not fs[full_path]:
            fs.pop(full_path)
            if dir_name in fs[cwd]:
                fs[cwd].remove(dir_name)
            print(f"Directory '{dir_name}' removed.")
        else:
            print("Directory not empty or does not exist.")

    elif cmd.startswith("touch "):
        file_name = cmd[6:]
        if file_name not in fs.get(cwd, []):
            fs[cwd].append(file_name)
            print(f"File '{file_name}' created.")
        else:
            print("File already exists.")

    elif cmd.startswith("cp "):
        parts = cmd.split()
        if len(parts) == 3:
            src, dest = parts[1], parts[2]
            if src in fs.get(cwd, []):
                fs[cwd].append(dest)
                print(f"'{src}' copied to '{dest}'.")
            else:
                print("Source file not found.")
        else:
            print("Usage: cp [source] [destination]")

    elif cmd.startswith("mv "):
        parts = cmd.split()
        if len(parts) == 3:
            src, dest = parts[1], parts[2]
            if src in fs.get(cwd, []):
                fs[cwd].remove(src)
                fs[cwd].append(dest)
                print(f"'{src}' moved/renamed to '{dest}'.")
            else:
                print("Source file not found.")
        else:
            print("Usage: mv [source] [destination]")

    elif cmd.startswith("rm "):
        file_name = cmd[3:]
        if file_name in fs.get(cwd, []):
            fs[cwd].remove(file_name)
            print(f"'{file_name}' removed.")
        else:
            print("File not found.")

    elif cmd.startswith("chmod +x "):
        file = cmd[9:]
        if file in fs.get(cwd, []):
            print(f"Execute permission given to '{file}'.")
        else:
            print("File not found.")

    elif cmd.startswith("chmod -x "):
        file = cmd[9:]
        if file in fs.get(cwd, []):
            print(f"Execute permission removed from '{file}'.")
        else:
            print("File not found.")

    elif cmd == "clear":
        os.system("cls" if os.name == "nt" else "clear")

    elif cmd.startswith("echo "):
        print(cmd[5:])

    elif cmd.startswith("cat "):
        file_name = cmd[4:]
        if file_name in fs.get(cwd, []):
            print(f"Showing contents of '{file_name}' (simulated)...")
        else:
            print("File not found.")

    elif cmd == "neofetch":
        print(f"""
            ██████╗ ██╗     ██╗███╗   ██╗██╗   ██╗██╗   ██╗
            ██╔══██╗██║     ██║████╗  ██║██║   ██║╚██╗ ██╔╝
            ██████╔╝██║     ██║██╔██╗ ██║██║   ██║ ╚████╔╝ 
            ██╔═══╝ ██║     ██║██║╚██╗██║██║   ██║  ╚██╔╝  
            ██║     ███████╗██║██║ ╚████║╚██████╔╝   ██║   
            ╚═╝     ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝    ╚═╝   
        """)
        print(f"OS: {system_os}")
        print(f"Kernel: {kernel}")
        print(f"User: {whoami}")
        print(f"Tunnel: {tunnelid[:8]}...")

    elif cmd.startswith("ping "):
        host = cmd[5:]
        print(f"Pinging {host} with 32 bytes of data:")
        for i in range(4):
            print(f"Reply from {host}: bytes=32 time=1ms TTL=64")
        print("Ping complete.")

    elif cmd == "ifconfig" or cmd == "ip a":
        print("eth0: inet 192.168.56.101 netmask 255.255.255.0 broadcast 192.168.56.255")
        print("lo: inet 127.0.0.1")

    elif cmd == "history":
        print("Command history not saved in this simulation.")

    elif cmd.startswith("run "):
        script = cmd[4:]
        print(f"Executing script: {script} (simulated)...")
        print("Script completed.")

    elif cmd.startswith("ptpkg install "):
        pkg = cmd[15:]
        print(f"Installing {pkg} from PLinux Package Repository (simulated)...")
        print(f"Package {pkg} installed.")

    elif cmd.startswith("ptpkg remove "):
        pkg = cmd[14:]
        print(f"Removing {pkg} from PLinux Package Repository (simulated)...")
        print(f"Package {pkg} removed.")

    elif cmd == "sudo apt-get update":
        print("\U0001F6AB APT commands are blocked in PLinux Tunnel environment.")

    else:
        print(f"Command not found: {cmd}")
