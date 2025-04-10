import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수 불러오기
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "ap-northeast-2")
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_STORAGE_OVERRIDE = os.getenv("AWS_STORAGE_OVERRIDE", "false").lower() == "true"

def upload_to_s3():
    # 업로드할 파일과 S3 키 설정
    file_name = './from_bucket.png' # 우리의 local 디렉토리에 있는 파일명
    key = 'from_local_profile.png' # key로 올리겠다

    # S3 클라이언트 생성
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

    # 파일 존재 확인
    if not os.path.exists(file_name):
        print(f"업로드할 파일을 찾을 수 없습니다: {file_name}")
        return False

    # 덮어쓰기 여부 확인
    if not AWS_STORAGE_OVERRIDE:
        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=key)
            print(f"파일이 이미 S3에 존재합니다: s3://{BUCKET_NAME}/{key}")
            print("업로드를 중단합니다 (덮어쓰기 비허용).")
            return False
        except ClientError as e:
            if e.response["Error"]["Code"] != "404":
                print(f"오류 발생: {e}")
                return False
            # 파일이 없으면 계속 진행

    # 업로드 시도
    try:
        s3.upload_file(file_name, BUCKET_NAME, key)
        print(f"업로드 성공: s3://{BUCKET_NAME}/{key}")
        return True
    except Exception as e:
        print(f"업로드 중 오류 발생: {e}")
        return False

# 단독 실행 시 동작
if __name__ == "__main__":
    result = upload_to_s3()
    if not result:
        print("파일 업로드 실패")
