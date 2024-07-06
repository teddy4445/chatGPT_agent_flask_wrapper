# ChatGPT Agent Flask Wrapper

## Abstract

This project is a Flask-based web application that allows users to upload CSV files and query the data using OpenAI's language models. The application processes the CSV file, cleans the column names, and uses an LLM (Large Language Model) API to answer questions based on the uploaded data. This project provides an interface for users to interact with the data in a natural language format.

## Deployment

### Deploy in a Local Environment (Linux) with Docker

1. **Install Docker**:
   Ensure Docker is installed on your Linux system. You can follow the official [Docker installation guide](https://docs.docker.com/engine/install/) for detailed steps.

2. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
	```
3. **Build the Docker Image**:
   ```bash
   docker build -t flask-csv-app .
	```
4. **Run the Docker Container**:
   ```bash
   docker run -d -p 5000:5000 --name flask-csv-container flask-csv-app
	```
5. **Access the Application**: Open a web browser and go to http://localhost:5000.


## Usage

### Requirements

- **OpenAI API Key**:
  To use the application, you need an OpenAI API key. Set your API key in the `OPENAI_API_KEY` variable in the `app.py` file:
  ```python
  OPENAI_API_KEY = 'your_openai_api_key'
```

### Steps to Use the Application
#### Upload a CSV File:
Navigate to the homepage of the application.
Upload a CSV file using the provided file upload form.
The application will process the file and store it temporarily.

#### Query the Data:
After successfully uploading a CSV file, you can query the data by navigating to the query page.
Input your question related to the data in natural language.
The application will use the LLM API to process the query and return the relevant information based on the uploaded data.