import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Bucket, EventType } from 'aws-cdk-lib/aws-s3';
import {  Rule } from 'aws-cdk-lib/aws-events';
import { LambdaFunction, SnsTopic } from 'aws-cdk-lib/aws-events-targets';
import { CfnTrigger, CfnWorkflow } from 'aws-cdk-lib/aws-glue';
import { ManagedPolicy, PolicyStatement } from 'aws-cdk-lib/aws-iam';
import { BucketDeployment, Source } from 'aws-cdk-lib/aws-s3-deployment';
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';
import { Environment } from '../env/environment';
import { Topic } from 'aws-cdk-lib/aws-sns';
import { EmailSubscription, SqsSubscription } from 'aws-cdk-lib/aws-sns-subscriptions';
import { Code, Function, Runtime } from 'aws-cdk-lib/aws-lambda';
import { SnsDestination } from 'aws-cdk-lib/aws-s3-notifications';
import { Queue } from 'aws-cdk-lib/aws-sqs';
import * as path from 'path';
import { SqsEventSource } from 'aws-cdk-lib/aws-lambda-event-sources';

export class CdkGlueWorkflowStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const env = new Environment('dev');

    // create Glue workflow
    //https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_glue.CfnWorkflow.html
    const glueWorkflow = new CfnWorkflow(this, `${this.stackName}-glue-workflow`, {
      description: 'sample work flow',
      name: `${this.stackName}-workflow`
    });

    // create s3 bucket
    // https://zenn.dev/nmemoto/articles/s3-eventnotification-with-eventbridge
    const s3Bucket = new Bucket(this, `${this.stackName}-s3`, {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      eventBridgeEnabled: true,
      bucketName: `${(this.stackName).toLowerCase()}-s3`,
    });

    const role = new cdk.aws_iam.Role(this, "access-glue-job", {
      assumedBy: new cdk.aws_iam.ServicePrincipal('glue.amazonaws.com'),
      description: "glue job attach role"
    });
    
    // Add AWSGlueServiceRole to role.
    const gluePolicy = ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSGlueServiceRole");
    role.addManagedPolicy(gluePolicy);

    s3Bucket.grantReadWrite(role);

    // create sqs queue from ARN
    // https://medium.com/@shimo164/cdk-send-amazon-sns-from-aws-lambda-1a0e6c86073e
    // 1-1 Use existing SNS topic: Hard code the topic arn
    // const myTopic = sns.Topic.fromTopicArn(this, 'MyTopic', <topic-arn>);
    const queue = new Queue(this, "kaso snowflake sqs origin", {
      queueName: 'dummy-queue-temp-snowflake-integration',
    });
    // queue.queueArn is Snowflake <ARN>
    const sqsFromArn = Queue.fromQueueArn(this, 'snowflake sqs', queue.queueArn);
    const dummyTopic = new Topic(this, "snowflake sqs 2 sns 2 lambda", {topicName: `${this.stackName}-dummy-sns`});
    dummyTopic.addSubscription(new SqsSubscription(sqsFromArn));

    // create lambda function
    const polingLambda = new NodejsFunction(this, 'fromArnSqn-fooklambda', {
      functionName: `${this.stackName}-sqsLambda`,
      memorySize:1024,
      runtime: Runtime.NODEJS_16_X,
      handler: 'main',
      entry: path.join(__dirname, '/../src/sqs2lambda.ts'),
      description: 'it logs sqs message',
    });
    polingLambda.addEventSource(new SqsEventSource(sqsFromArn, {batchSize: 10,}));

    const polingLambdaPoliy = new PolicyStatement({
      actions: ['sns:*', 'sqs:*'],
      resources: ["*"],
    });
    polingLambda.addToRolePolicy(polingLambdaPoliy);
    sqsFromArn.addToResourcePolicy(polingLambdaPoliy);

    // import { SnsDestination } from 'aws-cdk-lib/aws-s3-notifications';
    s3Bucket.addEventNotification(
      EventType.OBJECT_CREATED,
      new SnsDestination(dummyTopic),
      {prefix: 'test/', suffix: '.png'},
    );

    // Deploy glue job to s3 bucket
    new BucketDeployment(this, "DeployGlueJobFiles", {
      sources: [Source.asset("./lib/assets")],
      destinationBucket: s3Bucket
    });

    // Deploy csv to s3 bucket
    new BucketDeployment(this, "DeployTargetFiles", {
      sources: [Source.asset("./files")],
      destinationBucket: s3Bucket,
      destinationKeyPrefix: "in"
    });

    const glueJob = new cdk.aws_glue.CfnJob(this, "simple-glue-job", {
      name: `${this.stackName}-glue-job`,
      role: role.roleArn,
      description: "glue-workflow test",
      command: {
        name: "pythonshell", 
        pythonVersion: "3.9",
        scriptLocation: "s3://" + s3Bucket.bucketName + "/glue.py"
      },
      defaultArguments:{
        "--TempDir":"s3://" + s3Bucket.bucketName + "/lib",
        "--job-language":"python",
        "--output_bucket_name": s3Bucket.bucketName,
        "--output_prefix_path": "parquet",
        "--BUCKET": s3Bucket.bucketName,
      },
      glueVersion : "3.0",
      maxRetries: 0,
    });

    // // Setting glue workflow
    // // https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_glue.CfnTrigger.html
    const cfnTrigger = new CfnTrigger(this, `${this.stackName}-Trigger`, {
      name: `${this.stackName}-Trigger`,
      workflowName: glueWorkflow.name,
      type: 'SCHEDULED',
      startOnCreation: true,
      schedule: "cron(0 4 * * ? *)",
      actions:[{
        jobName: glueJob.name,
        timeout: 360,
      },
    ],
    });
    cfnTrigger.addDependsOn(glueJob);
    cfnTrigger.addDependsOn(glueWorkflow);

    // SNS
    const notificationTopic = new Topic(this, 'notification-topic-by-email-gluejob', {
      topicName: `${this.stackName}-notificationTopic`,
    });
    notificationTopic.addSubscription(new EmailSubscription(env.email));

    // lambda
    const sampleLambda = new Function(this, "SampleLambdaHandler", {
      functionName: `${this.stackName}-${env.id}-lambda-function`,
      runtime: Runtime.PYTHON_3_9,
      code: Code.fromAsset('src'),
      handler: 'index.lambda_handler',
      environment: {'SNS_ARN' : notificationTopic.topicArn},
      description: "send sns message",
    });

    const snsTopicPoliy = new PolicyStatement({
      actions: ['sns:publish'],
      resources: ["*"],
    });
    sampleLambda.addToRolePolicy(snsTopicPoliy);

    // event rule
    // {
    //   "source": [
    //     "aws.glue"
    //   ],
    //   "detail-type": [
    //     "Glue Job State Change"
    //   ],
    //   "detail": {
    //     "jobName": [
    //       "glue-job-for-err-notification"
    //     ],
    //     "state": [
    //       "FAILED"
    //     ]
    //   }
    // }
    // eventPatternはsource,detailType,detailの順番にする
    const rule = new Rule(this, "glue job error", {
      eventPattern: {
        source: ['aws.glue'],
        'detailType': [
          "Glue Job State Change"
        ],
        detail: {
          jobName:[
            glueJob.name,
          ],
          state:[
            "FAILED"
          ],
        },
      },
      'description': 'glue job error event',
      targets: [new LambdaFunction(sampleLambda)],
      //targets: [new SnsTopic(notificationTopic)]
    });
  }
}
