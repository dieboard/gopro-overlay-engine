# Use your existing base image that has all the Python libraries installed
FROM gopro-dev-final

# Set the working directory inside the container
WORKDIR /app

# This makes the container self-sufficient.
COPY . .
RUN chmod +x bin/*