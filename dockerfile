FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    apache2 \
    python3 \
    python3-pip \
    python3-venv \
    snmp \
    libsnmp-dev \
    snmp-mibs-downloader \
    gcc \
    python3-dev \
    dos2unix \
    mysql-client \
    yq \
    ca-certificates \
    curl \
    gnupg \
    net-tools \
    iptables \
    apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

# Configure Apache
RUN a2enmod proxy proxy_http

# Create switchmap user
RUN groupadd -r switchmap && \
    useradd -r -g switchmap -s /bin/false switchmap

# Copy application code
COPY . /switchmap-ng
WORKDIR /switchmap-ng

# Fix line endings and permissions
RUN find . -type f -exec dos2unix {} + && \
    chmod 750 bin/systemd/*

# Copy Apache config
COPY examples/linux/apache/switchmap-ng-apache.conf /etc/apache2/sites-available/switchmap-ng.conf
RUN a2ensite switchmap-ng.conf

# Copy and set up config.yaml
COPY examples/etc/config.yaml /switchmap-ng/etc/config.yaml
RUN chmod 640 /switchmap-ng/etc/config.yaml && \
    chown switchmap:switchmap /switchmap-ng/etc/config.yaml

# Create necessary directories
RUN mkdir -p /switchmap-ng/var/{log,run,cache} && \
    chown -R switchmap:switchmap /switchmap-ng/var

# Set up virtual environment
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

# Entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && \
    chmod 750 /entrypoint.sh

# Environment variables
ENV PATH="/venv/bin:$PATH"
ENV SWITCHMAP_CONFIGDIR=/switchmap-ng/etc

EXPOSE 80 7000 7001

ENTRYPOINT ["/entrypoint.sh"]