# Universal Deployment Engineering

## Phase 5: Domains, DNS and HTTPS

**Status:** Complete\
**Date:** 19 November 2026\
**Project:** `nasibi.duckdns.org`

## Goal

Make the Django application reachable through a real hostname over
HTTPS, with HTTP redirected to HTTPS and certificate renewal configured.

## 1. Domain and DNS

-   Hostname: `nasibi.duckdns.org`
-   VPS public IPv4: `138.68.187.190`
-   DNS A records map a hostname to an IPv4 address.
-   A CNAME maps one hostname to another hostname, not directly to an
    IP.
-   DNS resolves the hostname. It does not redirect a browser or
    configure Nginx.
-   Nginx uses the requested hostname and its `server_name`
    configuration to select a server block.
-   Django separately checks the hostname against `ALLOWED_HOSTS`.

**DNS check:**

``` bash
dig +short nasibi.duckdns.org A
```

Expected result during this deployment:

``` text
138.68.187.190
```

The practical used one hostname because there is no separate
frontend/API service to deploy. The roadmap's example of using a main
domain and API subdomain was deliberately reduced in scope.

## 2. Request path

``` text
Browser
  -> DNS resolves nasibi.duckdns.org
  -> VPS public IP
  -> Nginx
  -> Gunicorn at 127.0.0.1:8000
  -> Django
  -> PostgreSQL
```

The browser does not connect directly to PostgreSQL. Nginx receives web
traffic and proxies application requests to Gunicorn.

## 3. HTTP, HTTPS and TLS

-   HTTP sends application data without TLS protection.
-   HTTPS is HTTP carried over TLS.
-   TLS provides confidentiality, integrity and server authentication.
-   TCP provides reliable, ordered transport. Its connection handshake
    is `SYN -> SYN-ACK -> ACK`.
-   TLS has its own handshake. Do not confuse the TCP handshake with the
    TLS handshake.
-   A browser checks that the certificate matches the hostname, is
    within its validity period and chains to a trusted certificate
    authority.
-   The certificate authority helps establish that the certificate is
    valid for the hostname.
-   SHA-256 is a hash function. It is not itself a digital signature.

## 4. Nginx and HTTPS

Nginx is configured to: - Listen for HTTPS traffic on port `443`. - Use
the Let's Encrypt certificate and private key. - Proxy application
requests to `127.0.0.1:8000`. - Pass the original host and forwarded
protocol information to Django. - Redirect HTTP requests on port `80` to
HTTPS.

Certificate files:

``` text
/etc/letsencrypt/live/nasibi.duckdns.org/fullchain.pem
/etc/letsencrypt/live/nasibi.duckdns.org/privkey.pem
```

Active Nginx configuration inspected during the deployment:

``` text
/etc/nginx/sites-available/default
```

Important proxy header:

``` nginx
proxy_set_header X-Forwarded-Proto $scheme;
```

Django trusts this header through:

``` python
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

This trust is appropriate when Nginx is the trusted proxy and sets the
header. Gunicorn should not be exposed directly to untrusted clients.

## 5. Certificate and renewal

Certbot was installed through APT, including its Nginx integration. It
was not installed through Snap.

Useful commands:

``` bash
sudo apt install certbot
certbot --version
sudo systemctl status certbot.timer
sudo certbot renew --dry-run
```

Verified results: - Certbot version: `2.9.0`. - The Let's Encrypt
certificate was issued and installed for `nasibi.duckdns.org`. -
`certbot.timer` was enabled and active. - The renewal simulation
completed successfully with:
`Congratulations, all simulated renewals succeeded`.

The dry run tests the renewal process without replacing the live
certificate.

## 6. HTTP-to-HTTPS redirect

The first HTTP visit can receive a permanent `301` redirect from Nginx.
The browser then makes the request over HTTPS.

Check the redirect:

``` bash
curl -sSI http://nasibi.duckdns.org/admin/login/
```

Verified response:

``` http
HTTP/1.1 301 Moved Permanently
Location: https://nasibi.duckdns.org/admin/login/
```

Check the HTTPS endpoint:

``` bash
curl -sSI https://nasibi.duckdns.org/admin/login/
```

Verified response status:

``` http
HTTP/1.1 200 OK
```

Curl completed the HTTPS request without a certificate verification
error.

## 7. Secure cookies

Production settings in `config/settings/production.py`:

``` python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
```

What they do:

-   `SESSION_COOKIE_SECURE`: the browser sends the session cookie only
    over HTTPS.
-   `CSRF_COOKIE_SECURE`: the browser sends the CSRF cookie only over
    HTTPS.
-   `SESSION_COOKIE_HTTPONLY`: JavaScript cannot read the session
    cookie.
-   `CSRF_COOKIE_HTTPONLY = False`: JavaScript can read the CSRF cookie
    when the frontend needs to obtain the CSRF token and send it in a
    request header such as `X-CSRFToken`.

The HTTPS login response was observed setting a CSRF cookie with the
`Secure` attribute. The session cookie settings are configured, but a
session cookie was not directly observed in that login-page response.

## 8. HSTS

Production settings:

``` python
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
```

The HTTPS response returned:

``` http
Strict-Transport-Security: max-age=3600
```

HSTS tells a browser that has received the header over HTTPS to use
HTTPS for later visits during the policy period. Here, `3600` means one
hour.

HSTS does not secure the first HTTP visit when the browser has no cached
policy. A browser preload list can provide protection before the first
visit, but this deployment has not enabled preload.

## 9. Django production checks

The production settings use:

``` text
config.settings.production
```

Run the Django system check from the backend directory with the virtual
environment active:

``` bash
python manage.py check --settings=config.settings.production
```

Verified result:

``` text
System check identified no issues (0 silenced).
```

This checks Django configuration consistency. It does not, by itself,
prove that Gunicorn is running or that the live HTTPS response contains
the expected headers.

## 10. Useful commands from this phase

  ----------------------------------------------------------------------------------------------------
  Purpose                             Command
  ----------------------------------- ----------------------------------------------------------------
  Resolve the hostname                `dig +short nasibi.duckdns.org A`

  Check Nginx configuration           `sudo nginx -t`

  Check HTTPS response headers        `curl -sSI https://nasibi.duckdns.org/admin/login/`

  Check HTTP redirect                 `curl -sSI http://nasibi.duckdns.org/admin/login/`

  Check Certbot version               `certbot --version`

  Check renewal timer                 `sudo systemctl status certbot.timer`

  Test certificate renewal            `sudo certbot renew --dry-run`

  Check Django production settings    `python manage.py check --settings=config.settings.production`

  Inspect Gunicorn processes          `ps -ef \| grep '[g]unicorn'`
  ----------------------------------------------------------------------------------------------------

Run the Django command from the backend directory with the project's
virtual environment active. Run the Nginx and Certbot administration
commands on the VPS.

## 11. Phase 5 completion evidence

  -----------------------------------------------------------------------
  Requirement                         Result
  ----------------------------------- -----------------------------------
  Hostname resolves to the VPS        Verified with `dig`

  Nginx serves the hostname           Verified

  Real HTTPS certificate installed    Verified

  HTTPS endpoint responds             HTTP `200 OK`

  HTTP redirects to HTTPS             HTTP `301` with HTTPS `Location`

  Certificate renewal process         Dry run succeeded

  Secure cookie settings              Configured; CSRF `Secure` attribute
                                      observed

  HSTS                                Header observed with `max-age=3600`

  Django production system check      Passed
  -----------------------------------------------------------------------

**Phase 5 exit criterion met:** the application responds over HTTPS on
`nasibi.duckdns.org` without a certificate verification error, and HTTP
redirects to HTTPS.

## 12. Git and secrets

From the local repository `~/development-engineering`, review the
documentation change:

``` bash
git status
git diff
```

Stage only the intended roadmap/documentation files, then commit and
push:

``` bash
git add <intended-files>
git diff --cached
git commit -m "Document phase 5 domain and HTTPS deployment"
git push
```

Never commit `.env`, `.venv`, the DuckDNS token, database passwords,
Django `SECRET_KEY`, private keys or other credentials.

## Next phase

**Phase 6: Static and Media Files.**

Do not begin it until this Phase 5 record is saved in the repository and
pushed. Phase 6 will be handled separately, in roadmap order.
