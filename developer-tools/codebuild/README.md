# CodeBuild

## Example #1 : Deploy a static application to AWS S3

See [static-app-buildspec.yml](https://github.com/wingkwong/aws-playground/blob/master/developer-tools/codebuild/static-app-buildspec.yml)

## Example #2 : Deploy a java application to AWS ECS (Fargate)

#### Test Stage

- Dependencies are fetched from Nexus 
   - Settings are defined in ``~/.m2/settings.xml``
- With SonarQube (SAST & SCA)
- Example: See [java-app-test-buildspec.yml](https://github.com/wingkwong/aws-playground/blob/master/developer-tools/codebuild/java-app-test-buildspec.yml)

#### Build Stage

- Dockerize the application and push it to AWS ECR
- Create ``imagedefinitions.json`` for Amazon ECS standard deployments
- Create ``imageDetail.json`` for Amazon ECS blue/green deployments
- Example: See [java-app-build-buildspec.yml](https://github.com/wingkwong/aws-playground/blob/master/developer-tools/codebuild/java-app-build-buildspec.yml)
