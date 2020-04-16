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

## Run Docker Image
### Authorize Docker command line interface
* `gcloud auth configure-docker`

### run the gcp-dac docker image
* `docker run -p 3100:3100 gcr.io/tranquility-base-images/tb-gcp-dac:alpha`
* with google credentials
* `docker run -p 3100:3100 gcr.io/tranquility-base-images/tb-gcp-dac:alpha -v <CREDENTIALS FILE>:/credentials.json:ro -e GOOGLE_CLOUD_PROJECT=<GOOGLE PROJECT ID> -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json`

### check rest api is working
* `localhost:3100/api/health` 

### Run the stack (gcp-dac + houston-service + mysql57)
* docker-compose -f stack.yml up

### bash shell on container
* `docker exec -it <container name> /bin/bash` 

## References
TODO