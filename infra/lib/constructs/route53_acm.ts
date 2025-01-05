import { Construct } from 'constructs';
import * as route53 from 'aws-cdk-lib/aws-route53';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import * as targets from 'aws-cdk-lib/aws-route53-targets';
import { ApplicationLoadBalancer } from 'aws-cdk-lib/aws-elasticloadbalancingv2';

interface Route53AndAcmProps {
  domainName: string;
  alb: ApplicationLoadBalancer;
}

export class Route53AndAcm extends Construct {
  constructor(scope: Construct, id: string, props: Route53AndAcmProps) {
    super(scope, id);

    const { domainName, alb } = props;

    // ホストゾーン
    const hostedZone = new route53.HostedZone(this, 'HostedZone', {
      zoneName: domainName,
    });

    // ACM証明書
    const certificate = new acm.Certificate(this, 'Certificate', {
      domainName,
      validation: acm.CertificateValidation.fromDns(hostedZone), // DNS検証にRoute 53を使用
    });

    // ALBのリスナーに証明書を設定
    alb.listeners[0].addCertificates('HttpsCertificate', [certificate]);

    // Route 53にAレコードを設定 (ALBへのAliasレコード)
    new route53.ARecord(this, 'AliasRecord', {
      zone: hostedZone,
      target: route53.RecordTarget.fromAlias(new targets.LoadBalancerTarget(alb)),
    });
  }
}