import boto3
import os

region = "us-east-1"
client = boto3.client('ecs', region_name=region)

CONTAINER_NAME = os.environ['NAME']
DOCKER_IMAGE = os.environ['IMAGE']
FAMILY_DEF = os.environ['TASK_DEF']
CLUSTER_NAME = os.environ['CLUSTER']
SERVICE_NAME = os.environ['SERVICE']

def lambda_handler(event, context):
    response = client.register_task_definition(
        family=FAMILY_DEF,
        #taskRoleArn='string',
        networkMode='awsvpc',
        containerDefinitions=[
            {
                'name': CONTAINER_NAME,
                ## Amazon URI for your Docker image in ECS
                'image': DOCKER_IMAGE,
                'memory': 300,
                'portMappings': [
                    {
                        'containerPort': 80,
                        'hostPort': 80,
                        'protocol': 'tcp'
                    },
                ],
                'essential': True,
            },
        ],
    )

    ## Setting our TaskDef for updating our service.
    response = client.update_service(
        cluster=CLUSTER_NAME,
        service=SERVICE_NAME,
        desiredCount=1,
        forceNewDeployment=True,
        deploymentConfiguration={
            'maximumPercent': 200,
            'minimumHealthyPercent': 100
        }
    )
    print("Updated the service named {} under the cluster named {} with an updated task definition".format(SERVICE_NAME, CLUSTER_NAME))