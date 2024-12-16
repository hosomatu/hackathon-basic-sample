import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { StackParameter } from '../../parameter';
import { Vpc } from '../constructs/vpc';
import { Rds } from '../constructs/rds';
import { Ec2 } from '../constructs/ec2';

export class InfraStack extends cdk.Stack {
  constructor(
    scope: Construct,
    id: string,
    props: cdk.StackProps&{
      config: StackParameter;
    },
    ) {
    super(scope, id, props);

    const { envName, vpcCidr } = props.config;

    // VPC
    const vpcResources = new Vpc (this, 'VpcResources', {vpcCidr,envName});
    const vpc = vpcResources.vpc;

    // RDS
    const rds = new Rds(this, 'Rds', {vpc, envName});
    const rdsSecurityGroup = rds.rdsSecurityGroup;
    const rdsInstance = rds.databaseInstance;

    // EC2
    const ec2 = new Ec2(this, 'EC2', {vpc, rdsSecurityGroup})
  }
}
