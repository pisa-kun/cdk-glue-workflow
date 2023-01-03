# Welcome to your CDK TypeScript project
[glue-workflow](https://blog.serverworks.co.jp/run-glue-workflow-when-the-files-is-reached)


---

### glue workflow sample

https://github.com/aws-samples/glue-workflow-aws-cdk/blob/main/lib/blog-glue-workflow-stack.ts


### glue schedule

https://dev.classmethod.jp/articles/what-to-do-when-aws-glue-trigger-does-not-start-automatically/

```py
    const cfnTrigger = new CfnTrigger(this, `${this.stackName}-Trigger`, {
      name: `${this.stackName}-Trigger`,
      workflowName: glueWorkflow.name,
      type: 'SCHEDULED',
      startOnCreation: true,
      schedule: "cron(0 4 * * ? *)",
```

スケジュール時はstartoncreationをtrueにする必要がある
https://dev.classmethod.jp/articles/what-to-do-when-aws-glue-trigger-does-not-start-automatically/

### pyspark job commit

https://github.com/aws-samples/glue-workflow-aws-cdk/blob/main/lib/assets/glue-parquet-etl.py


https://docs.aws.amazon.com/ja_jp/glue/latest/dg/monitor-continuations.html
> AWS Glue ではジョブの実行による状態情報を保持することで、ETL ジョブの以前の実行中にすでに処理されたデータを追跡します。この継続状態の情報はジョブのブックマークと呼ばれています。ジョブのブックマークは、AWS Glue で状態情報を保持して、古いデータを再処理しないために役立ちます。ジョブのブックマークを使用すると、スケジュールされた間隔で再実行する際に新しいデータを処理できます。ジョブのブックマークは、ソース、変換、ターゲットなど、さまざまなジョブの要素で構成されています。例えば、ETL ジョブが Amazon S3 ファイルで新しいパーティションを読み込むとします。AWS Glue は、そのジョブにより正常に処理されたのはどのパーティションなのかを追跡し、処理の重複およびジョブのターゲットデータストアにデータが重複するのを防ぎます。

```py
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
// job名に対してBOOKMARK
job.init(job_args['JOB_NAME'], job_args)

//
// 変換処理
//
//

// BOOKMARKに追記
job.commit()
```

#### 失敗時に通知発信
- job 失敗イベントを受け取る
https://dev.classmethod.jp/articles/glue_job_err_notification/

```json
{
  "source": [
    "aws.glue"
  ],
  "detail-type": [
    "Glue Job State Change"
  ],
  "detail": {
    "jobName": [
      "glue-job-for-err-notification"
    ],
    "state": [
      "FAILED"
    ]
  }
}
```

**jobName**なので注意、Nが大文字

new events.Rule
https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_events-readme.html


#### Error: spawnSync docker ENOENT
> npm install --save-dev aws-sdk
> $ npm install --save-dev esbuild@0
>
> https://qiita.com/derodero24/items/a0b05ef026f63fca8f03
>

#### yamlの読み込み
https://kakehashi-dev.hatenablog.com/entry/2021/12/20/080000

npm install --save js-yaml
npm install -D @types/js-yaml

```yaml
dev:
  region: ap-northeast-1
  id: 00000000000
  email: hogehoge@gmail.com

stg:
  region: ap-northeast-2
  id: 00000000000
  email: hogehoge@gmail.com
```

#### node-ts
> node .\node_modules\ts-node\dist\bin.js .\env\environment.ts  

- Best
> npx ts-node .\env\environment.ts

https://www.wakuwakubank.com/posts/726-typescript-ts-node/

#### Send SNS from Lambda

https://medium.com/@shimo164/cdk-send-amazon-sns-from-aws-lambda-1a0e6c86073e

```typescript
    // 1. Set SNS Topic
    // 1-1 Use existing SNS topic: Hard code the topic arn
    const myTopic = sns.Topic.fromTopicArn(this, 'MyTopic', <topic-arn>);
```

#### add EventNotify to s3

https://bobbyhadz.com/blog/aws-cdk-s3-bucket-event-notifications

```typescript
    const topic = new sns.Topic(this, 'sns-topic');

    s3Bucket.addEventNotification(
      s3.EventType.REDUCED_REDUNDANCY_LOST_OBJECT,
      new s3n.SnsDestination(topic),
      // 👇 only send message to topic if object matches the filter
      // {prefix: 'test/', suffix: '.png'},
    );
```

#### create sqs from ARN
https://bobbyhadz.com/blog/aws-cdk-sqs-sns-lambda
```ts
const sqs = cdk.aws_sqs.Queue.fromQueueArn(this, 'snowflake sqs', <ARN>);
```

- sqsEventをlambdaで受け取って処理するために
https://bobbyhadz.com/blog/aws-cdk-sqs-sns-lambda

> npm i --save-dev aws-lambda @types/aws-lambda

**SQS自身にも**Action:Sqsを追加する必要がある(SQSのアクセスポリシーも追加する必要あり・・・？)

#### s3bucket destination error

> An error occurred (InvalidArgument) when calling the PutBucketNotificationConfiguration operation: Unable to validate the following destination configurations
