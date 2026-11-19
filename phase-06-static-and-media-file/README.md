# Phase 6: Static and Media Files

**Project:** Universal Deployment Engineering  
**Phase:** 6  Static and Media Files  
**Checkpoint date:** 19 November 2026  
**Status:** Partially complete  concepts and static-file deployment completed; external object storage deferred.

---

## 1. Goal

Serve frontend assets and user uploads correctly in production.

This phase covers Django static files, user-uploaded media, Nginx static serving, object storage, and public/private file access.

## 2. Concepts learned

### 2.1 Static files vs media files

- Static files are application assets such as CSS, JavaScript, fonts and logos.
- Media files are uploaded by users, such as profile photos and documents.

### 2.2 Django static-file settings

- `STATIC_URL`: URL prefix used to access static files.
- `STATIC_ROOT`: destination directory for collected static files.
- `collectstatic`: collects static files from Django applications into `STATIC_ROOT`.

### 2.3 Production static-file serving

Nginx serves collected static files directly instead of sending every static-file request through Django and Gunicorn.

This reduces unnecessary application-server work.

### 2.4 Storage backends and STORAGES

A storage backend handles saving, opening, retrieving and deleting files.

Django's `STORAGES` setting selects the storage backend.

Important aliases:

- `default`: user-uploaded files.
- `staticfiles`: collected static files.

### 2.5 FileField and database storage

A Django `FileField` delegates file operations to the configured storage backend.

The database stores the file's name or reference, while the storage system stores the actual file bytes.

### 2.6 Object storage

Object storage keeps files outside the application server.

Important terminology:

- Bucket: a container for stored objects.
- Object: an individual stored file.
- Object key: the name used to identify an object.

Object storage allows uploaded files to remain available independently of the VPS disk.

### 2.7 Public and private media

- Public files can be accessed by anyone with the appropriate URL.
- Private files require authorization before access.

Nginx's `internal` directive blocks direct external requests to a location. It does not authenticate users or check application permissions.

Django must authorize the user before allowing access, for example through an internal Nginx redirect.

---

## 3. Practical work completed: Static files

### Environment

- Operating system: Ubuntu 24.04
- VPS provider: DigitalOcean
- Domain: `nasibi.duckdns.org`
- Django production settings: `config.settings.production`

### Django configuration

The backend uses:

```python
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

The resolved static directory is:

```text
/home/deploy/apps/phase-03-postgresql-production-deployment/backend/staticfiles/
```

### Nginx configuration

The `/static/` location uses an alias pointing to the collected static directory:

```nginx
location /static/ {
    alias /home/deploy/apps/phase-03-postgresql-production-deployment/backend/staticfiles/;
}
```

The Nginx alias matches Django's `STATIC_ROOT`.

### Collecting static files

Command executed:

```bash
python manage.py collectstatic --noinput --settings=config.settings.production
```

Recorded result:

```text
0 static files copied
130 unmodified
```

This showed that the collected files were already up to date.

### Verification

Tested the Django admin CSS file:

```bash
curl -I https://nasibi.duckdns.org/static/admin/css/base.css
```

Recorded result:

```text
HTTP/1.1 200 OK
```

The response was served by Nginx with CSS content type.

**Conclusion:** Production static-file serving through Nginx was successfully configured and verified.

---

## 4. Media storage: Learning completed, practical deferred

The project inspection found no matching `FileField`, `ImageField`, `MEDIA_ROOT`, `MEDIA_URL` or `STORAGES` configuration in the searched Python files.

The learner explicitly chose not to add a demonstration upload model, application, view or endpoint to the actual project.

External object storage was discussed, but implementation was deferred because the learner does not currently have the budget for a paid storage provider.

No provider was selected or configured.

The following work remains outstanding:

- Select an affordable object-storage provider.
- Create a bucket and access credentials.
- Install and configure the appropriate Django storage backend.
- Store credentials securely in environment variables.
- Upload a real test file.
- Retrieve the uploaded file successfully.
- Verify that the upload does not depend on the VPS local disk.

No storage package, bucket, credentials or object-storage configuration was created during this phase.

**Important:** The external upload and retrieval requirements have not been verified. They must not be reported as completed.

---

## 5. Phase 6 assessment

| Requirement | Result |
|---|---|
| Understand static vs media files | Completed |
| Understand production static-file serving | Completed |
| Configure collected static files | Completed |
| Serve static files through Nginx | Verified |
| Understand object storage | Covered |
| Understand public vs private media | Covered |
| Move uploads to external object storage | Deferred |
| Verify external upload and retrieval | Not tested |

### Final status

Phase 6 learning and static-file deployment are complete.

The external object-storage practical is deferred until the learner has a production budget.

The formal Phase 6 exit criteria are therefore not fully satisfied.

---

## 6. Next roadmap phase

**Phase 7: Docker and Docker Compose**

The next phase will cover:

- What Docker solves.
- Images and containers.
- Dockerfiles.
- Building and running containers.
- Ports, volumes and networks.
- Environment variables.
- Docker Compose and multiple services.
- Persistent PostgreSQL storage.

Do not restart Phase 6 lessons or implement paid object storage unless the learner explicitly requests it.

---

## 7. Git checkpoint

After adding this documentation:

```bash
git status
git add docs/phase-06-static-and-media-files.md
git diff --cached
git commit -m "docs: record phase 6 static and media progress"
git push
```

Only stage the intended documentation. Never commit `.env`, `.venv`, credentials, tokens or other secrets.