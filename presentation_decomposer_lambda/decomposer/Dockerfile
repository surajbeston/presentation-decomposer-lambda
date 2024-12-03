FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libreoffice \
    libreoffice-script-provider-python \
    python3-uno \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set PYTHONPATH to include LibreOffice Python path
ENV PYTHONPATH="/usr/lib/python3/dist-packages"

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir awslambdaric

# Remove any conflicting uno package
RUN pip3 uninstall -y uno

# Install pdf2image
RUN pip3 install pdf2image --no-cache-dir

# Copy the application code
COPY . .

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD aws-lambda-rie /aws-lambda-rie
RUN chmod +x /aws-lambda-rie

# Set up LibreOffice environment variables
ENV HOME="/tmp"
ENV XDG_CONFIG_HOME="/tmp/.config"
ENV XDG_CACHE_HOME="/tmp/.cache"
ENV XDG_DATA_HOME="/tmp/.local/share"
ENV DCONF_PROFILE="/tmp/.config/dconf"

# Create all necessary directories with proper permissions
RUN mkdir -p /tmp/.config/dconf && \
    mkdir -p /tmp/.cache && \
    mkdir -p /tmp/.local/share && \
    mkdir -p /tmp/LibreOffice_Conversion && \
    chmod -R 777 /tmp/.config && \
    chmod -R 777 /tmp/.cache && \
    chmod -R 777 /tmp/.local && \
    chmod -R 777 /tmp/LibreOffice_Conversion

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

