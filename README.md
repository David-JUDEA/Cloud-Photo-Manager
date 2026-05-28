# Cloud-Photo-Manager

This project is a technical demonstration that simulates an AWS Cloud environment directly on a Mac, without the need to create an AWS account or use a Linux virtual machine.

The goal is to set up an API capable of receiving images, storing them in a simulated S3 bucket, and saving their metadata in a local database.

## Summary

[1: Setting up the infrastructure](#1-setting-up-the-infrastructure)

[2: Configuring the S3 Bucket](#2-configuring-the-s3-bucket)

[3: Installation and launch of the API](#3-installation-and-launch-of-the-api)

[4: Usage and Testing](#4-usage-and-testing)

[5: User Interface](#5-user-interface)

- [Docker Installation and usage](#docker-installation-and-usage)

[Common troubleshooting](#common-troubleshooting)

### Technical architecture

The project is based on three main components:

1. Docker & LocalStack: To simulate the AWS S3 service locally.

2. AWS CLI: To interact with the simulated cloud and configure storage.

3. Python & Flask: For the API that links the user to S3 storage.

### Prerequisites

Before starting the project, make sure you have the following tools installed on your machine (macOS):

- Docker Desktop

- Python 3

- AWS CLI

## 1 Setting up the infrastructure

We use Docker Compose to launch LocalStack. The `docker-compose.yml` configuration file defines a service exposed on port 4566, acting as a gateway to the simulated AWS services.

To start the infrastructure, open a terminal at the root of the project and run :

```
docker compose up -d
```

Once the command is complete, you can verify that the S3 service is available with this command :

```
curl http://localhost:4566/\_localstack/health
```

> **_Note: It is normal to see many services with a “disabled” status. Only the “s3” service should be marked as "available"._**

[Summary](#summary)

## 2 Configuring the S3 Bucket

Once LocalStack is up and running, we need to create the bucket (storage space) via the AWS CLI.

First, configure the AWS CLI with dummy credentials (LocalStack accepts them by default) :

```
aws configure
```

Use the following values :

- AWS Access Key ID : `test`

- AWS Secret Access Key : `test`

- Default region name : `us-east-1`

- Default output format : `json`

Next, create the bucket named `cloud-photo-bucket`.

> **_Note the use of the endpoint-url parameter to force the use of our local server rather than the actual Amazon servers. :_**

```
aws --endpoint-url=http://localhost:4566 s3 mb s3://cloud-photo-bucket
```

[To summary](#summary)

## 3 Installation and launch of the API

The API is developed in Python using the Flask framework. It manages file uploads to LocalStack and referencing in an SQLite database.

### Installing dependencies

It is recommended to use a virtual environment to isolate the project libraries. Go to the `back-end` folder :

```
cd back-end
python3 -m venv venv
source venv/bin/activate
pip install flask boto3 flask-cors
```

### Starting the server

Start the server with the following command :

```
python app.py
```

The server will start on port 5001. (http://127.0.0.1:5001).

> **_Note: Port 5001 is used specifically to avoid frequent conflicts with the macOS AirPlay service on port 5000._**

[To summary](#summary)

## 4 Usage and Testing

You can interact with the API via the terminal or a browser.

### Uploading an image (POST)

To send an image, use the following `curl` command (make sure you have a `test.jpg` file in your current folder) :

```
curl -X POST -F "file=@test.jpg" http://127.0.0.1:5001/upload
```

### View the list of images (GET)

To view the list of stored images and their S3 URLs, use curl :

```
curl http://127.0.0.1:5001/images
```

[To summary](#summary)

## 5 User Interface

To provide a user-friendly way to interact with the system, a web interface was created using standard HTML, CSS, and JavaScript. This allows users to visualize the gallery and upload files without using command-line tools.

### Architecture

The frontend is located in the `front-end` folder and communicates with the backend API (port 5001) using JavaScript `fetch` requests. It consists of three static files :

- index.html: Defines the structure of the page, including the upload button and the gallery grid.

- style.css: Manages the visual appearance, including dark mode, card layout, and transparency effects.

- script.js: Handles the logic for selecting files, sending them to the API, and dynamically displaying the list of images.

### Launching the Interface

Modern browsers restrict interactions between local files and APIs (CORS security) when opening an HTML file directly. To run the interface correctly, we must serve it using a simple local web server.

Open a new terminal window (keep the Docker and Python API terminals running) and execute:

```
cd front-end
python3 -m http.server 8000
```

### Accessing the Application

Once the server is running, open your web browser and navigate to:

```
http://localhost:8000
```

You will see the gallery interface. You can now select an image file from your computer, click "Send", and watch it appear dynamically in the gallery grid.

[To summary](#summary)

## Docker Installation and Usage

This is the most efficient way to run the project. It launches the infrastructure (LocalStack), the Backend (Python), and the Frontend (Web Interface) with a single command.

### 1. Start the project

Open a terminal at the root of the project (where the `docker-compose.yml` file is located) and run :

```
docker compose up --build -d
```

The `--build` flag ensures that the latest changes to your code are compiled.

### 2. Access the application

Once the containers are running, everything is accessible automatically:

- Web Interface (Frontend): `http://localhost:8080`

- API (Backend): `http://localhost:5001`

- AWS Services (LocalStack): `http://localhost:4566`

### 3. Useful commands

View logs (for debugging) :

```
docker compose logs -f
```

(Press `Ctrl+C` to exit logs)

Stop the project:

```
docker compose down
```

[To summary](#summary)

## Common troubleshooting

**Error “Connection refused” on port 4566**

- This usually means that Docker is not running or that the LocalStack container has stopped. Check your Docker Desktop application.

**Error “Address already in use” on port 5001**

- Another instance of Python is probably already running. Use the command `lsof -i :5001` to identify the process and stop it, or restart your terminal.

**Database not found**

- If you have recently moved the `app.py` file, make sure you run the python command from inside the `back-end` folder so that the `DB.db` file is created in the right place.

**Images do not load or "Failed to fetch" error**

- Ensure that both your backend server or container (port 5001) and your frontend server (port 8000) are running or container (port 8080) are running using `docker ps`.

- If the console shows a CORS error, verify that you have installed `flask-cors` in your backend and that the server was restarted after the installation.

**Error 500 (Internal Server Error) after restarting Docker**

- Cause: LocalStack is ephemeral by default. Every time you stop the containers (`docker compose down`) or restart Docker, **all data is wiped** (buckets, files, database). The S3 bucket no longer exists.

- Solution: You must recreate the S3 bucket manually after every restart using this command :

```
aws --endpoint-url=http://localhost:4566 s3 mb s3://cloud-photo-bucket
```

[To summary](#summary)
