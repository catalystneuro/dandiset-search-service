FROM python:3.10-slim-buster

# Set the working directory in docker
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose port 8050
EXPOSE 8050

# Specify the command to run on container start
CMD gunicorn --bind 0.0.0.0:8050 app:server
