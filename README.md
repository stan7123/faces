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

Images can be submitted by sending request with `multipart/form-data` content type and file in `image` field to http://localhost:8282/image/.

An exemplary **curl** call: `curl -v -F image=@/path/to/image.png http://localhost:8282/image/`

In a response to this call, there is a websocket endpoint address returned. All websocket's connected clients are notified in real time about each successful face recognition.

Message format: 
```json
{
    "message": "Successful face detection", 
    "created_at": "2024-11-29T16:01:39.784343+00:00", 
    "processed_at": "2024-11-29T16:01:42.763898+00:00", 
    "faces_count": 9, 
    "image_url": "/static/processed_faces/72/46/7246f927-94a4-4225-9a56-b52bab894ad0.jpg"
}
```

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
