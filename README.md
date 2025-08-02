# 🔍 Web Security Toolkit (SQLi + XSS)

A dual-toolkit for penetration testers to detect and analyze:
- SQL Injection (SQLi) vulnerabilities
- Cross-Site Scripting (XSS) vulnerabilities (Reflected, DOM, Custom Payload)

---

## 📦 Tools Included

### 1. SQL Injection Scanner (based on `sqlmap`)

Powerful wrapper around `sqlmap` with enhanced CLI interface.

#### 🔹 Features:
- Full site scan with detection of DBMS & WAF
- Dump all databases and sensitive fields (emails, passwords)
- Try OS-Shell access
- Read arbitrary server files
- Extract DBMS login credentials
- Colored output (green = success, red = error)

#### ▶️ How to Use

```bash
python sql_tool.py

Then follow the prompt:

[+] Enter Target URL
[+] Choose Option:
    [1] Full Website Scan
    [2] Dump All Databases
    [3] Dump Users and Passwords
    [4] Open OS Shell
    [5] Read Server File
    [6] Extract DBMS Passwords
    [0] Exit

> ⚠️ Note: Requires sqlmap to be installed and accessible in your system PATH.




---

2. XSS Scanner

Custom XSS scanner for:

Reflected XSS

DOM-based XSS detection

Custom payload injection


🔹 Features:

Injects multiple known XSS payloads

Detects DOM-based vulnerable JavaScript patterns

Accepts and tests your own payloads

Clean console output using rich

Color-coded: green = vulnerable, red = safe/error


▶️ How to Use

python xss_tool.py

Then follow the prompt:

[+] Enter URL
[1] Reflected XSS
[2] DOM XSS
[3] Custom Payload
[0] Exit


---

📁 Requirements

Install dependencies using:

pip install -r requirements.txt

✅ Minimal requirements.txt:

rich
requests

💡 Optional (for advanced performance):

httpx
tqdm
lxml
beautifulsoup4
playwright


---

⚠️ Disclaimer

This toolkit is intended for educational purposes and authorized security testing only.
Do not scan or attack any system or website without explicit permission.
The author is not responsible for any misuse or illegal activity.


---

📫 Author

Made with purpose for learning and ethical testing.
Modify, fork, and expand as needed.

