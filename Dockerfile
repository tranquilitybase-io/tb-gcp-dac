# FROM python:3.7-slim-buster
FROM google/cloud-sdk:latest
MAINTAINER "GFT"

ENV TERRAFORM_VERSION=0.12.24

RUN apt-get update -y
RUN apt-get install python3 python3-pip git unzip wget curl dos2unix nano -y
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN apt-get clean && rm -rf /var/lib/apt/lists/

# install terraform
ENV TF_DEV=true
ENV TF_RELEASE=true
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN mv terraform /usr/local/bin/
# Enable Terraform logging
ENV TF_LOG=ERROR
ENV TF_LOG_PATH=/var/log/tb-gcp-dac-deployment.log

# install python libraries
WORKDIR /app
COPY . .
RUN pip install -r ./requirements.txt
RUN dos2unix app_docker.sh

RUN ["chmod", "+x", "./app_docker.sh"]
EXPOSE 3100
CMD ["/bin/bash", "./app_docker.sh"]

