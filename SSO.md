# SSO MediaWiki → Django

MediaWiki is the sole login authority. The existing Nginx TLS proxy serves `https://funding.wiki`, sends `/doc`, `/w` and `/images` to MediaWiki, and sends other paths to Django. The location fragment is in `nginx-sso-locations.conf`; include it in the existing TLS `server` block on the public proxy. Adjust the backend IP there if the app server is reached at a different address. Django reads only the configured MediaWiki session cookie and calls the internal MediaWiki Action API over the Docker bridge network. It never accepts identity from a client supplied identity header and does not use Django's login session to authenticate requests. Django's CSRF middleware remains enabled.

## Configuration

Set matching values in `.env.production` for Django and in the MediaWiki Compose environment (shell or its Compose `.env` file):

| Variable | Default | Purpose |
|---|---|---|
| `MEDIAWIKI_SERVER_URL` | `https://funding.wiki` | Public origin and MediaWiki canonical server |
| `MEDIAWIKI_INTERNAL_API_URL` | `http://mediawiki/w/api.php` | Django-only internal API endpoint |
| `MEDIAWIKI_INTERNAL_SERVER_URL` | `http://mediawiki` | MediaWiki internal server URL |
| `MEDIAWIKI_API_HOST` | `funding.wiki` | Host header for API requests |
| `MEDIAWIKI_COOKIE_PREFIX` | `mediawiki` | Cookie prefix; session cookie is `<prefix>_session` (matches this wiki's current DB name and legacy cookie) |
| `MEDIAWIKI_COOKIE_PATH` | `/` | Cookie path so it reaches Django and MediaWiki |
| `MEDIAWIKI_COOKIE_DOMAIN` | unset | Optional cookie domain; host-only cookie is preferred |
| `MEDIAWIKI_COOKIE_SECURE` | `true` | Secure cookie flag; use HTTPS publicly |
| `MEDIAWIKI_COOKIE_SAMESITE` | `Lax` | MediaWiki SameSite cookie setting |
| `MEDIAWIKI_CACHE_TTL` | `20` | Userinfo cache TTL, seconds |
| `MEDIAWIKI_API_TIMEOUT` | `2` | API timeout, seconds |
| `MEDIAWIKI_ADMIN_GROUP` | `sysop` | MediaWiki group mapped to Django admin flags |

`MEDIAWIKI_COOKIE_DOMAIN` is intentionally left unset by default: a host-only cookie is shared by paths on this origin without being sent to unrelated subdomains. Set it only if the deployment uses a deliberate shared parent domain.

Compose first creates the shared Docker network from `espacio_de_trabajo/mediawiki`, then the Django Compose stack attaches the app to it. The existing Nginx continues to terminate TLS. Django and MediaWiki backends are published on the app server's current private address for Nginx; Django's API lookup itself uses the Docker-only service name. Keep the internal API URL on the Docker network.

## Identity behavior

The middleware maps MediaWiki's numeric ID to an additive `MWIdentity` one-to-one profile for Django's existing auth `User`; it does not change `AUTH_USER_MODEL`. It updates Django usernames when MediaWiki renames an account, sets unusable passwords, and synchronizes `is_staff`/`is_superuser` from the configured group on each cache refresh. MediaWiki usernames that Django's built-in username validator cannot store (notably temporary names beginning with `~`) use `mw_<id>` locally.

`userinfo`'s `blockinfo` reports active blocks (including `blockedby`); blocked users are treated as anonymous in Django and their local account is deactivated. If the same profile is later seen without a block, middleware reactivates an account it had deactivated for that block. MediaWiki's API docs describe `blockinfo` on [API:Userinfo](https://www.mediawiki.org/wiki/API:Userinfo).

Temporary accounts do not exist as MediaWiki identities until MediaWiki creates one, usually on the first edit. Before then, no session identity is returned and Django sees `AnonymousUser`. Once created, `userinfo` returns `temp`; Django marks the profile temporary. MediaWiki 1.46 exposes expiration through `list=allusers&auprop=tempexpired` (see [API:Allusers](https://www.mediawiki.org/wiki/API:Allusers)); run `python manage.py expire_mw_temp_users` periodically to deactivate matching Django users. MediaWiki must also run its own `expireTemporaryAccounts.php` maintenance script for account expiration to happen.

## Try it

1. Start MediaWiki Compose, then Django Compose, preserving the existing database volumes. Add `nginx-sso-locations.conf` to the active Nginx TLS server block and reload that proxy.
2. Browse to `https://funding.wiki/doc/Special:UserLogin`, sign in, and visit a Django page. The current user should be the matching Django user; a sysop should be able to use `/admin/`.
3. Sign out through `https://funding.wiki/doc/Special:UserLogout`, then reload Django; the next identity lookup should be anonymous (up to the configured cache TTL).
4. In a private browser session, edit a page anonymously to trigger MediaWiki temporary-account creation, then visit Django. It should identify the temporary profile. Before the edit, it should identify the visitor as anonymous.
5. Django redirects `/login/`, `/accounts/login/`, `/accounts/register/`, `/logout`, and `/admin/login/` to MediaWiki.

Automated middleware tests are in `apps/mediawiki_auth/tests.py` and mock the MediaWiki API. Apply migrations additively with `python manage.py migrate` after the database backups are secured.
