# High Availabiltiy Design Pattern

## Multi-AZ Pattern

If 1 AZ fails, the system is still available 

### Implementation:

- Create an AMI for your instance
- Spin up multiple instances using that AMI in multiple AZs
- Create a load balancer in multiple AZs and attach the instances
- Confirm instances are attached to load balancer and are in a healthy state 

```
Traffic ---  Elastic Load Balancing ---EC2 in AZ A
                                    ---EC2 in AZ B
```

## HA Database 

One connection string for master and slave with automatic failover. maintenance does not bring down DB but causes failover. Read replicas take load off of master.

### Implementation

- Create an Amazon RDS instance
- Deploy in mulitple AZs
- Create read replicas for each zone

```
Amazon RDS master --- Amazon RDS read replica
        |         |______________
        |                       |
Amazon RDS standby --- Amazon RDS read replica
```

## Floating IP Pattern

Use an Elastic IP address to push traffic to another instance with the same public IP address from the instance which is being failed or upgraded. 

No DNS is required to be updated. Fallback is easy. Just move the EIP address back to the original instance. EIP address can be moved across instances in different AZs in the same region.

### Implementation

- Allocate the EIP address for the EC2 instance
- Upon failure or upgrade, launch a new EC2 instance 
- Disassociate the EIP address from the EC2 instance and associate it to the new EC2 instance

## Floating Interface Pattern

Use an Elastic Network Interface(ENI) on eth1 that can be moved between instances to push traffic to another instance with the same public & private IP address and the same network interface when a ninstance fails or needs to be upgraded.

Similar to Floating IP Pattern, DNS will not need to be updated. You just need to move the ENI back to the original instance for rollback. 

### Implementation

- Allocate the ENI for the instance
- Upon failure or upgrade, launch a new instance 
- Detact the ENI from the instance and attach it to the new instance

## State-Sharing 

Move state off your server intoa a key-value store for better horizontal scale 

### Implementation

- Use Amazon ElastiCache and DynamoDB for data storage
- Prepare a data store for storing the state info 
- Use an ID as a key to identifies a session ID or user ID and store the user info as a value
- Store, reference, and update the state info in the data store instead of storing it in the web/app server

## Scheduled Scale-Out

Use Scaling by Schedule or Scaling by Policy

### Implementation

- Create a customized AMI
- Create a Launch Config for your auto Scaling group
- Create an Auto Scaling group for your instances (behind a load balancer)
- Options:
    - Create Schedule Update to launch or terminate instances at a specified time 
    - Create Scale by Recurrence policy that will automatically scale your instance based upon cron

## Job Observer Pattern

Create an Auto Scaling Group to scale compute resources based upon queue depth to manage resources against the depth of your work queue

### Implementation

- Work items for batch job placed in Amazon SQS queue as messages
- ASG should be created to scale compute resource s up or down based upon Amazon CloudWatch queue depth metric
- Batch processing servers retrieve work items from Amazon SQS to complete job

## Bootstrap Instance

Develop a base AMI, and then bootstrap the instance during the boot process to install software, get updates, and install source code so that your AMI rarely or never changes

### Implementation

- Identify a base AMI to start from
- Create a repository where your code is located
- Identify all packages and configs that need to occur at launch of the instance 
- During launch, pass user data to your EC2 instances that will be executed to bootstrap your instance