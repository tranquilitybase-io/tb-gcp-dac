## GCP DAC: deploys Tranquility Base Solutions and Activators on the Google Cloud Platform

To run the GCP DAC locally, follow the instructions [here](https://github.com/tranquilitybase-io/tb-gcp-dac/wiki/RunServicesWithDocker) 

### Build a container image using the Dockerfile
* `docker build -t gcr.io/tranquility-base-images/tb-gcp-dac:alpha .`

### Push container image to Google Container Repository
* `docker push gcr.io/tranquility-base-images/tb-gcp-dac:alpha`

### list existing containers and remove them
* `docker container list -a `
* `docker container rm xxxxxxx`

### list existing images and remove them 
* `docker image list` 
* `docker image rm xxxxxx`

