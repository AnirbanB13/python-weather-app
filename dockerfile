# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt if you have dependencies
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory into the container
COPY . /app

# Expose the port that the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]