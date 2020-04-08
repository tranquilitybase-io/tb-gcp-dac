FROM golang:alpine
MAINTAINER "GFT"

ENV TERRAFORM_VERSION=0.12.24

RUN apk add --update git bash openssh python3

ENV TF_DEV=true
ENV TF_RELEASE=true

WORKDIR $GOPATH/src/github.com/hashicorp/terraform
RUN git clone https://github.com/hashicorp/terraform.git ./ && \
    git checkout v${TERRAFORM_VERSION} && \
    /bin/bash scripts/build.sh

WORKDIR /srv
COPY . .
RUN pip install -r ./requirements.txt
RUN ["chmod", "+x", "./app_docker.sh"]
EXPOSE 3100
CMD ["/bin/bash", "./app_docker.sh"]