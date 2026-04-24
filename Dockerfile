FROM eclipse-temurin:17-jdk
WORKDIR /home/ubuntu
RUN curl -LO https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar \
    && chmod 777 /home/ubuntu/synthea-with-dependencies.jar