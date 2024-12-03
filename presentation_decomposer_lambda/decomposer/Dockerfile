FROM public.ecr.aws/lambda/python:3.10

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=${PATH}:/opt/libreoffice24.8/program

# Install system dependencies and LibreOffice
RUN set -ex && \
    yum update -y && \
    yum install -y \
        wget \
        tar \
        gzip \
        cairo \
        cups \
        libXinerama \
        cups-libs \
        dbus-glib \
        libxslt \
        libxml2 \
        libX11 \
        libXext \
        libXrender \
        libgcc \
        libstdc++ \
        dbus-libs \
        dbus-glib-devel \
        fontconfig \
        liberation-fonts \
        && \
    cd /usr/local && \
    wget https://mirrors.arunmathaisk.in/tdf/libreoffice/stable/24.8.3/rpm/x86_64/LibreOffice_24.8.3_Linux_x86-64_rpm.tar.gz && \
    tar -xvf LibreOffice_24.8.3_Linux_x86-64_rpm.tar.gz && \
    cd LibreOffice_24.8.3.2_Linux_x86-64_rpm/RPMS/ && \
    yum localinstall -y *.rpm --skip-broken && \
    cd /usr/local && \
    rm -rf LibreOffice_24.8.3* && \
    yum clean all

# Create necessary directories with proper permissions
RUN mkdir -p /tmp/.config && \
    mkdir -p /tmp/.cache && \
    mkdir -p /tmp/LibreOffice_Conversion && \
    chmod 777 /tmp/.config && \
    chmod 777 /tmp/.cache && \
    chmod 777 /tmp/LibreOffice_Conversion

# Set PYTHONPATH to include LibreOffice Python path
ENV PYTHONPATH="${LAMBDA_TASK_ROOT}:/usr/lib64/python3.10/site-packages:/opt/libreoffice24.8/program"

# Add symbolic links for LibreOffice Python modules if they're in a different location
RUN ln -s /opt/libreoffice24.8/program/uno.py /usr/lib64/python3.9/site-packages/uno.py && \
    ln -s /opt/libreoffice24.8/program/unohelper.py /usr/lib64/python3.9/site-packages/unohelper.py

# Verify Python can find the uno module
RUN python3 -c "import uno; print('uno module found')" || echo "Failed to import uno"

# Install awslambdaric
RUN pip3 install awslambdaric

# Copy requirements and install Python dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . ${LAMBDA_TASK_ROOT}

# Create decomposer directory if it doesn't exist
RUN mkdir -p ${LAMBDA_TASK_ROOT}/decomposer && \
    touch ${LAMBDA_TASK_ROOT}/decomposer/__init__.py

# Copy and set permissions for bootstrap script
COPY bootstrap.sh /var/runtime/bootstrap
RUN chmod +x /var/runtime/bootstrap

# Verify LibreOffice installation and create symlinks if needed
RUN find / -name soffice -type f 2>/dev/null || find / -name libreoffice -type f 2>/dev/null || echo "LibreOffice not found in standard locations" && \
    echo "PATH=$PATH" && \
    echo "Checking specific LibreOffice locations:" && \
    ls -la /opt/libreoffice*/program/ || true && \
    ls -la /usr/lib64/libreoffice/program/ || true && \
    ls -la /usr/bin/libreoffice* || true

# Set environment variables for library path
ENV LD_LIBRARY_PATH=/usr/lib64:/usr/lib:/lib64:/lib:/opt/libreoffice24.8/program

# Set the Lambda handler
ENTRYPOINT ["/var/runtime/bootstrap"]
CMD ["processor.process_slide.handler"]

