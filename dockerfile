FROM ubuntu:24.04

#dependencies
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

RUN useradd -r -s /bin/false switchmap

COPY . /switchmap-ng
WORKDIR /switchmap-ng

#Fix line endings and permissions
RUN find . -type f -exec dos2unix {} + && \
    chmod +x bin/systemd/*

#config directory
RUN mkdir -p etc && cp examples/etc/config.yaml etc/config.yaml && \
    chmod 644 etc/config.yaml && \
    chown switchmap:switchmap etc/config.yaml

#Modifying config paths using yq
RUN yq -i -y '.core.system_directory = "/switchmap-ng/var"' etc/config.yaml && \
    yq -i -y '.core.log_directory = "/switchmap-ng/var/log"' etc/config.yaml && \
    yq -i -y '.core.daemon_directory = "/switchmap-ng/var/run"' etc/config.yaml

#Creating directories
RUN mkdir -p /switchmap-ng/var/{log,run}

RUN mkdir -p /switchmap-ng/var/log && \
    chown -R switchmap:switchmap /switchmap-ng/var/log && \
    chmod -R 755 /switchmap-ng/var/log

#virtual environment
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

#Setting up permissions
RUN chown -R switchmap:switchmap /switchmap-ng

USER switchmap
ENV PATH="/venv/bin:$PATH"