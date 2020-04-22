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
    * `docker run -p 3100:3100 gcr.io/tranquility-base-images/tb-gcp-dac:alpha -v <EC CONFIG YAML FILE>:/ec-config.yaml:ro -v <CREDENTIALS FILE>:/credentials.json:ro  -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json`
* example call
    *  `docker run -p 3100:3100 -v C:/dev/tb-gcp-dac/tbase-ci-647fda7b088a.json:/credentials.json:ro -v C:/dev/tb-gcp-dac/ec-config.yaml:/app/ec-config.yaml:ro  -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json gcr.io/tranquility-base-images/tb-gcp-dac:alpha`
### check rest api is working
* `localhost:3100/api/health` 

### Run the stack (gcp-dac + houston-service + mysql57)
* docker-compose -f stack.yml up

### bash shell on container
* `docker exec -it <container name> /bin/bash` 

## References
TODO