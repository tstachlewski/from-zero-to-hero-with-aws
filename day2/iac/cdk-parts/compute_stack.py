from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_elasticloadbalancingv2 as elb


ec2_type = 't3.micro'
key_name = 'workshop'
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )

with open("./user_data/user_data.sh") as f:
    user_data = f.read()


class ComputeStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #Creating Bastion
        bastion = ec2.BastionHostLinux(self,'webapp-bastion',
            vpc = vpc,
            subnet_selection = ec2.SubnetSelection( subnet_type = ec2.SubnetType.PUBLIC)
        )
        bastion.instance.instance.add_property_override("KeyName", key_name)
        bastion.connections.allow_from_any_ipv4( ec2.Port.tcp(22), "Internet access SSH")

        #Creating AutoScaling group
        self.asg = autoscaling.AutoScalingGroup(self, "webapp-autoscaling",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,
                                                )

        #Creating Load Balancer
        alb = elb.ApplicationLoadBalancer(self, "webapp-alb",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="webapp-alb"
                                          )
        alb.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Internet access ALB 80")
        listener = alb.add_listener("my80",port=80,open=True)

        #Final Configuration
        self.asg.connections.allow_from(alb, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
        listener.add_targets("addTargetGroup",port=80,targets=[self.asg])

        core.CfnOutput(self, "Output", value=alb.load_balancer_dns_name)