# Use the Python 3.11 image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port your application listens on (if any)
EXPOSE 50505

# Define the command to run your Python application
CMD ["python", "app.py"]
