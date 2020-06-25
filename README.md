## GCP DAC: deploys Tranquility Base Solutions and Activators on the Google Cloud Platform

To run the GCP DAC locally using Docker , follow the instructions [here](https://github.com/tranquilitybase-io/tb-gcp-dac/wiki/RunServicesWithDocker) 

### Build a DAC container image 
* `docker build -t gcr.io/tranquility-base-images/tb-gcp-dac:<tag> .`

### Push container image to Google Container Repository
* `docker push gcr.io/tranquility-base-images/tb-gcp-dac:<tag>`

### Build and push a mock container image using Dockerfile_mock
NB This mock is just intended to help test the flow with the Eagle Console and Houston Service without executing terraform, Jenkins or gcloud commands
* `docker build -f Dockerfile_mock -t gcr.io/eagle-console-resources/tb-gcp-dac-mock:<tag> .`
* `docker push gcr.io/eagle-console-resources/tb-gcp-dac-mock:<tag>`


