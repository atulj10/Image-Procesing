# Use the latest Node.js image as the base image
FROM node:latest

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy all frontend files to the working directory
COPY . .

# Expose port 3000 for the frontend application
EXPOSE 3000

# Specify the command to run the frontend application
CMD ["npm", "start"]
