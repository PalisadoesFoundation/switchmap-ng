FROM ubuntu:24.04

#Installing dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    apache2 \
    systemd \
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
    apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

# Enabling Apache modules
RUN a2enmod proxy proxy_http

# Creating a user for SwitchMap-NG
RUN groupadd -r switchmap && \
    useradd -r -g switchmap -s /bin/false switchmap

COPY . /switchmap-ng
WORKDIR /switchmap-ng

#Fixing line endings and permissions
RUN find . -type f -exec dos2unix {} + && \
    chmod 750 bin/systemd/*

#configuring Apache
COPY examples/linux/apache/switchmap-ng-apache.conf /etc/apache2/sites-available/switchmap-ng.conf
RUN a2ensite switchmap-ng.conf && \
    a2enmod proxy proxy_http 

#configuring SwitchMap
COPY examples/etc/config.yaml /switchmap-ng/etc/config.yaml
RUN chmod 640 /switchmap-ng/etc/config.yaml && \
    chown switchmap:switchmap /switchmap-ng/etc/config.yaml

# Copying systemd service files
COPY examples/linux/systemd/switchmap_server.service /etc/systemd/system/
COPY examples/linux/systemd/switchmap_poller.service /etc/systemd/system/
COPY examples/linux/systemd/switchmap_ingester.service /etc/systemd/system/
COPY examples/linux/systemd/switchmap_dashboard.service /etc/systemd/system/

#systemd services
RUN systemctl enable switchmap_server.service && \
    systemctl enable switchmap_poller.service && \
    systemctl enable switchmap_ingester.service && \
    systemctl enable switchmap_dashboard.service

#Creating necessary directories
RUN mkdir -p /switchmap-ng/var/{log,run,cache} && \
    chown -R switchmap:switchmap /switchmap-ng/var

#virtual environment
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

#entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && \
    chmod 750 /entrypoint.sh

#environment variables
ENV PATH="/venv/bin:$PATH"
ENV SWITCHMAP_CONFIGDIR=/switchmap-ng/etc

#ports
EXPOSE 80 7000 7001

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]