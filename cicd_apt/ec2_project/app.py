import os
import boto3
import sys
import locale
import mysql.connector
import logging
from dotenv import load_dotenv

# UTF-8 설정
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 현재 로케일 확인
print(f"Current Locale: {locale.getpreferredencoding()}")

# .env 파일 로드
load_dotenv("/home/ec2-user/.env")

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger()

def download_sql_from_s3(local_path, file_name):
    """S3에서 SQL 파일 다운로드"""
    s3_bucket = os.getenv("S3_BUCKET_NAME")
    s3_directory = os.getenv("S3_DIRECTORY", "sql_backups/")
    s3_key = f"{s3_directory}{file_name}"

    # S3 클라이언트 설정
    s3_client = boto3.client("s3")
    logger.info(f"Downloading {s3_key} from S3 bucket {s3_bucket} to {local_path}...")
    s3_client.download_file(s3_bucket, s3_key, local_path)
    logger.info("S3 파일 다운로드 완료.")

def get_latest_time_from_rds(cursor):
    """RDS에서 최신 TIME 값 조회"""
    cursor.execute("SELECT MAX(TIME) FROM tb")  # 'TIME' 컬럼에서 최신 값 가져오기
    latest_time = cursor.fetchone()[0]
    logger.info(f"Latest TIME in RDS: {latest_time}")
    return latest_time

def filter_and_insert_sql(cursor, sql_file_path, latest_time):
    """SQL 파일에서 최신 값 이후 데이터를 필터링하고 삽입"""
    with open(sql_file_path, "r") as sql_file:
        sql_script = sql_file.read()
    
    for statement in sql_script.split(";"):
        statement = statement.strip()
        if statement.startswith("INSERT INTO") and "VALUES" in statement:
            # TIME 값을 추출 (예: INSERT INTO `tb` VALUES ('2024-12-18 14:06:25', ...))
            values_part = statement.split("VALUES")[1].strip(" ();")
            time_value = values_part.split(",")[0].strip(" '")

            # 최신 TIME 값 이후 데이터만 삽입
            if time_value > str(latest_time):  # 문자열 비교
                logger.info(f"Inserting new record with TIME: {time_value}")
                cursor.execute(statement)
            else:
                logger.info(f"Skipping duplicate or older record with TIME: {time_value}")

def import_sql_to_rds(sql_file_path):
    """SQL 파일을 RDS에 Import"""
    rds_host = os.getenv("RDS_HOST")
    rds_user = os.getenv("RDS_USERNAME")
    rds_password = os.getenv("RDS_PASSWORD")
    rds_database = os.getenv("RDS_DATABASE")

    try:
        logger.info("Connecting to RDS...")
        conn = mysql.connector.connect(
            host=rds_host,
            user=rds_user,
            password=rds_password,
            database=rds_database
        )
        cursor = conn.cursor()

        # RDS에서 최신 TIME 값 가져오기
        latest_time = get_latest_time_from_rds(cursor)

        # SQL 파일에서 최신 데이터 이후만 삽입
        filter_and_insert_sql(cursor, sql_file_path, latest_time)

        # 커밋
        conn.commit()
        logger.info("SQL 데이터 Import 성공!")
    except mysql.connector.Error as e:
        logger.error(f"RDS Import 오류: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()

def get_latest_sql_file_from_s3():
    """S3에서 최신 SQL 파일의 이름 반환"""
    s3_bucket = os.getenv("S3_BUCKET_NAME")
    s3_directory = os.getenv("S3_DIRECTORY", "sql_backups/")

    # S3 클라이언트 설정
    s3_client = boto3.client("s3")
    logger.info(f"Fetching latest file from S3 bucket {s3_bucket} in directory {s3_directory}...")

    # S3 객체 리스트 가져오기
    response = s3_client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_directory)

    if "Contents" not in response or not response["Contents"]:
        raise FileNotFoundError(f"S3 경로 {s3_directory}에 SQL 파일이 없습니다.")

    # 가장 최신 파일 찾기
    files = response["Contents"]
    latest_file = max(files, key=lambda x: x["LastModified"])
    logger.info(f"Latest file in S3: {latest_file['Key']}")
    return os.path.basename(latest_file["Key"])

if __name__ == "__main__":
    try:
        # S3에서 최신 SQL 파일 가져오기
        file_name = get_latest_sql_file_from_s3()
        local_sql_path = f"/tmp/{file_name}"

        logger.info(f"Processing file: {file_name}")

        # S3에서 SQL 파일 다운로드 및 RDS Import
        download_sql_from_s3(local_sql_path, file_name)
        import_sql_to_rds(local_sql_path)

    except Exception as e:
        logger.error(f"오류 발생: {e}")
