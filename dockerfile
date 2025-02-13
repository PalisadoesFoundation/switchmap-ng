FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    snmp \
    libsnmp-dev \
    snmp-mibs-downloader \
    gcc \
    python3-dev \
    python3-venv \
    dos2unix \
    mysql-client \
    yq && \
    rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -r -s /bin/false switchmap

# Copy application
COPY . /switchmap-ng
WORKDIR /switchmap-ng

# Fix line endings and permissions
RUN find . -type f -exec dos2unix {} + && \
    chmod +x bin/systemd/*

# Ensure config directory exists
RUN mkdir -p etc && cp examples/etc/config.yaml etc/config.yaml && \
    chmod 644 etc/config.yaml && \
    chown switchmap:switchmap etc/config.yaml

# Modify config paths using yq
RUN yq -i -y '.core.system_directory = "/switchmap-ng/var"' etc/config.yaml && \
    yq -i -y '.core.log_directory = "/switchmap-ng/var/log"' etc/config.yaml && \
    yq -i -y '.core.daemon_directory = "/switchmap-ng/var/run"' etc/config.yaml && \
    yq -i -y '.server.db_host = "mysql"' etc/config.yaml && \
    yq -i -y '.server.db_user = "switchmap"' etc/config.yaml && \
    yq -i -y '.server.db_pass = "CHANGE_ME_NOW"' etc/config.yaml
    
# Create necessary directories
RUN mkdir -p /switchmap-ng/var/{log,run,cache} && \
    chown -R switchmap:switchmap /switchmap-ng/var

# Setup virtual environment
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

# Set permissions
RUN chown -R switchmap:switchmap /switchmap-ng

USER switchmap
ENV PATH="/venv/bin:$PATH"
