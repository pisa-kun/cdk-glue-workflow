import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Bucket } from 'aws-cdk-lib/aws-s3';
import { CfnRule, Schedule, Rule } from 'aws-cdk-lib/aws-events';
import { LambdaFunction, SnsTopic } from 'aws-cdk-lib/aws-events-targets';
import { CfnJob, CfnTrigger, CfnWorkflow } from 'aws-cdk-lib/aws-glue';
import { Effect, ManagedPolicy, Policy, PolicyStatement, Role, ServicePrincipal } from 'aws-cdk-lib/aws-iam';
import { BucketDeployment, Source } from 'aws-cdk-lib/aws-s3-deployment';
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';

export class CdkGlueWorkflowStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

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

    // create role and policy
    // https://wp-kyoto.net/add-iam-role-to-ec2-instance-by-aws-cdk/
    const statement = new PolicyStatement({
      effect: Effect.ALLOW,
    });
    statement.addActions(
      'glue:notifyEvent'
    );
    statement.addResources(`arn:aws:glue:ap-northeast-1:<id>:workflow/${glueWorkflow.name}`);

    const managedPolicy = new ManagedPolicy(this, `${this.stackName}-Policy`, {
      description: 'to notfiy glue workflow from eventbridge',
      statements: [statement]
    });

    // create role
    const glueNotifyRole = new Role(this, `${this.stackName}-Role`, {
      assumedBy: new ServicePrincipal("events.amazonaws.com"),
      managedPolicies: [
        managedPolicy
      ]
    });

    // https://repost.aws/questions/QUUuqr0SKyQ6StAkOJzWLyTQ/adding-etl-workflow-to-event-rule
    new CfnRule(this, `${this.stackName}-Rule`, {
      eventPattern: {
        'source': ['aws.s3'],
        'detailType':['Object Created'],
        'detail':{
          'bucket':{
            'name': [s3Bucket.bucketName],
            'key':[{'prefix':'in/'}]
          }
        }
      },
      targets:[
        {
          arn: `arn:aws:glue:ap-northeast-1:<id>:workflow/${glueWorkflow.name}`,
          id: "some_id",
          roleArn: glueNotifyRole.roleArn,
        },
      ]
    });

    const role = new cdk.aws_iam.Role(this, "access-glue-job", {
      assumedBy: new cdk.aws_iam.ServicePrincipal('glue.amazonaws.com'),
    });
    
    // Add AWSGlueServiceRole to role.
    const gluePolicy = ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSGlueServiceRole");
    role.addManagedPolicy(gluePolicy);

    s3Bucket.grantReadWrite(role);

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
      name: "glue-workflow-parquetjob",
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
    const sampleLambda = new NodejsFunction(this, "sampleLambda",{
      entry: "src/index.ts",
      handler: "handler",
    });

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
          'jobname': [
            glueJob.name
          ],
          'state': [
            "FAILED"
          ]
        },
      },
      'description': 'glue job error event',
      targets: [new LambdaFunction(sampleLambda)],
    });
  }
}
