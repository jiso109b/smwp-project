import os
import subprocess
import sys
import locale
import logging
from dotenv import load_dotenv

# UTF-8 설정
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 현재 로케일 확인
print(f"Current Locale: {locale.getpreferredencoding()}")

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# .env 파일 로드
load_dotenv()

# EC2_SSH 명령 가져오기
ssh_command = os.getenv("EC2_SSH")

if ssh_command:
    try:
        # 명령어 정의
        full_command = f'{ssh_command} "source ~/.bashrc && python3 /home/ec2-user/app.py"'
        logger.info(f"Executing command: {full_command}")
        
        # 명령 실행
        result = subprocess.run(
            full_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 출력 로그
        if result.stdout:
            logger.info("EC2 Output:")
            logger.info(result.stdout.decode())
        if result.stderr:
            logger.error("EC2 Error:")
            logger.error(result.stderr.decode())
    except Exception as e:
        logger.error(f"Error executing EC2 SSH command: {e}")
else:
    logger.error("EC2_SSH environment variable not found in .env file.")
