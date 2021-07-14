# ECR 

## Create a repository
```
aws ecr create-repository --repository-name <YOUR_REPO_NAME>
```

## Login ECR
```
aws ecr get-login-password --region <AWS_REGION> | docker login --username AWS --password-stdin XXXXXXXXXXX.dkr.ecr.<AWS_REGION>.amazonaws.com
```

## Build & Push to ECR
```
docker build -t <YOUR_REPO_NAME> .
docker tag <YOUR_REPO_NAME>:<TAG> XXXXXXXXXXX.dkr.ecr.<AWS_REGION>.amazonaws.com/<YOUR_REPO_NAME>:<TAG>
docker push XXXXXXXXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/<YOUR_REPO_NAME>:<TAG>
```
