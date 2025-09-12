# Geo Reverse Service (Photon)

This directory contains a Docker setup for running a [Photon](https://photon.komoot.io/) instance for reverse geocoding. Photon is an open-source reverse geocoder powered by OpenStreetMap.

### Prerequisites

Before you begin, ensure you have the following installed and running on your system:
* **Docker:** [Installation Guide](https://docs.docker.com/get-docker/)
* **Docker Compose:** [Installation Guide](https://docs.docker.com/compose/install/) (Often included with Docker Desktop).

## Setup & Running

### Step 1: Prepare the Data Directory

Create a directory to hold the OpenStreetMap data. In your project's root folder, run this command in the terminal:
```bash
mkdir data
```
### Step 2: Download OpenStreetMap Data
This service requires an OpenStreetMap data file in .osm.pbf format. For this example, we'll use data for the Netherlands.

Download netherlands-latest.osm.pbf from Geofabrik.

Place the downloaded file inside the data directory you created in the previous step.

Your directory structure should now look like this:
```bash
.
├── data/
│   └── netherlands-latest.osm.pbf
└── docker-compose.yml
```

### Step 3: Update docker-compose.yml (Optional)
Create a file named docker-compose.yml in your project's root folder and add the following content. This configuration mounts your local data directory into the container, which is the most efficient way to handle large data files.
```bash
YAML

version: '3.8'
services:
  photon:
    image: rtuszik/photon-docker:latest
    container_name: photon_reverse_geocoder
    ports:
      # Maps port 2322 on your machine to port 2322 in the container.
      - "2322:2322"
    volumes:
      # Mounts your local './data' directory into the container.
      # Photon will automatically find and import the .osm.pbf file from here.
      - ./data:/photon/photon_data
    command: ["-nominatim-import", "-host", "0.0.0.0", "-port", "2322"]
```
### Step 4: Start the Service
With the data file in place and your docker-compose.yml saved, start the service using the VS Code terminal:
```bash
Bash

docker-compose up -d```
(The -d flag runs the container in the background.)

The first time you run this, it will take a significant amount of time to import the OpenStreetMap data. You can watch the progress by running docker logs -f dockergeoreverse-photon-1 or open Docker Desktop and click on Containers photon-1. 

Testing the Service
Once the import is complete, the service will be available on port 2322. You can test it by making a reverse geocoding request. For example, to find out what's at latitude 52.37 and longitude 4.89 (Amsterdam), open your terminal and use curl:

Bash
```bash
curl "http://localhost:2322/reverse?lon=4.89&lat=52.37"
```
You should receive a GeoJSON response with details about the location. 🌍

### Step 5: Reverse Geocoding with Docker

The `gopro-to-csv.py` script can enrich your data with street and city names by using a reverse geocoding service.Once the Photon container is running, you can use the `--reverse-geocode` flag. 
Now street, city and state are used from docker (and timestamp from coridnations), in the link above you can see all available data that could be added lateron in this extraction step.


Here is an example command:

```shell
py Bin/gopro-to-csv.py --street-state-only --simple-output your_video.MP4 output.csv
```
### Step 6: Create a Overlay

The `output.csv` can enrich your doverlay ata with street and city names. You can use the `--location` flag. 


Here is an example command:

```shell
py Bin/gopro-to-csv.py --street-state-only --simple-output your_overlay.mov output.csv

