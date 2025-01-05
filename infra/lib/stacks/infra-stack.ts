import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { StackParameter } from '../../parameter';
import { Vpc } from '../constructs/vpc';
import { Rds } from '../constructs/rds';
import { Ec2 } from '../constructs/ec2';
import { Alb } from '../constructs/alb';
import { Route53AndAcm } from '../constructs/route53_acm';

export class InfraStack extends cdk.Stack {
  constructor(
    scope: Construct,
    id: string,
    props: cdk.StackProps&{
      config: StackParameter;
    },
    ) {
    super(scope, id, props);

    const { envName, vpcCidr, domainName } = props.config;

    // VPC
    const vpcResources = new Vpc (this, 'VpcResources', {vpcCidr,envName});
    const vpc = vpcResources.vpc;

    // RDS
    const rds = new Rds(this, 'Rds', {vpc, envName});
    const rdsSecurityGroup = rds.rdsSecurityGroup;
    const secretArn = rds.secretArn;

    // EC2
    const ec2 = new Ec2(this, 'EC2', {vpc, rdsSecurityGroup, secretArn});
    const ec2Instance = ec2.instance;
    const ec2SecurityGroup = ec2.securityGroup;

    // ALB
    const alb = new Alb(this, 'Alb', {vpc, ec2Instance, ec2SecurityGroup});

    // Route53、ACM
    // new Route53AndAcm(this, 'Route53andACM', {domainName, alb})
  }
}
