Important info to starting this app
ensure you have the following installed:
- Python >= 3.11

cd into flask-api directory
if running without docker:
  create a venv in the root directory of the backend of the project (flask-api)
- `python3 -m venv venv`
  activate the virtual environment
 For Mac:
- `source venv/bin/activate`
  For Windows:
- `venv\Scripts\activate`
  install the required packages
- `pip install -r requirements.txt --no-cache-dir`

  to run the app:
run the app api first
- `flask run`
run the frontend app
- `npm start`
--------------------------------
## DEVELOPMENT If running with Docker  on backend
  build the docker image: WITHOUT SCRIPT
  ```bash
    docker pull python:3.8-slim
    docker build -f Dev.Dockerfile . -t flask_dev
  ```
  run the container:
 ```bash
 docker run -it -v $(pwd):/app -p 127.0.0.1:5000:5000 test
-----------------------------------
## If running with Docker DEPLOYMENT ONLY on backend
  build the docker image: WITHOUT SCRIPT
  ```bash
    docker pull python:3.8-slim
    docker build . -t flask_server
  ```
  run the container:
 ```bash
 docker run -p 127.0.0.1:5000:5000 flask_server
 ```
 or using the script provided
- ` Docker_Deployment_script/buildContainer.bash`
then `Docker_Deployment_script/runContainer.bash`