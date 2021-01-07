#You might need to install boto3 first. "sudo pip install boto3" / sudo pip3 install boto3
import boto3

#Creating a low-level client representing EC2 (with VPC)
client = boto3.client('ec2')

#Creating VPC
Vpc = client.create_vpc( CidrBlock='10.0.0.0/16', TagSpecifications=[ {'ResourceType': 'vpc', 'Tags': [ { 'Key': 'Name', 'Value': 'Workshop-Network' }, ] }, ] )["Vpc"]["VpcId"]
client.modify_vpc_attribute( EnableDnsHostnames={ 'Value': True }, VpcId=Vpc )

#Creating Subnets
subnetPublic1 = client.create_subnet( AvailabilityZone='eu-west-1a', CidrBlock='10.0.1.0/24', VpcId = Vpc, TagSpecifications=[ {'ResourceType': 'subnet', 'Tags': [ { 'Key': 'Name', 'Value': 'SubnetPub1' }, ] }, ])["Subnet"]["SubnetId"]
subnetPublic2 = client.create_subnet( AvailabilityZone='eu-west-1b', CidrBlock='10.0.2.0/24', VpcId = Vpc, TagSpecifications=[ {'ResourceType': 'subnet', 'Tags': [ { 'Key': 'Name', 'Value': 'SubnetPub2' }, ] }, ])["Subnet"]["SubnetId"]
subnetPrivate1 = client.create_subnet( AvailabilityZone='eu-west-1a', CidrBlock='10.0.3.0/24', VpcId = Vpc, TagSpecifications=[ {'ResourceType': 'subnet', 'Tags': [ { 'Key': 'Name', 'Value': 'SubnetPrv1' }, ] }, ])["Subnet"]["SubnetId"]
subnetPrivate2 = client.create_subnet( AvailabilityZone='eu-west-1b', CidrBlock='10.0.4.0/24', VpcId = Vpc, TagSpecifications=[ {'ResourceType': 'subnet', 'Tags': [ { 'Key': 'Name', 'Value': 'SubnetPrv2' }, ] }, ])["Subnet"]["SubnetId"]

#Create Internet Gateway
igw = client.create_internet_gateway( TagSpecifications=[ {'ResourceType': 'internet-gateway', 'Tags': [ { 'Key': 'Name', 'Value': 'igw' }, ] }, ])["InternetGateway"]["InternetGatewayId"]
client.attach_internet_gateway( InternetGatewayId=igw, VpcId=Vpc )

#Configure Routing
routingTable = client.create_route_table( VpcId = Vpc, TagSpecifications=[ {'ResourceType': 'route-table', 'Tags': [ { 'Key': 'Name', 'Value': 'public-rt' }, ] }, ] )["RouteTable"]["RouteTableId"]
client.associate_route_table(RouteTableId=routingTable, SubnetId=subnetPublic1)
client.associate_route_table(RouteTableId=routingTable, SubnetId=subnetPublic2)
route = client.create_route( DestinationCidrBlock="0.0.0.0/0", GatewayId = igw, RouteTableId=routingTable )

#Auto-Assign Public IP for Public Subnets
client.modify_subnet_attribute( MapPublicIpOnLaunch={ 'Value': True }, SubnetId=subnetPublic1)
client.modify_subnet_attribute( MapPublicIpOnLaunch={ 'Value': True }, SubnetId=subnetPublic2)