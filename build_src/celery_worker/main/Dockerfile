FROM google/cloud-sdk:298.0.0


## ==== Arguments/Defaults ====
ENV TERRAFORM_VERSION=0.12.24
ARG src_main_python=src/main/python/
ARG src_main_bash=src/main/bash
ARG src_main_terraform=src/main/terraform
ARG build=build_src/


# ==== Unix ====
RUN apt-get update \
 && apt-get install unzip wget dos2unix nano \
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
COPY ${src_main_terraform} ${src_main_terraform}
COPY ${build} ${build}

# celery seems to be non-intuative working outside the root
COPY src/main/python/tranquilitybase/gcpdac/celery_worker/celery_worker.py celery_worker.py
COPY src/main/bash/tranquilitybase/gcpdac/celery_worker/celery_worker.sh celery_worker.sh

RUN pip install -r ${src_main_python}/tranquilitybase/requirements.txt


# ==== Shell =====
# ensure shell scripts have unix line endings and can run
#RUN dos2unix -- ${src_main_bash}/*.sh
#RUN dos2unix ${src_main_bash}/bash_scripts/*.sh

# ==== Run ====
EXPOSE 3100

#RUN ["sh", "-c", "sh celery_worker.sh"]