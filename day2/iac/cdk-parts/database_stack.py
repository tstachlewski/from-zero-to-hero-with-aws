from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds


class DatabaseStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, asg_security_groups, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        #Creating Database
        db_mysql_easy = rds.DatabaseInstance(self, "webapp-db",
                                             engine=rds.DatabaseInstanceEngine.MYSQL,
                                             instance_type=ec2.InstanceType.of(
                                                 ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
                                             vpc=vpc,
                                             multi_az=False,
                                             allocated_storage=100,
                                             storage_type=rds.StorageType.GP2,
                                             cloudwatch_logs_exports=[ "error", "general", "slowquery"],
                                             deletion_protection=False,
                                             delete_automated_backups=True,
                                             backup_retention=core.Duration.days(7),
                                             parameter_group=rds.ParameterGroup.from_parameter_group_name(
                                                 self, "para-group-mysql",
                                                 parameter_group_name="default.mysql5.7"
                                             )
                                             )
        for asg_sg in asg_security_groups:
            db_mysql_easy.connections.allow_default_port_from(asg_sg, "EC2 Autoscaling Group access MySQL")