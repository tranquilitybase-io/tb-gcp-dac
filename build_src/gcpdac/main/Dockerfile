FROM google/cloud-sdk:298.0.0
MAINTAINER "GFT"


## ==== Arguments/Defaults ====
ENV TERRAFORM_VERSION=0.12.24
ARG src_main_python=src/main/python/
ARG src_test_python=src/test/python/
ARG src_main_bash=src/main/bash
ARG build=build_src/gcpdac


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


# ==== composition ====
WORKDIR /app
COPY credentials/ credentials/
COPY ${src_main_python} ${src_main_python}
COPY ${src_main_bash} ${src_main_bash}
COPY ${build} ${build}
RUN pip install -r ${src_main_python}tranquilitybase/requirements.txt


# ==== Shell =====
# ensure shell scripts have unix line endings and can run
#RUN dos2unix -- ${src_main_bash}/*.sh
#RUN dos2unix ${src_main_bash}/bash_scripts/*.sh

# ==== Run ====
EXPOSE 3100

#RUN ["sh", "-c", "sh ${src_main_bash}/tranquilitybase/gcpdac/app_docker.sh"]