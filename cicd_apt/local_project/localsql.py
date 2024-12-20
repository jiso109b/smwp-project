import os
import mysql.connector
import re
import sys
import locale
from dotenv import load_dotenv

# UTF-8 설정
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 현재 로케일 확인
print(f"Current Locale: {locale.getpreferredencoding()}")

# .env 파일 로드
load_dotenv(r"C:\Users\User\Desktop\AWS\local_project\.env")

def get_latest_time_from_file(file_path):
    """SQL 파일에서 최신 TIME 값 추출"""
    latest_time = None
    time_pattern = re.compile(r"INSERT INTO .* VALUES \('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = time_pattern.search(line)
                if match:
                    current_time = match.group(1)
                    if not latest_time or current_time > latest_time:
                        latest_time = current_time
        print(f"Latest TIME from file '{file_path}': {latest_time}")
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Fetching all data.")
    return latest_time

def export_mysql_data():
    """MySQL 데이터베이스를 덤프하여 .sql 파일로 저장"""

    # .env 파일에서 로컬 DB 정보 불러오기
    local_db_host = os.getenv("LOCAL_DB_HOST")
    local_db_name = os.getenv("LOCAL_DB_NAME")
    local_db_user = os.getenv("LOCAL_DB_USER")
    local_db_password = os.getenv("LOCAL_DB_PASSWORD")

    # 덤프 파일을 저장할 경로
    export_dir = r"C:\Users\User\Desktop\AWS\local_project\rawDB"  # 절대 경로 설정
    os.makedirs(export_dir, exist_ok=True)

    try:
        # MySQL 연결
        conn = mysql.connector.connect(
            host=local_db_host,
            user=local_db_user,
            password=local_db_password,
            database=local_db_name
        )
        cursor = conn.cursor()

        # 테이블 덤프
        table_name = "tb"  # 특정 테이블 이름 (예시)
        output_file = os.path.join(export_dir, f"{table_name}.sql")
        print(f"Exporting table '{table_name}' to '{output_file}'...")

        # 기존 파일에서 최신 TIME 값 가져오기
        latest_time = get_latest_time_from_file(output_file)

        # SQL 쿼리 생성
        if latest_time:
            query = f"SELECT * FROM {table_name} WHERE TIME >= '{latest_time}' ORDER BY TIME ASC"
            print(f"Fetching data with TIME >= '{latest_time}'...")
        else:
            query = f"SELECT * FROM {table_name} ORDER BY TIME ASC"
            print(f"Fetching all data...")

        cursor.execute(query)
        rows = cursor.fetchall()

        # 데이터를 .sql 파일로 저장 (추가 모드)
        with open(output_file, "a", encoding="utf-8") as f:
            existing_data = set()  # 중복 제거를 위한 집합
            if os.path.exists(output_file):
                with open(output_file, "r", encoding="utf-8") as existing_file:
                    for line in existing_file:
                        existing_data.add(line.strip())

            for row in rows:
                row_data = ", ".join(
                    ["'{}'".format(str(item).replace("'", "\\'")) if item is not None else "NULL" for item in row]
                )
                insert_statement = f"INSERT INTO `{table_name}` VALUES ({row_data});"

                # 중복 방지: 기존 데이터에 없으면 추가
                if insert_statement.strip() not in existing_data:
                    f.write(f"{insert_statement}\n")

        print("MySQL 데이터 덤프 성공!")

    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        # 커서 및 연결 종료
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    export_mysql_data()  # MySQL 덤프 실행
