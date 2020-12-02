FROM google/cloud-sdk:298.0.0
MAINTAINER "GFT"


# ==== Arguments ====
ENV TERRAFORM_VERSION=0.12.24
ARG python_src=src/main/python/tranquilitybase/gcpdac
ARG bash_src=src/main/bash


# ==== Unix ====
RUN apt-get update \
 && apt-get install unzip=6.0-25 wget=1.20.1-1.1 dos2unix=7.4.0-1 nano=3.2-3 \
 -y --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1


# ==== terraform ====
ENV TF_DEV=true
ENV TF_RELEASE=true
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN mv terraform /usr/local/bin/
# Enable Terraform logging
ENV TF_LOG=ERROR
ENV TF_LOG_PATH=/var/log/tb-gcp-dac-deployment.log


# ==== python ====
WORKDIR /app
COPY ${python_src} src/main/python/tranquilitybase/gcpdac
COPY ${bash_src} src/main/bash
RUN pip install -r ${python_src}/requirements.txt


# ==== Shell =====
# ensure shell scripts have unix line endings and can run
RUN dos2unix -- ${bash_src}/*.sh
RUN dos2unix ${bash_src}/bash_scripts/*.sh
RUN ["sh", "-c", "chmod +x ${bash_src}"]
RUN ["sh", "-c", "chmod +x ${bash_src}/bash_scripts/create_gcp_repo.sh"]

# ==== Run ====
EXPOSE 3100
RUN ["sh", "-c", "sh ${bash_src}/app_docker.sh"]