# Use a Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Install system dependencies if needed (e.g., for certain NLP libraries)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy your requirements file first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project code
COPY . .

# Command to run your app (change 'app.py' to your main file name)
CMD ["python", "app.py"]