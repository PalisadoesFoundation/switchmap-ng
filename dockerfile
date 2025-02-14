FROM ubuntu:24.04

#dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
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
    yq \
    ca-certificates \
    curl \
    gnupg \
    apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

#user
RUN groupadd -r switchmap && \
    useradd -r -g switchmap -s /bin/false switchmap

COPY . /switchmap-ng
RUN chown -R root:switchmap /switchmap-ng && \
    chmod -R 750 /switchmap-ng
WORKDIR /switchmap-ng

# Fixing line endings and permissions
RUN find . -type f -exec dos2unix {} + && \
    chmod 750 bin/systemd/*

# Ensuring config directory exists
RUN mkdir -p etc && cp examples/etc/config.yaml etc/config.yaml && \
    chmod 640 etc/config.yaml && \
    chown switchmap:switchmap etc/config.yaml

# Modifing config paths using yq
RUN yq -i -y '.core.system_directory = "/switchmap-ng/var"' etc/config.yaml && \
    yq -i -y '.core.log_directory = "/switchmap-ng/var/log"' etc/config.yaml && \
    yq -i -y '.core.daemon_directory = "/switchmap-ng/var/run"' etc/config.yaml && \
    yq -i -y '.server.db_host = "mysql"' etc/config.yaml && \
    yq -i -y '.server.db_user = "switchmap"' etc/config.yaml && \
    yq -i -y '.server.db_pass = "${DB_PASSWORD}"' etc/config.yaml

#necessary directories
RUN mkdir -p /switchmap-ng/var/{log,run,cache} && \
    chown -R switchmap:switchmap /switchmap-ng/var

#virtual environment
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

#permissions
RUN chown -R switchmap:switchmap /switchmap-ng

USER switchmap
ENV PATH="/venv/bin:$PATH"