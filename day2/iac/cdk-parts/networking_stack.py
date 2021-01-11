from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

class NetworkingStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(self, "webapp-vpc",
            cidr="10.0.0.0/16",
            max_azs = 2,
            nat_gateways = 2,
            subnet_configuration = [
                ec2.SubnetConfiguration(
                    name = 'PUBLIC',
                    subnet_type = ec2.SubnetType.PUBLIC,
                    cidr_mask = 24
                ),
                ec2.SubnetConfiguration(
                    name = 'PRIVATE',
                    subnet_type = ec2.SubnetType.PRIVATE,
                    cidr_mask = 24
                ),
                ec2.SubnetConfiguration(
                    name = 'ISOLATED',
                    subnet_type = ec2.SubnetType.ISOLATED,
                    cidr_mask = 24
                )
            ]
        )

        core.CfnOutput(self, "Output", value=self.vpc.vpc_id)