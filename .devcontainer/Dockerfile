FROM mcr.microsoft.com/devcontainers/python:3.12

# Install system dependencies for GeoDjango and other libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libjpeg-dev \
    zlib1g-dev \
    libxml2-dev \
    libxslt1-dev \
    libxmlsec1-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN uv pip install --system -r /tmp/requirements.txt \
    && pip uninstall -y decouple python-openid 2>/dev/null; \
    rm -rf /usr/local/lib/python3.12/site-packages/openid/ \
    && pip install --force-reinstall python3-openid

# Install frontend dependencies
COPY frontend/package.json frontend/package-lock.json /tmp/frontend/
RUN cd /tmp/frontend && npm install
