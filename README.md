# Starting the Application without Docker

## Prerequisites
Ensure you have Python version 3.11 or higher installed.

## Backend Setup
1. **Set Up the Virtual Environment:**
   - Navigate to the `flask-api` directory.
   - Create a virtual environment in the root directory:
     ```bash
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     - On macOS:
       ```bash
       source venv/bin/activate
       ```
     - On Windows:
       ```powershell
       .\venv\Scripts\activate
       ```
   - Install the required packages:
     ```bash
     pip install -r requirements.txt --no-cache-dir
     ```

2. **Run the Application:**
   - Start the API:
     ```bash
     flask run
     ```

## Frontend Setup
- Navigate to the `polyphonypal` root directory.
- Install dependencies and start the frontend application:
  ```bash
  npm install
  npm start







# Starting the Application with Docker
--------------------------------
## Prerequisites
Ensure you have Docker installed on your machine. and includes docker compose V2

--------------------------------
### Build the docker image: WITH COMPOSE (FOR DEVELOPMENT)
   - ensure you have docker daemon running, then cd into flask api directory to run the following commands:
  ```bash
  docker compose up --build
```
   - To stop the container:
   `docker compose down`

   - To run the frontend app: cd into polyphonypal root directory run
    `npm install`
    then
    `npm start`


## Build the Docker image: WITHOUT COMPOSE (FOR DEVELOPMENT)
-----------------------------------
# DEVELOPMENT If running WITH Docker on backend


```bash
docker pull python:3.10-slim
docker build -f Dev.Dockerfile . -t dockertesting
  Run the container:
 ```bash (maybe unix systems only)
 docker run -it -v "$(pwd)":/app -p 127.0.0.1:5001:5000 dockertesting
```
## Build the docker image: WITH COMPOSE (FOR DEVELOPMENT)

  - Ensure you have docker daemon running, then cd into flask api directory to run the following commands:

  ```bash
  docker compose up --build
```

  - To stop the container: `docker compose down`

  - To run the frontend app: cd into polyphonypal root directory run:
   `npm install`
   and then:
  `npm start`
-----------------------------------
#### If running with Docker DEPLOYMENT ONLY on backend
  build the docker image: WITHOUT SCRIPT
  ```bash
    docker pull python:3.10-slim
    docker build -t flask_server .
  ```
  Run the container:
 ```bash
 docker run -p 127.0.0.1:5001:5000 flask_server
 ```
 Or using the DEPLOYMENT ONLY script provided:
 ` Docker_Deployment_script/buildContainer.bash`

Then: `Docker_Deployment_script/runContainer.bash`
