# Deployment
Our application is deployed at: https://polyphonypal.netlify.app/

Jocelyn's CS^2 Research Extension is under "Counterpoint" in the navbar.

--------------------------------
# Starting the Application with Docker (recommended)

Ensure you have Docker installed on your machine and that it includes docker compose V2.

Navigate to PolyphonyPal/polyphonypal/flask-api and run

  ```bash
  docker compose up --build
```

In a new terminal in PolyphonyPal/polyphonpal, run the frontend:

```commandline
npm install
npm start
```

To stop the backend container:
```
docker compose down
```

--------------------------------



# Building the Docker Image without compose
cd into PolyponyPal/polyphonypal/flask-api

Create the image:
```bash
 docker pull python:3.10-slim
 docker build -f Dev.Dockerfile . -t dockertesting
```
Run the container:
```bash
docker run -it -v "$(pwd)":/app -p 127.0.0.1:5001:5000 dockertesting
```

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