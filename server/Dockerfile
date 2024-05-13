# Use an official Python 3.9 runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Add the requirements file to the container
ADD requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Add the current directory contents into the container at /app
ADD . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the command to start uVicorn server
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
