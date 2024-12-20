import os
import subprocess
import sys
import locale
import boto3
from dotenv import load_dotenv

# UTF-8 설정
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 현재 로케일 확인
print(f"Current Locale: {locale.getpreferredencoding()}")

# .env 파일 로드
load_dotenv(r"C:\Users\User\Desktop\AWS\local_project\.env")

def validate_env_variables():
    """환경 변수 유효성 검사"""
    required_env_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "S3_BUCKET_NAME", "EXPORT_DIR"]
    for var in required_env_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"환경 변수 '{var}'가 설정되지 않았습니다.")

def run_localsql_script():
    """Shell 명령어로 localsql.py 실행"""
    localsql_path = r"C:\Users\User\Desktop\AWS\local_project\localsql.py"
    try:
        print("Executing localsql.py...")
        subprocess.run(["python", localsql_path], check=True)
        print("localsql.py executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error while executing localsql.py: {e}")
        raise

def upload_sql_to_s3():
    """로컬의 .sql 파일을 S3로 업로드"""
    export_dir = os.getenv("EXPORT_DIR")
    s3_bucket_name = os.getenv("S3_BUCKET_NAME")
    s3_directory = os.getenv("S3_DIRECTORY", "sql_backups/")

    # AWS S3 클라이언트 설정
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "ap-northeast-2")  # 리전 확인
    )

    print(f"Checking files in export directory: {export_dir}")
    try:
        for file_name in os.listdir(export_dir):
            if file_name.endswith(".sql"):
                local_file_path = os.path.join(export_dir, file_name)
                s3_path = os.path.join(s3_directory, file_name).replace("\\", "/")

                # S3 업로드
                print(f"Attempting to upload '{local_file_path}' to 's3://{s3_bucket_name}/{s3_path}'...")
                s3_client.upload_file(local_file_path, s3_bucket_name, s3_path)
                print(f"Successfully uploaded '{file_name}' to 's3://{s3_bucket_name}/{s3_path}'")

        print("SQL 파일 S3 업로드 완료!")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

if __name__ == "__main__":
    validate_env_variables()       # 환경 변수 확인
    run_localsql_script()          # Shell 명령어로 localsql 실행
    upload_sql_to_s3()             # S3 업로드
