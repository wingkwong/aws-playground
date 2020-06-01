# Create & connect to an Aurora Serverless Database via CLI

![image](https://user-images.githubusercontent.com/35857179/83414597-5f36fe80-a450-11ea-8534-a5765d171aab.png)

## Create Aurora Serverless DB Cluster

```
aws rds create-db-cluster --engine-version 5.6.10a --db-cluster-identifier serverlessdb --engine-mode serverless --engine aurora --master-username <USERNAME> --master-user-password <SECURE_PASSWORD> --db-subnet-group-name <DB_SUBNET_NAME> --scaling-configuration MinCapacity=2,MaxCapacity=4,AutoPause=false,TimeoutAction=ForceApplyCapacityChange --enable-http-endpoint --region us-east-1
```

In the returned JSON, copy the DBClusterArn and paste it into a text file, as we'll need it a little later.

## Create a Secret in Secrets Manager for DB Credentials

Create a secret in Secrets Manager, replacing <USERNAME> and <SECURE_PASSWORD> with the credentials you set in the previous command:

```
aws secretsmanager create-secret --name "ServerlessDBSecret" --description "Credentials for serverless DB" --secret-string '{"username":"<USERNAME>" , "password":"<SECURE_PASSWORD>"}' --region us-east-1
```

In the returned JSON, copy the DBClusterArn and paste it into a text file, as we'll need it a little later.

## Connect to and Execute SQL Query Against Your Provisioned Serverless Aurora DB Instance

```
aws rds-data execute-statement --resource-arn <DB_CLUSTER_ARN> --secret-arn <SECRET_ARN> --database information_schema --sql "select * from information_schema.tables LIMIT 1" --region us-east-1
```
