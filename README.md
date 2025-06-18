# Netflix Trending Api

## Table of Contents
- [Technologies](#technologies)
- [Installation](#installation)
- [API Usage](#api-usage)
- [Testing](#testing)

## Technologies

- Python
- FastAPI
- MySQL
- Docker
- PyTest

## Installation

### Prerequisites

- Docker
- Docker Compose
- Git
- Python

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/narminnsn/probit_app.git
cd your_repo_name
```

### 2. Environment Variables
Create a .env file in the root directory with the following content:

- MYSQL_USER=mysql
- MYSQL_PASSWORD=mysql
- MYSQL_DB=netflixdb
- MYSQL_HOST=localhost
- MYSQL_PORT=3306

### 3. Starting Docker

```bash
docker-compose up
```

### 4. Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```


### 5. Running Application

```bash
uvicorn app.main:app --reload

```


# API Documentation

For detailed API documentation, visit:

- Swagger: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

# Testing

You can run tests:

```bash
python -m pytest

```