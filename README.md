Important info to starting this app WITHOUT DOCKER
ensure you have the following installed:
- Python >= 3.11

- cd into flask-api directory
if running without docker:
  create a venv in the root directory of the backend of the project (flask-api)
- Activate the virtual environment: `python3 -m venv venv`
- For Mac: `source venv/bin/activate`
- For Windows: `venv\Scripts\activate`
- Install the required packages: `pip install -r requirements.txt --no-cache-dir`

- To run the app, run the app api first: `flask run`
- Run the frontend app: `npm start`
--------------------------------
## DEVELOPMENT If running WITH Docker  on backend
  Build the docker image: WITHOUT SCRIPT (FOR DEVELOPMENT)
  ```bash
    docker pull python:3.10-slim
    docker build -f Dev.Dockerfile . -t dockertesting
  ```
  Run the container:
 ```bash (maybe unix systems only)
 docker run -it -v "$(pwd)":/app -p 127.0.0.1:5001:5000 dockertesting
-----------------------------------
## If running with Docker DEPLOYMENT ONLY on backend
  build the docker image: WITHOUT SCRIPT
  ```bash
    docker pull python:3.8-slim
    docker build -t flask_server .
  ```
  Run the container:
 ```bash
 docker run -p 127.0.0.1:5001:5000 flask_server
 ```
 Or using the DEPLOYMENT ONLY script provided:
 ` Docker_Deployment_script/buildContainer.bash`

Then: `Docker_Deployment_script/runContainer.bash`