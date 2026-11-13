# Phase 4  Application Serving, Gunicorn and Nginx

## Goal

Understand and deploy the production serving layer between the internet and Django using Gunicorn and Nginx.

## What I Learned

### 1. WSGI and Gunicorn
- What WSGI does and how Django exposes its application through `config.wsgi`.
- Why Gunicorn is used to run Django in production.
- Gunicorn master and worker processes.
- Binding Gunicorn to `127.0.0.1:8000`.
- Inspecting processes with `pgrep` and `ps`.
- Stopping Gunicorn with `kill -TERM`.
- Graceful shutdown and the `--graceful-timeout` option.

### 2. Nginx
- Nginx as a web server and reverse proxy.
- Nginx location matching.
- Forwarding dynamic requests to Gunicorn using `proxy_pass`.
- Forwarding request headers using `proxy_set_header`.
- Serving static files directly from the filesystem using `alias`.

### 3. Static File Permissions
- Linux directory traversal permissions.
- Nginx worker access through the `www-data` user.
- ACL permissions using `setfacl` and `getfacl`.
- Diagnosing and fixing a static file permission error (403).

### 4. Logging and Error Diagnosis
- Difference between access logs and error logs.
- What stdout and stderr mean.
- How to interpret HTTP status codes and Python tracebacks.
- Why an HTTP 500 response does not automatically identify the underlying Python error.

## Request Architecture

**Dynamic requests:**

Browser → Nginx → Gunicorn → Django → Response

**Static requests:**

Browser → Nginx → Static files on disk → Response

## Practical Implementation

- Installed and ran Gunicorn.
- Configured Nginx as a reverse proxy.
- Configured Nginx to serve Django static files.
- Fixed filesystem permissions using ACL.
- Verified static file delivery with HTTP 200.
- Stopped Gunicorn and verified that dynamic requests returned HTTP 502.
- Restarted Gunicorn and verified that Django admin returned HTTP 200 without restarting Nginx.
- Practised process inspection, graceful shutdown and error diagnosis.

## Key Understanding

Nginx and Gunicorn are separate processes.

Nginx forwards dynamic requests to the configured Gunicorn address (`127.0.0.1:8000`). If Gunicorn stops, dynamic requests fail because the upstream is unavailable.

Static files continue working because Nginx serves them directly from the filesystem.

Restarting Gunicorn does not require restarting or reconfiguring Nginx, provided Gunicorn returns on the configured address and port.

## Phase 4 Result

**Status: Completed**

The production request path from Nginx through Gunicorn to Django was configured and tested successfully.

The original exit criterion was demonstrated: stopping and restarting Gunicorn does not require touching Nginx.