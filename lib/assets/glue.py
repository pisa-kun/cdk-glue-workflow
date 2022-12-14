import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])


# ジョブ初期化
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


# from_options関数でcSV読み込み
dynamic_frame = glueContext.create_dynamic_frame.from_options(connection_type = "s3",
                                                              connection_options = {"paths": [ "s3://cdkglueworkflowstack-s3/in/sample.csv"]},
                                                              format="csv",
                                                              format_options={"withHeader": True})

# データの情報を表示
print('Count: {0}'.format(dynamic_frame.count()))
dynamic_frame.printSchema()

# データの中身を表示
dynamic_frame.show(dynamic_frame.count())


# Parquet変換して書き込み
data_frame = dynamic_frame.toDF()

## snappy
data_frame.write.mode("overwrite").format("parquet").option("compression", "snappy").save("s3://cdkglueworkflowstack-s3/out/sample.snappy.parquet")


# ジョブコミット
job.commit()