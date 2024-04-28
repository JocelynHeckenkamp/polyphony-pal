
# Accessing the Hosted Application
The hosted application is accessible via the url: ```https://polyphonypal.netlify.app/```
*Note: the database can only be accessed by running the app locally. There is no public access to the hosted database; however, I have made most of the data available for for download.

--------------------------------
--------------------------------
# Music Generation Usage
## Basic Usage
1. Open application via ```https://polyphonypal.netlify.app/``` or ```localhost:3000```
2. Navigate to music generation via "generation" tab. 
3. Select a key signature (uppercase = major, lowercase = minor)
4. Enter a valid roman numeral combination. ```<chord symbol>,<chord symbol>,...,<chord symbol>```
Full regular expression for valid roman numeral entries shown below:
```
Major Keys:
^(?:(?:viio|IV|I|ii|iii|V|vi)(?:6|64|42|43|65|7|9|11|13|2)?(?:\/(?:viio|IV|I|ii|iii|V|vi)(?:6|64|42|43|65|7|9|11|13|2)?)?(?:,(?!$)|$))+$

Minor Keys:
^(?:(?:VII|VI|V|v|iv|III|iio|i)(?:6|64|42|43|65|7|9|11|13|2)?(?:\/(?:VII|VI|V|v|iv|III|iio|i)(?:6|64|42|43|65|7|9|11|13|2)?)?(?:,(?!$)|$))+$
```
5. Press the "Upload" button. If the combination is not already in the database, a process will be created to find every valid harmonization (limited to 10000 combinations). As they are created, they will be rendered on the page.

7. (Optional) click the desired harmonization to download the midi and copy the music XML to clipboard.

## Access local database
1. Connect to localhost:8080 with the following credentials
```
POSTGRES_USER: postgres
POSTGRES_PASSWORD: password
POSTGRES_DB: mydatabase
```
2. Select XML and RomanScore tables
3. Export the tables with the button in the bottom right of the select screen.
--------------------------------
--------------------------------
# Starting the Application with Docker

## Prerequisites
Ensure you have Docker installed on your machine. and includes docker compose V2

### Build the docker image: WITH COMPOSE (FOR DEVELOPMENT)
   - ensure you have docker daemon running, then cd into polyphonypal root directory to run the following commands:
  ```bash
  docker compose up --build
```
   - To stop the container:
   `docker compose stop`

   - To run the frontend app: cd into polyphonypal root directory run
   ```bash
    npm install
    npm start
```