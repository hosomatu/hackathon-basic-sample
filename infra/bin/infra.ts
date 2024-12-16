#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { InfraStack } from '../lib/stacks/infra-stack';
import { DevStackParameter } from '../parameter';

const app = new cdk.App();
new InfraStack(app, 'InfraStack', {
  config: DevStackParameter,
});