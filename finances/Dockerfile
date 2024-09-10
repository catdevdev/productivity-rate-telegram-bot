# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.10 AS build

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports 80 and 443
EXPOSE 80

# Run the FastAPI app using uvicorn on both ports 80 and 443
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 80"]
