ROM python:3.7-slim-buster
MAINTAINER "GFT"

ENV TERRAFORM_VERSION=0.12.24

RUN apt-get update -y && apt-get install -y git unzip wget

ENV TF_DEV=true
ENV TF_RELEASE=true

RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN mv terraform /usr/local/bin/

WORKDIR /srv
COPY . .
RUN pip install -r ./requirements.txt
RUN ["chmod", "+x", "./app_docker.sh"]
EXPOSE 3100
CMD ["/bin/bash", "./app_docker.sh"]

#ENTRYPOINT ["terraform"]

