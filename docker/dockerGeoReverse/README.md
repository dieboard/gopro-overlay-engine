# Geo Reverse Service (Photon)

This directory contains a Docker setup for running a [Photon](httpss://photon.komoot.io/) instance for reverse geocoding.

## Setup

### 1. Download OpenStreetMap Data

This service requires an OpenStreetMap data file. For the Netherlands, you can download the `netherlands-latest.osm.pbf` file from [Geofabrik](https://download.geofabrik.de/europe/netherlands.html).

Download the file and place it in a directory of your choice. You will need to mount this directory into the Docker container.

For example, you can create a `data` directory inside this directory (`docker/dockerGeoReverse/data`) and place the `.osm.pbf` file there.

### 2. Update `docker-compose.yml` (Optional)

If you placed the data file in a different location than `docker/dockerGeoReverse/data`, you will need to update the `volumes` section in the `docker-compose.yml` file to point to the correct location of your data file.

The current `docker-compose.yml` assumes the data is in a volume that will be populated by the container on first run, but for a large file like `netherlands-latest.osm.pbf`, it's better to mount it directly.

Here is an example of how to mount a local directory:

```yaml
version: '3.8'
services:
  photon:
    image: rtuszik/photon-docker:latest
    environment:
      - COUNTRY_CODE=nl
      - UPDATE_STRATEGY=DISABLED
    ports:
      - "2322:2322"
    volumes:
      - ./data:/photon/photon_data # Mounts the local 'data' directory

volumes:
  photon_data:
```

**Note:** The `photon.jar` file is part of the `rtuszik/photon-docker` Docker image, so you do not need to download it separately.

## Running the service

Once you have downloaded the data file and configured the `docker-compose.yml` correctly, you can start the service using:

```bash
docker-compose up
```

The first time you run this, it may take a while to import the OpenStreetMap data.

The service will be available on port `2322`.
