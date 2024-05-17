import os
import boto3
import time
import sys

session = boto3.Session(profile_name = 'default')
s3 = session.client('s3')

def download(s3, bucket, obj, local_file_path):
    s3.download_file(bucket, obj, local_file_path)

def upload(s3, local_file_path, bucket, obj):
    s3.upload_file(local_file_path, bucket, obj)

def make_public_read(s3, bucket, key):
    s3.put_object_acl(ACL='public-read', Bucket = bucket, Key = key)


if __name__ == '__main__' :

    if len(sys.argv) != 6:
        print("Usage: python script.py <local_folder_path> <bucket_name> <s3_path> <publicOpt> <downOpt>")
        sys.exit(1)

    # 업로드할 파일 경로, 객체의 퍼블릭 설정 값, 다운로드 설정 값 변수 생성
    local_file_path = sys.argv[1]
    bucketname = sys.argv[2]
    s3path = sys.argv[3]
    publicOpt = int(sys.argv[4])
    downOpt = int(sys.argv[5])

    # s3에서 파일경로 변수생성 
    s3_file_path = s3path + os.path.basename(local_file_path)

        #업로드진행
    upload(s3, local_file_path, bucketname, s3_file_path)
    print("finish upload\n", "local_path: ", local_file_path, "\nbket_name: ", bucketname, "\ns3_path: ", s3_file_path, sep = '')
        
        #public 설정 값 확인 후 처리
    if publicOpt == 1:
            make_public_read(s3, bucketname, s3_file_path)

    #download설정 값 확인 후 처리
    if downOpt == 1:
        download(s3, bucketname, s3_file_path, local_file_path + 'copy')