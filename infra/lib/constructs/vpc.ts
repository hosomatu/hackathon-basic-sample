import { Construct } from "constructs";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import { EnvName } from "../../parameter";

interface VpcProps {
  vpcCidr: string;
  envName: EnvName;
}

export class Vpc extends Construct {
  readonly vpc: ec2.Vpc;

  constructor(
    scope: Construct,
    id: string,
    props: VpcProps
    ) {
    super(scope, id);

    const { vpcCidr, envName } = props;

    // VPC
    const vpc = new ec2.Vpc(this, "Vpc", {
      vpcName: `hackathon-sample-vpc-${envName}`,
      maxAzs: 2,
      natGateways: 1,
      ipAddresses: ec2.IpAddresses.cidr(vpcCidr),
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: "Public",
          subnetType: ec2.SubnetType.PUBLIC
        },
        {
          cidrMask: 24,
          name: "ApplicationPrivate",
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
        },
        {
          cidrMask: 24,
          name: "DBPrivate",
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
        },
      ],
    });

    // フローログ
    new ec2.FlowLog(this, 'FlowLog', {
      resourceType: ec2.FlowLogResourceType.fromVpc(vpc),
      destination: ec2.FlowLogDestination.toCloudWatchLogs(),
      trafficType: ec2.FlowLogTrafficType.ALL,
    });

    this.vpc = vpc;
  }
}