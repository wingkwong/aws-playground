# Copilot

Originally Copilot was called Amazon ECS CLI v2. 

The AWS Copilot CLI is a tool for developers to create, release and manage production ready containerized applications on Amazon ECS and AWS Fargate. From getting started, pushing to a test environment and releasing to production, Copilot helps you through the entire life of your app development.

In short, you can develop, release and operate Container Apps on AWS with a few commands.

![image](https://user-images.githubusercontent.com/35857179/90715223-2fbfc180-e2dc-11ea-923a-f0807146ca61.png)

## Prerequisites

Before using Copilot, make sure you have installed AWS command line tool and setup your aws credentials. To do that, you can run ``aws configure`` to perform your setup. The region for this demonstration is ``ap-southeast-1``. 

After the configuration setup, you can run the below command to verify

```bash
aws sts get-caller-identity
```

## Install

```
curl -Lo /usr/local/bin/copilot https://github.com/aws/copilot-cli/releases/download/v0.1.0/copilot-darwin-v0.1.0 &&
chmod +x /usr/local/bin/copilot &&
copilot --help
```

or through Homebrew

```
brew install aws/tap/copilot-cli
```

## Getting started

Run 

```
copilot
```

to see the commands

```
👩‍✈️ Launch and manage applications on Amazon ECS and AWS Fargate.

Commands 
  Getting Started 🌱
    init        Create a new ECS application.
    docs        Open the copilot docs.
 
  Develop ✨
    app         Commands for applications.
                Applications are a collection of services and environments.

    env         Commands for environments.
                Environments are deployment stages shared between services.

    svc         Commands for services.
                Services are long-running Amazon ECS services.
 
  Release 🚀
    pipeline    Commands for pipelines.
                Continuous delivery pipelines to release services.

    deploy      Deploy your service.
 
  Settings ⚙️
    version     Print the version number.
    completion  Output shell completion code.

Flags
  -h, --help      help for copilot
  -v, --version   version for copilot

Examples
  Displays the help menu for the "init" command.
  `$ copilot init --help`
```

## Init

Copilot will locate the Dockerfile automatically and ask you several questions. After that, it will create a new application containing your service(s).

A sample Dockerfile

```dockerfile
FROM nginx:alpine
EXPOSE 80
COPY . /usr/share/nginx/html
```

Run 

```
copilot init
```

```
Application name: hello-world
Service type: Load Balanced Web Service
Service name: copilot-lb
Dockerfile: ./Dockerfile
Ok great, we'll set up a Load Balanced Web Service named copilot-lb in application hello-world listening on port 80.

✔ Created the infrastructure to manage services under application hello-world.

✔ Wrote the manifest for service copilot-lb at ../copilot-lb/manifest.yml
Your manifest contains configurations like your container size and port (:80).

✔ Created ECR repositories for service copilot-lb.

All right, you're all set for local development.
Deploy: Yes

✔ Created the infrastructure for the test environment.
- Virtual private cloud on 2 availability zones to hold your services     [Complete]
- Virtual private cloud on 2 availability zones to hold your services     [Complete]
  - Internet gateway to connect the network to the internet               [Complete]
  - Public subnets for internet facing services                           [Complete]
  - Private subnets for services that can't be reached from the internet  [Complete]
  - Routing tables for services to talk with each other                   [Complete]
- ECS Cluster to hold your services                                       [Complete]
- Application load balancer to distribute traffic                         [Complete]
✔ Linked account XXXXXXXXXXXX and region ap-southeast-1 to application hello-world.
```

You should be able to see the link at the end. 

Click the link and verify that a simple nginx app is up and running 

![image](https://user-images.githubusercontent.com/35857179/90713597-43692900-e2d8-11ea-8c2f-3caf73e49a28.png)

Go to ECS and you should see a cluster has been provisioned

![image](https://user-images.githubusercontent.com/35857179/90713396-cd64c200-e2d7-11ea-9bd3-a66f86360d2b.png)

You can also take a look at ECS - Task Definition / ECR / EC2 - Load Balancer

## Logs

Copilot provides ``svc logs`` to allow users to check the service logs more easily. You can stream the logs or display the logs within a specfic timeslot

```
  -a, --app string          Name of the application.
      --end-time string     Optional. Only return logs before a specific date (RFC3339).
                            Defaults to all logs. Only one of end-time / follow may be used.
  -e, --env string          Name of the environment.
      --follow              Optional. Specifies if the logs should be streamed.
  -h, --help                help for logs
      --json                Optional. Outputs in JSON format.
      --limit int           Optional. The maximum number of log events returned. (default 10)
  -n, --name string         Name of the service.
      --since duration      Optional. Only return logs newer than a relative duration like 5s, 2m, or 3h.
                            Defaults to all logs. Only one of start-time / since may be used.
      --start-time string   Optional. Only return logs after a specific date (RFC3339).
                            Defaults to all logs. Only one of start-time / since may be used.
```

To stream the logs

```
copilot svc logs --follow
```

To display the logs within a specfic timeslot 

```
copilot svc logs --start-time 2006-01-02T15:04:05+00:00 --end-time 2006-01-02T15:05:05+00:00
```

## Deploy

The application was deployed to the testing environment, which is a single small container to Fargate. It is only for development purposes. 

To deploy in production, run the following command to create a new environment

```
copilot env init
```

Update the manifest file to tell Copilot the application is going to be deployed to production

```yaml
environments:
  production:
    count: 2
    cpu: 1024
    memory: 2048
```

Copilot will create the infrastructure fro the production environment 

```
What is your environment's name? prod
Which named profile should we use to create prod? default
✔ Created the infrastructure for the prod environment.
- Virtual private cloud on 2 availability zones to hold your services     [Complete]
- Virtual private cloud on 2 availability zones to hold your services     [Complete]
  - Internet gateway to connect the network to the internet               [Complete]
  - Public subnets for internet facing services                           [Complete]
  - Private subnets for services that can't be reached from the internet  [Complete]
  - Routing tables for services to talk with each other                   [Complete]
- ECS Cluster to hold your services                                       [Complete]
- Application load balancer to distribute traffic                         [Complete]
✔ Linked account XXXXXXXXXXXX and region ap-southeast-1 to application hello-world.

✔ Created environment prod in region ap-southeast-1 under application hello-world.
```

Deploy your service to production

```
copilot svc deploy --env production
```

## Clean up

```
copilot env list
```

I got 

```
test
prod
```

Force delete the application with environments "test" and "prod"

```
copilot app delete --yes --env-profiles test=default,prod=prod-profile
```

## Conclusion

Copilot can help you to deploy your service containerized to production with a few commands. What you need is just Copilot and Dockerfile. 

Copilot is still in beta. Some services like provisioning storage are not supported yet. (As of 20/08/2020)

## For more

- https://github.com/aws/copilot-cli

