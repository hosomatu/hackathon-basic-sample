import * as ec2 from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";

interface Ec2Props {
  vpc: ec2.Vpc;
  rdsSecurityGroup: ec2.SecurityGroup;
}

export class Ec2 extends Construct {
  readonly Instance: ec2.Instance;

  constructor(scope: Construct, id: string, props: Ec2Props) {
    super(scope, id);

    const { vpc, rdsSecurityGroup } = props;

    // セキュリティグループ。RDSとの通信を許可
    const ec2SecurityGroup = new ec2.SecurityGroup(this, "Ec2SecurityGroup", {
      vpc: vpc,
      allowAllOutbound: true,
    });
    ec2SecurityGroup.addIngressRule(
      rdsSecurityGroup,
      ec2.Port.tcp(3306),
      "EC2 to RDS"
    );
    rdsSecurityGroup.addIngressRule(
      ec2SecurityGroup,
      ec2.Port.tcp(3306),
      "RDS to EC2"
    );

    // EC2インスタンス
    const ec2Instance = new ec2.Instance(this, "Instance", {
      vpc: vpc,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO), // t3.micro
      machineImage: new ec2.AmazonLinuxImage({
        generation: ec2.AmazonLinuxGeneration.AMAZON_LINUX_2 // Amazon Linux 2
    }),
      securityGroup: ec2SecurityGroup,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      },
    });
    this.Instance = ec2Instance;
  }
}
