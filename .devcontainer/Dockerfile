FROM python:3.12-slim

# Create a non-root user
#RUN useradd -ms /bin/bash vscode

# Set the user
#USER vscode

# Install pip requirements
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt \
    && apt-get update && apt-get install -y git zip unzip && rm -rf /var/lib/apt/lists/*

#WORKDIR /home/vscode
