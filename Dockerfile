FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    snmp \
    libsnmp-dev \
    snmp-mibs-downloader \
    gcc \
    python-dev-is-python3 \
    python3-venv \
    net-tools \
    netcat-traditional \
    mysql-client \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/switchmap-ng

RUN mkdir -p etc var/daemon/pid && \
    chmod -R 755 var && \
    chmod -R 700 var/daemon/pid && \
    chmod 755 etc

RUN python3 -m venv venv
ENV PATH="/opt/switchmap-ng/venv/bin:$PATH" \
    PYTHONPATH="/opt/switchmap-ng"


COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN mkdir -p /etc
COPY examples/etc/config.yaml /etc/config.yaml

COPY . .

COPY entrypoint.sh /opt/switchmap-ng/entrypoint.sh
RUN chmod +x /opt/switchmap-ng/entrypoint.sh

EXPOSE 7000 7001

ENTRYPOINT ["/opt/switchmap-ng/entrypoint.sh"]