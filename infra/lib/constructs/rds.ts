import * as rds from "aws-cdk-lib/aws-rds";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import { EnvName } from "../../parameter";
import { Construct } from "constructs";

interface RdsProps {
  vpc: ec2.Vpc;
  envName: EnvName;
}

export class Rds extends Construct {
  readonly databaseInstance: rds.DatabaseInstance;
  readonly rdsSecurityGroup: ec2.SecurityGroup;

  constructor(
    scope: Construct,
    id: string,
    props: RdsProps
    ) {
    super(scope, id);

    const { vpc, envName } = props;

    const rdsSecurityGroup = new ec2.SecurityGroup(this, "RdsSecurityGroup", {
      vpc: vpc, 
      allowAllOutbound: true,
    });
    rdsSecurityGroup.addIngressRule(
      ec2.Peer.ipv4(vpc.vpcCidrBlock),
      ec2.Port.tcp(3306), // MySQLのポート
      "Allow MySQL access from VPC"
    );

    const databaseInstance = new rds.DatabaseInstance(this, "DatabaseInstance", {
      engine: rds.DatabaseInstanceEngine.mysql({ version: rds.MysqlEngineVersion.VER_8_0 }), // MySQL 8.0
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO), // db.t3.micro
      vpc: vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
      },
      securityGroups: [rdsSecurityGroup],
      multiAz: false, // サンプルなので一旦マルチAZは無効
      allocatedStorage: 20,
      storageType: rds.StorageType.GP3,
      publiclyAccessible: false,
      deletionProtection: false, // サンプルなので削除可能にしておく
      databaseName: `hackathonSampleRDS${envName}`,
      credentials: rds.Credentials.fromGeneratedSecret("admin"), // SecretsManagerが自動生成される
    });
    this.databaseInstance = databaseInstance;
    this.rdsSecurityGroup = rdsSecurityGroup;
  }
}
