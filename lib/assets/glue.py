import sys
import boto3
from pathcheck import is_targetpath, translated_path
from awsglue.utils import getResolvedOptions
import logging
#from hello import hello_print

## @params: [JOB_NAME]
#args = getResolvedOptions(sys.argv, ['BUCKET'])
args = getResolvedOptions(sys.argv, ['BUCKET', 'KEY', 'SECRET'])
TARGET_BUCKET = 'upload-pisakun-bucket'
s3 = boto3.resource('s3', aws_access_key_id=args['KEY'], aws_secret_access_key=args['SECRET'])

#s3 = boto3.resource('s3')
def get_all_objects_high(bucket):
    bucket = s3.Bucket(bucket)
    return bucket.objects.all()

logger = logging.getLogger()
objs = get_all_objects_high(TARGET_BUCKET)
for i,obj in enumerate(iter(objs)):
    print(f'{i}: {obj.key}')
    if is_targetpath(obj.key) is False:
        logger.error(f'{obj.key} this is not targetpath')
        continue
    result, paths = translated_path(obj.key)
    print(result)
    if result is False:
        continue
    print(paths.dest, paths.moved, paths.error)
    ## 変換処理

    copy_source = {'Bucket': TARGET_BUCKET, 'Key': obj.key}
    s3.meta.client.copy(copy_source, TARGET_BUCKET, paths.dest)
    s3.meta.client.copy(copy_source, TARGET_BUCKET, paths.moved)
    # 削除処理
    s3obj = s3.Object(TARGET_BUCKET, obj.key)
    s3obj.delete()
    print(f'{obj.key}処理終了')
## call library
#hello_print()