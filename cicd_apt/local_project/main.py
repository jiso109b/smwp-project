import subprocess
import os
from dotenv import load_dotenv
import sys
import locale
import schedule
import time

# UTF-8 설정
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 현재 로케일 확인
print(f"Current Locale: {locale.getpreferredencoding()}")

# .env 파일 로드
load_dotenv(r"C:\Users\User\Desktop\AWS\local_project\.env")

def run_script(script_path):
    """지정된 Python 스크립트를 실행"""
    python_executable = os.getenv("LOCAL_PYTHON", "python")  # 로컬 Python 경로 가져오기, 없으면 기본 python 사용
    try:
        print(f"Running {script_path} with {python_executable}...")
        subprocess.run([python_executable, script_path], check=True)
        print(f"{script_path} executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_path}: {e}")
        raise

def main():
    """Main Workflow"""
    print("\nStarting Main Workflow...")

    try:
        # Step 1: localsql.py 실행
        run_script(r"C:\Users\User\Desktop\AWS\local_project\localsql.py")

        # Step 2: preprocess.py 실행
        run_script(r"C:\Users\User\Desktop\AWS\local_project\preprocess.py")

        # Step 3: app.py 실행
        run_script(r"C:\Users\User\Desktop\AWS\local_project\app.py")

        print("\nWorkflow completed successfully!")
    except Exception as e:
        print(f"\nWorkflow failed: {e}")

# 스케줄링 설정
print("\nInitializing Scheduler...")
schedule.every(45).seconds.do(main)  # 45초마다 main() 실행

# 스케줄 실행 루프
if __name__ == "__main__":
    print("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()  # 예약된 작업 실행
        time.sleep(1)  # 1초 대