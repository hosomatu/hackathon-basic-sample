import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { StackParameter } from '../../parameter';
import { Vpc } from '../constructs/vpc';
import { Rds } from '../constructs/rds';

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

    const vpcResources = new Vpc (this, 'VpcResources', {vpcCidr,envName});
    const vpc = vpcResources.vpc;

    const rds = new Rds(this, 'Rds', {vpc, envName});
  }
}
