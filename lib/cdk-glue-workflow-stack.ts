import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Bucket, EventType } from 'aws-cdk-lib/aws-s3';
import { CfnRule, Schedule, Rule } from 'aws-cdk-lib/aws-events';
import { LambdaFunction, SnsTopic } from 'aws-cdk-lib/aws-events-targets';
import { CfnJob, CfnTrigger, CfnWorkflow } from 'aws-cdk-lib/aws-glue';
import { Effect, ManagedPolicy, Policy, PolicyStatement, Role, ServicePrincipal } from 'aws-cdk-lib/aws-iam';
import { BucketDeployment, Source } from 'aws-cdk-lib/aws-s3-deployment';
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';
import { Environment } from '../env/environment';
import { Topic } from 'aws-cdk-lib/aws-sns';
import { EmailSubscription } from 'aws-cdk-lib/aws-sns-subscriptions';
import { Code, Function, Runtime } from 'aws-cdk-lib/aws-lambda';
import { SnsDestination } from 'aws-cdk-lib/aws-s3-notifications';
import { eventNames } from 'process';

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

    // SNS
    const notificationTopic = new Topic(this, 'notification-topic-by-email-gluejob', {
      topicName: `${this.stackName}-notificationTopic`,
    });
    notificationTopic.addSubscription(new EmailSubscription(env.email));

    // import { SnsDestination } from 'aws-cdk-lib/aws-s3-notifications';
    s3Bucket.addEventNotification(
      EventType.OBJECT_CREATED,
      new SnsDestination(notificationTopic),
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
