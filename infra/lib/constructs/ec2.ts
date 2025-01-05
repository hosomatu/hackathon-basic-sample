import * as ec2 from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";
import * as iam from "aws-cdk-lib/aws-iam";

interface Ec2Props {
  vpc: ec2.Vpc;
  rdsSecurityGroup: ec2.SecurityGroup;
  secretArn: string | undefined;
}

export class Ec2 extends Construct {
  readonly instance: ec2.Instance;
  readonly securityGroup: ec2.SecurityGroup;

  constructor(scope: Construct, id: string, props: Ec2Props) {
    super(scope, id);

    const { vpc, rdsSecurityGroup, secretArn } = props;

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

    // RDSのsecretを使用するポリシー
    const secretPolicy = new iam.PolicyStatement({
      actions: ["secretsmanager:GetSecretValue"],
      resources: [secretArn || ""],
    });

    // Session Manager用のIAMロール
    const ec2role = new iam.Role(this, "Ec2Role", {
      assumedBy: new iam.ServicePrincipal("ec2.amazonaws.com"),
    });
    ec2role.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName("AmazonSSMManagedInstanceCore")
    );
    ec2role.addToPolicy(secretPolicy);

    vpc.addInterfaceEndpoint("SSMEndpoint", {
      service: new ec2.InterfaceVpcEndpointAwsService("ssm"),
    });

    // EC2インスタンス
    const ec2Instance = new ec2.Instance(this, "Instance", {
      vpc: vpc,
      role: ec2role,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO), // t3.micro
      machineImage: new ec2.AmazonLinuxImage({
        generation: ec2.AmazonLinuxGeneration.AMAZON_LINUX_2 // Amazon Linux 2
    }),
      securityGroup: ec2SecurityGroup,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      },
    });
    this.instance = ec2Instance;
    this.securityGroup = ec2SecurityGroup;
  }
}
