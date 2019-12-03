FROM mongo

LABEL "MAINTAINER"="fernando.millan@ancud.de"
LABEL "PROJECT"="ML Pipeline"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt update && apt install -y --no-install-recommends python3 python3-wheel python3-setuptools python3-pip supervisor && apt clean && pip3 install --trusted-host pypi.python.org -r requirements.txt

RUN mkdir -p /var/log/supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Make ports 8080 and 27017 available to the world outside this container
EXPOSE 8080
EXPOSE 27017

# Run supervisor to coordinate both processes
CMD ["/usr/bin/supervisord"] 
