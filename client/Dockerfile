# Use an official Node runtime as a parent image
FROM node:21

# Set the working directory in the container to /app
WORKDIR /app

# Add any the package.json file to the container
ADD package.json /app/

#Install the dependencies
RUN npm install

# Add the current directory contents into the container
ADD . /app

# Make port 3000 available
EXPOSE 3000

# Run the command to start the node server
CMD ["npm", "start"]
