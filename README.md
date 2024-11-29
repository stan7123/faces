# Faces
Simple app for face recognition from images.

## Installation

### Requirements
- [Docker](https://docs.docker.com/engine/install/) and [Docker compose](https://docs.docker.com/compose/install/) installed in the system

### Installation

Get the code from Github:
```
git clone https://github.com/stan7123/faces.git
```

### Running

#### Configure
Create file named `.env` based on `default.env` and adjust variables if needed (should work fine without adjustments).

#### Run
```
docker compose up --build
```
Or to run in the background:
```
docker compose up -d --build
```

Open http://localhost:8282/image to confirm the service is running (should show DRF's submit image page). 

## How to use

Images can be submitted by sending request with content type as `multipart/form-data` to http://localhost:8282/image/.
An exemplary `curl` call: `curl -v -F image=@/path/to/image.png http://localhost:8282/image/`


Note: Image size is currently limited to 100MB. It can be adjusted on the proxy. 


## Design decisions
- Using sqlite instead of service like DB for simplicity. Potentially the app can be written without DB persistence layer using only Redis. Optionally, Redis' persistence can be uplifted.
- Storing uploaded and processed files in directories next to the code for simplicity. Usually some kind of storage service like S3 is used.
- Using django-rq as simple and lightweight alternative to Celery
- Using simple websocket stand-alone server to not go into more complicated Django channels. This required introducing nginx proxy to keep the requirement of serving the app on one port.

## Things to improve for production setup
- Components might require replacement when run in the cloud for scaling and reliability: RDBMS or key-value persistent storage as database, SQS or similar as queue etc.
- CI/CD workflows
- Introduce throttling to secure against API overload
- In case of high traffic few things can be improved in terms of scaling: auto-scaling of workers, using serverless like AWS Lambda instead of rq workers

## Possible optimizations
- Calculate image's hash and check if the image was already processed before. It would reduce required calculation in case same images are uploaded multiple times.
- Running face detection on GPU
- DB table with submissions might grow large with time, a process for archiving/deleting old submissions might be considered
