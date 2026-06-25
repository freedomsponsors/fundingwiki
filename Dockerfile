# syntax=docker/dockerfile:1
#
# Production image for Funding.Wiki.
#
# This is NOT the devcontainer image (.devcontainer/Dockerfile is for development).
# It builds the Vue frontend, bakes the Django app + dependencies, runs
# collectstatic, and serves via Gunicorn + WhiteNoise. No bind mounts, no
# runtime pip/npm — everything is baked in so the running container always
# matches what was built.

# ---------- Stage 1: build the Vue frontend ----------
FROM node:20-slim AS frontend
WORKDIR /app/frontend

# Install deps first so this layer is cached unless the lockfile changes.
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Build. `vite build` runs in production mode, which loads frontend/.env.production
# (VITE_BASE_PATH=/static/vue/). outDir is ../statfiles/static/vue (vite.config.ts),
# so the assets land at /app/statfiles/static/vue.
COPY frontend/ ./
RUN npm run build

# ---------- Stage 2: Django runtime ----------
FROM python:3.12-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# System deps for GeoDjango (GDAL/GEOS/PROJ), Postgres client, and lxml/xmlsec.
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
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

WORKDIR /app

# Python deps first (cached unless requirements.txt changes).
COPY requirements.txt .
RUN pip install -r requirements.txt

# App source.
COPY . .

# Bring in the freshly built frontend from stage 1 and publish the SPA shell
# as the Django template the root/idea routes render.
COPY --from=frontend /app/statfiles/static/vue ./statfiles/static/vue
RUN cp statfiles/static/vue/index.html templates/vue/index.html

# Collect static into STATIC_ROOT (WhiteNoise CompressedManifestStaticFilesStorage).
# collectstatic does not touch the database.
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
