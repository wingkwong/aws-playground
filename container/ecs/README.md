# ECS

## Create ECS Cluster

```
aws ecs create-cluster --cluster-name <YOUR_ECS_CLUSTER>
```

## Create Log group

```
aws logs create-log-group --log-group-name /ecs/<YOUR_APP_NAME>/<YOUR_CONTAINER_NAME>
```

## Create ECS Task Definiton

Every time you create it, it will add a new version. If it is not existing, the version will be 1. 

```bash
aws ecs register-task-definition --cli-input-json "file://./<YOUR_TASK_DEF_NAME>.json"
```

This json file defines the container spec. You can also define secrets and env variables here. 

Example: See [here](https://github.com/wingkwong/aws-playground/blob/master/container/ecs/task-definition-sample.json).

## Create ECS Service

Example: ECS Service with LB & Cloud Map

```bash
aws ecs create-service \
--cluster <YOUR_ECS_CLUSTER> \
--service-name  <YOUR_SERVICE_NAME> \
--task-definition <YOUR_TASK_DEF>:<YOUR_TASK_DEF_VERSION> \
--desired-count <DESIRED_COUNT> \
--launch-type "FARGATE" \
--platform-version 1.3.0 \
--health-check-grace-period-seconds 300 \
--network-configuration "awsvpcConfiguration={subnets=["<YOUR_SUBSETS>"], securityGroups=["<YOUR_SECURITY_GROUPS>"], assignPublicIp=DISABLED}" \
--load-balancer targetGroupArn=<TARGET_GROUP_ARN>,containerName=<CONTAINER_NAME>,containerPort=<YOUR_CONTAINER_PORT> \
--service-registries registryArn=<CLOUDMAP_SERVICE>
```
