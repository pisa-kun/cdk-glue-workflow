import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Bucket } from 'aws-cdk-lib/aws-s3';
import { CfnRule } from 'aws-cdk-lib/aws-events';
import { CfnTrigger, CfnWorkflow } from 'aws-cdk-lib/aws-glue';
import { Effect, ManagedPolicy, PolicyStatement, Role, ServicePrincipal } from 'aws-cdk-lib/aws-iam';

export class CdkGlueWorkflowStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // create Glue workflow
    //https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_glue.CfnWorkflow.html
    const glueWorkflow = new CfnWorkflow(this, `${this.stackName}-glue-workflow`, {
      description: 'sample work flow',
      maxConcurrentRuns: 1,
      name: `${this.stackName}-trigger`
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

    // // https://repost.aws/questions/QUUuqr0SKyQ6StAkOJzWLyTQ/adding-etl-workflow-to-event-rule
    new CfnRule(this, `${this.stackName}-Rule`, {
      eventPattern: {
        'source': ['aws.s3'],
        'detailType':['Object Created'],
        'detail':{
          'bucket':{
            'name': [s3Bucket.bucketName],
            'key':[{'prefix':'input/'}]
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

    // // Setting glue workflow
    // // https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_glue.CfnTrigger.html
    const cfnTrigger = new CfnTrigger(this, `${this.stackName}-Trigger`, {
      name: `${this.stackName}-Trigger`,
      workflowName: glueWorkflow.name,
      type: 'EVENT',
      actions:[{
        jobName: `${this.stackName}-job`,
      }]

    });

  }
}
