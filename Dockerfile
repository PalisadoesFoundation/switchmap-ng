FROM ubuntu:24.04
RUN  apt-get update && apt-get install -y \ 
    python3 \
    python3-pip \ 
    snmp \
    libsnmp-dev \
    snmp-mibs-downloader\ 
    gcc \ 
    python-dev-is-python3\
    git\
    dos2unix\
    python3-venv

WORKDIR /switchmap-ng

RUN git clone https://github.com/PalisadoesFoundation/switchmap-ng .

RUN groupadd -r switchmap && \
    useradd -r -g switchmap -s /bin/false switchmap

COPY /examples/etc/config.yaml /switchmap-ng/etc/config.yaml

RUN mkdir -p /switchmap-ng/var/{log,run,cache} && \
    chown -R switchmap:switchmap /switchmap-ng/var

RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt 
    
COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && \
    chmod 750 /entrypoint.sh

EXPOSE 7000

ENV PATH="/venv/bin:$PATH"
ENV SWITCHMAP_CONFIGDIR=/switchmap-ng/etc

ENTRYPOINT ["/entrypoint.sh"]