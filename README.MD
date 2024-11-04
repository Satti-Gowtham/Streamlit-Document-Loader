# RAG Application

This repository contains a Retrieval-Augmented Generation (RAG) application built using Python, Streamlit, and various Langchain components. The application allows users to upload files, convert them to Markdown, and store embeddings in a database.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Satti-Gowtham/streamlit-document-loader.git rag-app
    cd rag-app

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt

## Usage

1. Start the Streamlit application:

    ```bash
    streamlit run app.py

2. Open your web browser and navigate to `http://localhost:8501`

3. Use the file uploader to upload `.pdf`, `.doc`, or `.md` files. The application will process the files and add the data to the database.

## Code Overview

- `rag.py`: Contains the main logic for converting PDF files to Markdown, loading documents, splitting text into chunks, assigning chunk IDs, and adding data to the database.

- `app.py`: The Streamlit application that handles user interactions, file uploads, and invokes the functions defined in `rag.py`.

- `Dockerfile`: Defines the Docker image for the application, setting up the necessary environment and dependencies.

- `.env.example`: An example environment file that outlines required environment variables.

- `requirements.txt`: Lists the required Python packages for the application.

## Docker Setup

To run the application in a Docker container, follow these steps:

1. **Build the Docker image:**

    ```bash
    docker build -t rag-app .

2. **Run the Docker container:**

    ```bash
    docker run -p 8501:8501 rag-app

3. Access the application at `http://localhost:8501`

## Environment Variables

Make sure to create a .env file with the following variables:

```
OLLAMA_BASE_URL=your_ollama_base_url
```
- OLLAMA_BASE_URL: The base URL for the Ollama embeddings service.