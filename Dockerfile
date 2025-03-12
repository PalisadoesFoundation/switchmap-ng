FROM ubuntu:24.04

# Install required packges
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    snmp \
    libsnmp-dev \
    snmp-mibs-downloader \
    gcc \
    python-dev-is-python3 \
    git \
    dos2unix \
    python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Setting up the working directory
WORKDIR /opt/switchmap-ng

# Cloning the switchmap-ng repository into the working directory
RUN git clone https://github.com/PalisadoesFoundation/switchmap-ng .

# Creating a user and group for running the app
RUN groupadd -r switchmap && \
    useradd -r -g switchmap -s /bin/false switchmap

COPY examples/etc/config.yaml /opt/switchmap-ng/etc/config.yaml

RUN mkdir -p /opt/switchmap-ng/var/{log,run,cache} && \
    chown -R switchmap:switchmap /opt/switchmap-ng/var

RUN python3 -m venv /opt/switchmap-ng/venv && \
    /opt/switchmap-ng/venv/bin/pip install --upgrade pip && \
    /opt/switchmap-ng/venv/bin/pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && chmod 750 /entrypoint.sh

# Exposing ports
EXPOSE 7000 7001

#venv to PATH and config directory
ENV PATH="/opt/switchmap-ng/venv/bin:$PATH" \
    SWITCHMAP_CONFIGDIR=/opt/switchmap-ng/etc

ENTRYPOINT ["/entrypoint.sh"]
