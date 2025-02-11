FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
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

# Set working directory
WORKDIR /opt/switchmap-ng

# Create necessary directories with proper permissions
RUN mkdir -p etc var/daemon/pid && \
    chmod -R 755 var && \
    chmod -R 700 var/daemon/pid && \
    chmod 755 etc

# Set up Python virtual environment
RUN python3 -m venv venv
ENV PATH="/opt/switchmap-ng/venv/bin:$PATH" \
    PYTHONPATH="/opt/switchmap-ng"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create entrypoint script
COPY entrypoint.sh /opt/switchmap-ng/entrypoint.sh
RUN chmod +x /opt/switchmap-ng/entrypoint.sh

# Expose ports for API and Dashboard
EXPOSE 7000 7001

# Set entrypoint
ENTRYPOINT ["/opt/switchmap-ng/entrypoint.sh"]