FROM google/cloud-sdk:298.0.0
MAINTAINER "GFT"

ENV TERRAFORM_VERSION=0.12.24

RUN apt-get update \
 && apt-get install unzip=6.0-25 wget=1.20.1-1.1 dos2unix=7.4.0-1 nano=3.2-3 \
 -y --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

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

# ensure shell scripts have unix line endings
RUN dos2unix -- *.sh
RUN dos2unix ./bash_scripts/*.sh

RUN ["chmod", "+x", "./app_docker.sh"]
RUN ["chmod", "+x", "./bash_scripts/create_gcp_repo.sh"]
EXPOSE 3100
CMD ["/bin/bash", "./app_docker.sh"]


# Enable logs to docker logfile
# Run the wrapper script (to keep the container alive)
COPY daemon.sh /usr/bin/daemon.sh
RUN chmod +x /usr/bin/daemon.sh

# Create the pesudo log file to point to stdout
RUN ln -sf /dev/stdout /var/log/test.log

# Create a cronjob to echo into the logfile just created
RUN echo '* * * * * root `date` > /var/log/test.log' > /etc/crontab

ENTRYPOINT ["/usr/bin/daemon.sh"]