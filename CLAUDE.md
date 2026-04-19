# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**Djangology CfMS 2** — self-hosted crowdfunding platform (Django 5 + Vue 3), fork of FreedomSponsors generalizing software-bounty mechanics into a full project-lifecycle platform (ideation → knowledge → communication → execution → funding). Powers funding.wiki.

The **conceptual API** (target architecture) lives in `docs/api/overview.md` and `docs/api/entities.md`. Roles, entities, operations, invariants, and implementation status are the north star — the current code is a legacy codebase being progressively reshaped toward that model. When in doubt, consult those docs before reasoning about domain behavior.

## Development

Development is **container-first** — the devcontainer includes GeoDjango/PostGIS/GDAL/Redis dependencies that are painful to set up natively.

```bash
# bring stack up
cd .devcontainer && docker compose up -d
docker compose exec app bash

# inside the container:
.devcontainer/scripts/setup.sh   # waits for PG, migrates, seeds superuser + "Mai"/"Ana" system users, writes frontend/.env, npm install
.devcontainer/scripts/run.sh     # runs Django (:8000) + Vite (:5173) concurrently
.devcontainer/scripts/test.sh    # == python manage.py test
```

Frontend dev URL: `http://localhost:5173`. Backend: `http://localhost:8000`. CSRF cookie flows from Django; the axios client in `frontend/src/utils/request.js` forwards it via `X-CSRFToken`. CORS is open to :5173 with credentials.

### Common commands

```bash
python manage.py migrate
python manage.py makemigrations
pytest                                      # all tests (pytest-django, config in pytest.ini)
pytest apps/issues/tests.py                 # single module
pytest apps/issues/tests.py::test_up_vote   # single test
python manage.py shell
python manage.py fillLanguageData           # seed language data (run by setup.sh)
python manage.py indexIdeasFaiss            # rebuild FAISS index

cd frontend && npm run dev                  # Vite dev
cd frontend && npm run build                # typecheck + bundle (vue-tsc + vite build not wired; plain vite build)
```

### Seeded system users
`setup.sh` creates two app-level service users that code references by username — do not rename:
- **Mai** — attribution for OpenAI-generated content
- **Ana** — anonymous submissions (see `user_services.getAnonymousUser()`)

## Architecture

### Backend layout (`apps/`)

Two Django apps, but `apps.issues` is the monolith — it holds all domain logic (issues, offers, payments, solutions, comments, ideas, media, tech-solutions, tags, watches).

```
apps/issues/
  models/
    issues.py       # legacy monolithic models (~2000 lines): Issue, Offer, Solution, Payment, Project, etc.
    ideas.py        # newer "Ideas" feature (the Conceptual API will merge Ideas → Issues; not done yet)
  views/            # split by feature: issue_views, offer_views, payment_views, paypal_views, bitcoin_views,
                    # vue_views, vue_views_api (the new SPA API), github_hook_views, ...
  urls/             # one file per view module; mounted piecewise from config/urls.py
  services/         # domain/infra services — the canonical place to add new logic:
                    # issue_services, offer_services, payment_services, paypal_services, bitcoin_frespo_services,
                    # faiss_services, openai_services, redis_services, wikidata_services, geo_services,
                    # language_services, media_services, mail_services, activity_services, revision_services,
                    # stats_services, tag_services, techSolution_services, user_services, watch_services,
                    # comment_services, idea_services
  management/commands/  # fillLanguageData, indexIdeasFaiss
  serializers.py    # DRF serializers
apps/frespo_currencies/  # currency exchange (USD/BRL/BTC) — see currency_service.py
```

**URL mounting is non-obvious.** `config/urls.py` imports each `apps.issues.urls.*_urls` module and `include()`s them under different path prefixes (`/issue/`, `/offer/`, `/payment/`, `/api/`, `/vueapi/`, ...). When adding endpoints, find the matching `urls/*.py` rather than inventing a new one.

Two parallel API surfaces coexist:
- **Legacy**: traditional Django views returning HTML or JSON under `/core/`, `/json/...`, `/api/...`
- **New SPA**: DRF views in `views/vue_views_api.py` mounted at `/vueapi/` — this is where new Vue-SPA endpoints go.

### Frontend (`frontend/`)

Vue 3 + Vite + Vuetify + vue-router + axios. Single entry (`src/main.ts`), router in `src/router/index.js`, API services in `src/services/`. Talks to Django at `VITE_API_URL` (default `http://localhost:8000/`). The Django side serves two template shells — `templates/vue/dev.html` (points at Vite dev server) and `templates/vue/index.html` (built assets) — so the SPA is embedded *inside* Django routing rather than served standalone in production.

### Database — PostGIS, not plain Postgres

`DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'` and `apps/issues/models/ideas.py` imports from `django.contrib.gis.db`. New models should also use `django.contrib.gis.db.models` (or plain `django.db.models` if no spatial fields). Do not swap the engine to vanilla postgresql — geo_services and existing migrations assume PostGIS.

### External integrations & graceful degradation

FAISS (idea similarity) depends on OpenAI embeddings. Login + FAISS were recently hardened to degrade gracefully when `OPENAI_API_KEY` is unset (see recent commit `b7877c5`). Preserve that: do not make OpenAI required for core flows. Similarly, PayPal/Bitcoin/GitHub integrations are optional — gate them on configured credentials.

### Settings

`config/settings/base.py` + `config/settings/local.py`; `DJANGO_SETTINGS_MODULE` defaults to `config.settings` (package `__init__` selects the active module). Secrets/config via `python-decouple` (`config(...)` reads env / `.env`). OAuth creds are read from env (`GITHUB_APP_ID`, `GITHUB_API_SECRET`, Google, Twitter, Facebook, Bitbucket). Redis host/port from `REDIS_HOST`/`REDIS_PORT`.

## Conventions worth knowing

- **Services over fat views.** New domain logic goes into `apps/issues/services/<area>_services.py`, not into views or models. Views orchestrate; services decide.
- **`apps/issues/models/issues.py` is legacy and huge.** Prefer extending via services and new small model files rather than piling into that file.
- **Tag duality is transitional.** `Tag` (simple) is slated for removal in favor of `MultilingualTag` (Wikidata-backed). When touching tag code, check both and prefer `MultilingualTag`.
- **Ideas vs Issues.** `Ideas` is a newer experiment; the Conceptual API treats them as Issues. Don't add new divergence between the two — align with the Issue model where feasible.
- **Tests are sparse.** The project doesn't yet have meaningful test coverage; treat new tests as a net positive, but don't assume existing behavior is test-pinned. Runner is **pytest + pytest-django** (config in `pytest.ini`). See `apps/issues/tests.py` for the canonical example pattern (fixtures + `@pytest.mark.django_db` via the `db` fixture + `client.post` against `/vueapi/`).
- **SSL for localhost**, OAuth app setup, and manual non-Docker installation are documented in `README.md` under *Advanced* — not duplicated here.
