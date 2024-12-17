import { Duration } from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import { Construct } from 'constructs';
import * as elbv2_tg from 'aws-cdk-lib/aws-elasticloadbalancingv2-targets'

interface AlbProps {
  vpc: ec2.Vpc;
  ec2Instance: ec2.Instance;
  ec2SecurityGroup: ec2.SecurityGroup;
}

export class Alb extends Construct {
  readonly loadBalancer: elbv2.ApplicationLoadBalancer;

  constructor(scope: Construct, id: string, props: AlbProps) {
    super(scope, id);

    const { vpc, ec2Instance, ec2SecurityGroup } = props;

    // セキュリティグループ
    const albSecurityGroup = new ec2.SecurityGroup(this, 'AlbSecurityGroup', {
      vpc,
      description: 'Security group for ALB',
      allowAllOutbound: true,
    });
    albSecurityGroup.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(80), // 仮で80番ポートを開けておく
      'Allow HTTP traffic'
    );
    ec2SecurityGroup.addIngressRule(
      albSecurityGroup,
      ec2.Port.tcp(80),
      'ALB to EC2'
    );

    // ALB
    const alb = new elbv2.ApplicationLoadBalancer(this, 'Alb', {
      vpc,
      internetFacing: true,
      securityGroup: albSecurityGroup,
    });

    // リスナー
    const albListener = alb.addListener('HttpListener', {
      port: 80,
      protocol: elbv2.ApplicationProtocol.HTTP, //仮で80番でリッスンしておく
    });
    albListener.addTargets('HttpTarget', {
      port: 80,
      targets: [new elbv2_tg.InstanceTarget(ec2Instance)],
      healthCheck: {
        enabled: true,
        healthyThresholdCount: 2,
        interval: Duration.seconds(30),
        timeout: Duration.seconds(5),
        path: '/health',
      }
    });

    this.loadBalancer = alb;
  }
}
