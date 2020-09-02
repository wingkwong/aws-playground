import cdk = require('@aws-cdk/core');
import { Vpc, SubnetType } from '@aws-cdk/aws-ec2';
import { CfnCluster } from '@aws-cdk/aws-msk';
import { KafkaVersion } from './kafka_version';
import { KafkaInstanceType } from './kafka_instance_type';

export class MskStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Step 1: Create a VPC for Your MSK Cluster with a Single Public Subnet
    // AWS::EC2::VPC
    const vpc = new Vpc(this, 'AWSKafkaVPC', {
      cidr: '10.0.0.0/16',
      maxAzs: 3,
      subnetConfiguration: [
        { cidrMask: 24, name: 'kafka', subnetType: SubnetType.PUBLIC }
      ]
    });

    // Step 2: Create an Amazon MSK Cluster
    // AWS::MSK::Cluster
    const cluster = new CfnCluster(this, 'mskCluster', {
      clusterName: 'AWSKafkaCluster',
      kafkaVersion: KafkaVersion.VERSION_2_3_1,
      encryptionInfo: {
        encryptionInTransit: {
          inCluster: true,
          clientBroker: 'TLS'
        }
      },
      numberOfBrokerNodes: 2,
      brokerNodeGroupInfo: {
        clientSubnets: [
          vpc.publicSubnets[0].subnetId,
          vpc.publicSubnets[1].subnetId,
          vpc.publicSubnets[2].subnetId
        ],

        brokerAzDistribution: 'DEFAULT',
        instanceType: KafkaInstanceType.T3_SMALL,
        storageInfo: {
          ebsStorageInfo: {
            volumeSize: 10
          }
        }
      }
    });
  }
}