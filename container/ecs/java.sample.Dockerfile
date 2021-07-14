# Java Example
FROM XXXXXXXXXXX.dkr.ecr.<AWS_REGION>.amazonaws.com/<YOUR_BASE_IMAGE>:<TAG>
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
ADD ./<YOUR_APP_JAR_NAME>.jar .
EXPOSE 8080
# Default timezone : UTC
CMD ["java", "-Duser.timezone=Asia/Hong_Kong", "-jar", "<YOUR_APP_JAR_NAME>.jar"]
