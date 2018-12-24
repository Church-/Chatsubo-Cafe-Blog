from fabric.api import env
from fabric.operations import run as fabric_run
from fabric.context_managers import settings, hide
from kubernetes import client, config
import boto3
import asyncio

a_key = 'AKIAISPDCN67VYJSHSOA'
s_key = 'Yzc977ztGB/NkfXnwOOk1raNpowzVkZEf3IzxBEu'
region = 'us-east-1'
instance_type='t2.micro'
ami_id = 'ami-02d7618005ba44806'


def create_aws_sec_groups(ec2):
    master_ports = {'2379':'2380','6443':'6443','10250':'10252'}
    minion_ports = {'10250':'10252','30000':'32767'}

    kube_master_sec_group = ec2.create_security_group(GroupName='kube_master_sec_group', Description='kube_master_sec_group', VpcId=vpc.id)
    for k,v in master_ports.items():
        kube_master_sec_group.authorize_ingress(
            CidrIp='0.0.0.0/0',
            IpProtocol='tcp',
            FromPort=k,
            ToPort=v)


    kube_minion_sec_group = ec2.create_security_group(GroupName='kube_minion_sec_group', Description='kube_minion_sec_group', VpcId=vpc.id)
    for k,v in minion_ports.items():
        kube_master_sec_group.authorize_ingress(
            CidrIp='0.0.0.0/0',
            IpProtocol='tcp',
            FromPort=k,
            ToPort=v)

def create_aws_ec2_instances(ec2): 
    #Create k8s worker nodes
    ec2.create_instances(
    BlockDeviceMappings=[
            {
            'DeviceName': 'boot-drive',
            'VirtualName': 'boot-drive',
            'Ebs': {
                'DeleteOnTermination': False,
                'Iops': 123,
                'SnapshotId': 'string',
                'VolumeSize': 10,
                'VolumeType': 'standard',
                'Encrypted': False
                },
            'NoDevice': 'string'
            },
        ],
        ImageId=image_id,
        InstanceType=instance_type,
        MaxCount=2,
        MinCount=1,
        Monitoring={
            'Enabled': True|False
        },
        Placement={
            'AvailabilityZone': 'string',
            'Affinity': 'string',
            'GroupName': 'string',
            'PartitionNumber': 123,
            'HostId': 'string',
            'Tenancy': 'default'|'dedicated'|'host',
            'SpreadDomain': 'string'
        },
        SecurityGroups=[
            'string',
        ],
        SubnetId='string',
        UserData='string',
        AdditionalInfo='string',
        ClientToken='string',
        DisableApiTermination=True|False,
        EbsOptimized=True|False,
        IamInstanceProfile={
            'Arn': 'string',
            'Name': 'string'
        },
        InstanceInitiatedShutdownBehavior='stop'|'terminate',
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True|False,
                'DeleteOnTermination': True|False,
                'Description': 'string',
                'DeviceIndex': 123,
                'Groups': [
                    'string',
                ],
                'Ipv6AddressCount': 123,
                'Ipv6Addresses': [
                    {
                        'Ipv6Address': 'string'
                    },
                ],
                'NetworkInterfaceId': 'string',
                'PrivateIpAddress': 'string',
                'PrivateIpAddresses': [
                    {
                        'Primary': True|False,
                        'PrivateIpAddress': 'string'
                    },
                ],
                'SecondaryPrivateIpAddressCount': 123,
                'SubnetId': 'string'
            },
        ],
        PrivateIpAddress='string',
        ElasticGpuSpecification=[
            {
                'Type': 'string'
            },
        ],
    )

    #Create k8s worker nodes
    ec2.create_instances(
    BlockDeviceMappings=[
            {
            'DeviceName': 'boot-drive',
            'VirtualName': 'boot-drive',
            'Ebs': {
                'DeleteOnTermination': False,
                'Iops': 123,
                'SnapshotId': 'string',
                'VolumeSize': 10,
                'VolumeType': 'standard',
                'Encrypted': False
                },
            'NoDevice': 'string'
            },
        ],
        ImageId=image_id,
        InstanceType=instance_type,
        MaxCount=1,
        MinCount=1,
        Monitoring={
            'Enabled': True|False
        },
        Placement={
            'AvailabilityZone': 'string',
            'Affinity': 'string',
            'GroupName': 'string',
            'PartitionNumber': 123,
            'HostId': 'string',
            'Tenancy': 'default'|'dedicated'|'host',
            'SpreadDomain': 'string'
        },
        SecurityGroups=[
            'string',
        ],
        SubnetId='string',
        UserData='string',
        AdditionalInfo='string',
        ClientToken='string',
        DisableApiTermination=True|False,
        EbsOptimized=True|False,
        IamInstanceProfile={
            'Arn': 'string',
            'Name': 'string'
        },
        InstanceInitiatedShutdownBehavior='stop'|'terminate',
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True|False,
                'DeleteOnTermination': True|False,
                'Description': 'string',
                'DeviceIndex': 123,
                'Groups': [
                    'string',
                ],
                'Ipv6AddressCount': 123,
                'Ipv6Addresses': [
                    {
                        'Ipv6Address': 'string'
                    },
                ],
                'NetworkInterfaceId': 'string',
                'PrivateIpAddress': 'string',
                'PrivateIpAddresses': [
                    {
                        'Primary': True|False,
                        'PrivateIpAddress': 'string'
                    },
                ],
                'SecondaryPrivateIpAddressCount': 123,
                'SubnetId': 'string'
            },
        ],
        PrivateIpAddress='string',
        ElasticGpuSpecification=[
            {
                'Type': 'string'
            },
        ],
    )

def create_deployment_object(image_name,tag,port,replica_num):
    # Configureate Pod template container
    container = client.V1Container(
        name=image_name,
        image=str(image_name) + ":" + str(tag),
        ports=[client.V1ContainerPort(container_port=port)])
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": image_name}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=replica_num,
        template=template)
    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec)

    return deployment

def create_deployment(api_instance, deployments):
    # Create deployement
    for deployment in deployments:
        api_response = api_instance.create_namespaced_deployment(
            body=deployment,
            namespace="default")
            
    print("Deployment created. status='%s'" % str(api_response.status))


def deploy_k8s_resources():
    config.load_kube_config()
    extensions_v1beta1 = client.ExtensionsV1beta1Api()
    ghost_deploy = create_deployment_object()
    masto_deploy = create_deployment_object()
    create_deployment(extensions_v1beta1, [ghost_deploy, masto_deploy])
    ingress = create_ingress_object()
    create_ingress(extensions_v1beta1,ingress)
    
def main():
    ec2 = boto3.resource('ec2', aws_access_key_id='AWS_ACCESS_KEY_ID',
                         aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
                         region_name='us-west-2')

    create_aws_sec_groups(ec2)
    ips = create_aws_instances(ec2)
    provision_aws_instances(ips)
    deploy_k8s_resources()

main()