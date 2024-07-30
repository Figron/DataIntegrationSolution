# CSV Generator Project

## Overview

This project is designed to generate CSV files with sales data, including intentional flaws for testing purposes. The
generated CSV files are then uploaded to a MinIO bucket. The project also includes a MinIO watcher service that monitors
the bucket and processes the uploaded files.

## Project Structure

- `src/scripts/csv_generator/generate_csv_source_files.py`: Script to generate CSV files with sales data.
- `src/scripts/minio_watcher/minio_watcher.py`: Script to watch the MinIO bucket and process uploaded files.
- `docker-compose.yml`: Docker Compose configuration to set up the necessary services.

## Prerequisites

- Docker
- Docker Compose
- Python 3.x
- pip

## Setup

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```
2. **Install Python dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
3. **Build and start the Docker services:**
    ```sh
    docker-compose up --build
    ```

## Usage

### Running the CSV Generator

The CSV generator script will start automatically when the Docker services are up. It generates sales data with flaws
and uploads the CSV files to the MinIO bucket.

### Watching the MinIO Bucket

The MinIO watcher script will also start automatically and monitor the MinIO bucket for new CSV files. It processes the
uploaded files as they appear.

## Configuration

### MinIO

The MinIO service is configured in the `docker-compose.yml` file. The default credentials are:

- **Username:** minioadmin
- **Password:** minioadmin

### Kafka and Zookeeper

Kafka and Zookeeper services are also configured in the `docker-compose.yml` file. These services are used for message
brokering and coordination.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
