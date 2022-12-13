import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Bucket } from 'aws-cdk-lib/aws-s3';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class CdkGlueWorkflowStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // create s3 bucket
    // https://zenn.dev/nmemoto/articles/s3-eventnotification-with-eventbridge
    const s3Bucket = new Bucket(this, `${this.stackName}-Bucket`, {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      eventBridgeEnabled: true,
    });

    // create eventBridge rule
  }
}
