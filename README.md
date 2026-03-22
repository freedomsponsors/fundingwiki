# Djangology CfMS 2
 
**Djangology Crowdfunding Management System** — a self-hosted platform for building crowdfunding sites, built with Django 5 / Vue.js 3.
 
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5-green.svg)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/vue.js-3.x-brightgreen.svg)](https://vuejs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](https://www.docker.com/)

[[_TOC_]]

## What is this?

**Djangology CfMS** lets organizations build and run their own crowdfunding platform — fully self-hosted, no third-party lock-in.
 
It is a fork of [FreedomSponsors](https://github.com/freedomsponsors/www.freedomsponsors.org), generalized from software bounties into a full project lifecycle platform — supporting any type of project, with structured roles for ideation, knowledge, communication, execution, and funding. It currently powers [Funding.Wiki](https://funding.wiki).
 
*This version is a full-stack upgrade from the legacy Django 1 (Python 2) / AngularJS codebase.*

## Tech Stack
 
| Layer     | Technology              |
|-----------|-------------------------|
| Backend   | Python 3.12, Django 5   |
| Frontend  | Vue.js 3                |
| Database  | PostgreSQL + PostGIS    |
| Container | Docker, Docker Compose  |
 
## Installation instructions
### Quick Start
 
The only prerequisite is [Docker](https://docs.docker.com/get-docker/). The full environment — Python, Node.js, PostgreSQL/PostGIS, Redis, and all GeoDjango spatial dependencies — runs inside containers defined in `.devcontainer/`.
 
> _**Disk space required:** ~3.6 GB for all images (`devcontainer-app` ~2.9 GB, `postgreSQL/postgis` ~610 MB, `redis` ~41 MB)._

#### Option A — Command line (any OS, no editor required)

```
git clone https://gitlab.com/wikifunding/djangology-cfms-2 && cd djangology-cfms-2/.devcontainer
docker compose up -d
docker compose exec app bash
.devcontainer/scripts/setup.sh
.devcontainer/scripts/run.sh
```

[▶️ Video for command line installation](https://www.loom.com/share/2420e42b96b941ea8155dcf4e7593b67?t=5m19s)

> ✔️ Now you can access directly to the frontend dev server at **http://localhost:5173**.

#### Option B — Dev Containers (Visual Studio Codium/Code, Cursor, Codespaces and others)

1. Clone the repository and open the project folder in your editor
2. When prompted, click **"Reopen in Container"**
3. Wait for the container to build — setup runs automatically

> ✔️ Now you can access directly to the frontend dev server at **http://localhost:5173**.

Any editor that supports the [Dev Containers specification](https://containers.dev/) — including [VS Codium](https://vscodium.com/), [VS Code](https://code.visualstudio.com/), [Cursor](https://www.cursor.com/), [GitHub Codespaces](https://github.com/features/codespaces), and [Gitpod](https://www.gitpod.io/) — will detect `.devcontainer/` automatically. _[IntelliJ IDEA / PyCharm Professional or Community](https://www.jetbrains.com/help/idea/connect-to-devcontainer.html) has partial support._

### No Docker?

Manual setup is possible but not officially supported. See the [Dockerfile](.devcontainer/Dockerfile) for the full list of system dependencies — the GeoDjango spatial dependencies (GDAL, GEOS, PROJ) and PostGIS make it non-trivial across operating systems — you are on your own. See the [setup.sh](.devcontainer/scripts/setup.sh) for setup steps manually and [run.sh](.devcontainer/scripts/run.sh) for running frontend and backend.

## Development Workflow
 
### Applying migrations
 
```bash
docker compose exec web python manage.py migrate
```
 
### Frontend development
 
```bash
docker compose exec frontend npm run dev
```
 
### Rebuilding after dependency changes
If you change `requirements.txt`, `package.json`, or the `Dockerfile`:
```bash
docker compose up --build
```

## Contributing
 
We welcome contributions from developers and users. Here's how to get involved:
 
### Developing

As just saw: [fork the repository, install and set up](#quick-start) your environment:
 
```bash
git checkout -b feature/your-feature-name
```
 
#### Making your changes
 
- Backend code lives in `apps/`
- Frontend code lives in `frontend/`
- Write tests for new functionality
- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python and the [Vue Style Guide](https://vuejs.org/style-guide/) for the frontend
 
#### Opening a Merge Request
 
- Describe what the change does and why
- Reference any related issue
- Keep Merge Requests focused — one feature or fix per Merge Request
 
### Reporting issues
 
Open an issue on GitLab with:
- A clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Your environment (OS, Docker version)
 
---
 
## Advanced
 
### SSL for localhost
 
If you need to test SSL features locally (e.g. OAuth callbacks, payment providers), you can enable HTTPS on your development environment using [mkcert](https://github.com/FiloSottile/mkcert) and [django-sslserver](https://github.com/teddziuba/django-sslserver).
 
Without this, you may see `urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]` when integrating with external services. The alternative — disabling SSL verification globally in Python — works for basic testing but prevents you from testing SSL-dependent features.
 
**1. Install mkcert inside the container**
 
```bash
docker compose exec app bash
 
# Install certutil dependency
apt-get install -y libnss3-tools
 
# Download and install mkcert
curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
chmod +x mkcert-v*-linux-amd64
cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert
 
# Generate certificates
mkcert -install
cd config/
mkcert -cert-file cert.pem -key-file key.pem 0.0.0.0 localhost 127.0.0.1 ::1
```
 
Restart your browser after running `mkcert -install` so it picks up the new root certificate.
 
**2. Install django-sslserver**
 
```bash
uv pip install --system django-sslserver
```
 
Add `sslserver` to `INSTALLED_APPS` in your settings file, then run the dev server with:
 
```bash
python manage.py runsslserver
```
 
### OAuth credentials
 
To enable GitHub login, add these variables to your environment (or to the `environment:` block in `.devcontainer/docker-compose.yml`):
 
```
GITHUB_APP_ID=your_app_id
GITHUB_API_SECRET=your_api_secret
```
 
You can create a GitHub OAuth app at [github.com/settings/developers](https://github.com/settings/developers).

## About name

Djangology is a classic jazz composition co-written by guitarist [Django Reinhardt](http://en.wikipedia.org/wiki/Django_Reinhardt) —the original guitarist after whom the [Django framework](https://www.djangoproject.com/) is named— and “Vue-linist” [Stéphane Grappelli](https://en.wikipedia.org/wiki/St%C3%A9phane_Grappelli), in a nod to the elegant harmony between Django and [Vue.js](https://vuejs.org/) JavaScript framework. Just as Grappelli’s violin added depth and interplay to Django’s music, Vue brings reactivity and grace to this very application. Together, they swing.

## Thanks

To FreedomSponsors developers and Free Software community involved in big projects like Python, Django and PostgreSQL that make possible this project. A special thanks goes out to Tony Lampada for [FreedomSponsors development](https://github.com/freedomsponsors/www.freedomsponsors.org).

## Licensing

This software is licensed under the [Affero General Public License](http://www.gnu.org/licenses/agpl-3.0.html). Take care of your users' freedom when running this software ❤️.
