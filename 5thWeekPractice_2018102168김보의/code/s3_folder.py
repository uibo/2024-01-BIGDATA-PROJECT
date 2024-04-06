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

bucketname = "bucketforadvanced"
s3path = "test/"

if __name__ == '__main__' :
    # 업로드할 컨텐츠가 들어있는 폴더 경로, 객체의 퍼블릭 설정 값, 다운로드 설정 값 변수 생성
    local_folder_path = sys.argv[1] + '/'
    publicOpt = int(sys.argv[2])
    downOpt = int(sys.argv[3])

    #폴더 내에 파일이름을 한번씩 가져옴
    for file_name in os.listdir(local_folder_path):
        #파일이름, 로컬컴퓨터에서 파일경로, s3에서 파일경로/이름 변수생성 
        local_file_path = os.path.join(local_folder_path, file_name)
        s3path_filename = s3path + file_name

        #업로드진행
        upload(s3, local_file_path, bucketname, s3path_filename)
        print("finish upload ", "local_path=", local_file_path, ", bket_name=", bucketname, ", s3_path", s3path_filename)
        
        #public 설정 값 확인 후 처리
        if publicOpt == 1:
            make_public_read(s3, bucketname, s3path_filename)

        #download설정 값 확인 후 처리
        if downOpt == 1:
            download(s3, bucketname, s3path_filename, local_file_path + 'roms3')