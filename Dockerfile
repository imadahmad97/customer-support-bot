# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
# Including curl and build-essential for Rust, and other dependencies needed for your project
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
# Using rustup, the official installer for Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Add Cargo's bin directory to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy local code to the container image.
COPY . ./

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "run:app"]
