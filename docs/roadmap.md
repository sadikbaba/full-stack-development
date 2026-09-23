# Universal Deployment Engineering Roadmap

Practical deployment engineering for a full-stack and AI engineer. Not built around VTU, e-commerce, SaaS, or any single app. The goal is production capability, not DevOps/SRE specialization.

---

## Baseline Audit

**Already solid, light review only:** Python, Django, DRF, PostgreSQL basics, React, TypeScript, REST APIs, auth, backend security, external APIs, Redis and Celery basics, testing, Git/GitHub.

**Genuinely new:** Linux server administration, SSH, production Django settings, Gunicorn, Nginx, domains/DNS, HTTPS/TLS, Docker and Compose, Redis/Celery in production, process management, cloud deployment, CI/CD, logging, monitoring, backups, production security, React production deployment, AI service deployment, systematic production troubleshooting.

**Dependency order:**
- Linux and SSH come first, everything else runs on top of a server.
- Dev vs prod config depends on nothing else and unlocks Postgres, Gunicorn, Nginx.
- Gunicorn depends on a working Django app with production settings.
- Nginx depends on Gunicorn running.
- Domains/HTTPS depend on Nginx.
- Docker is an alternate packaging layer, can be learned right after dev vs prod config, independent of Nginx/Gunicorn done manually first (both paths are taught, manual first, then Docker).
- Redis and Celery depend on the app already running in some deployable form.
- CI/CD depends on there being a real deployment process to automate.
- Logging, monitoring, backups, security are layered on top of a working deployment.
- Troubleshooting depends on knowing every layer above.

**Independent, any order once prerequisites are met:** Logging, Monitoring, Backups.

**Delayed on purpose, not core:** Kubernetes, Terraform, advanced AWS architecture, service meshes, multi-region infrastructure, advanced Nginx/Docker internals, advanced Linux administration, advanced observability engineering, advanced database administration. Introduced later only if a real project needs them.

**Learning depth used throughout:**
- Level 1, Understand: what it is, why it exists, what problem it solves, its main risks.
- Level 2, Use: configure it, deploy it, connect it, troubleshoot common failures, maintain it.
- Level 3, Deep expertise: not required for Nginx, Docker, Redis, cloud platforms, CI/CD, monitoring, or Linux administration. Deep expertise stays in Python, Django, DRF, PostgreSQL, React, TypeScript, AI/LLM engineering.

---

## Phase 1: Linux Fundamentals and SSH

**Goal:** Operate a Linux server well enough to run a production application on it.

**Concepts:**
- Filesystem, directories, paths, users, groups, permissions, ownership
- Processes, services, ports, package management, environment variables
- systemctl, journalctl, basic networking commands
- Disk, memory, CPU inspection, basic firewall concepts
- SSH, key pairs, why keys beat passwords, connecting, copying files, remote commands
- Root vs normal users, disabling unnecessary access

**Prerequisites:** None.

**Practical project:** Provision a Linux server (VPS), connect only by SSH key, create a non-root deploy user, install required packages, and inspect running processes, ports, and resource usage.

**Skills gained:** Comfortable operating a remote Linux server for real work.

**What NOT to study yet:** Django deployment, Docker, Nginx.

**Exit criteria:** Can SSH into a fresh server, harden access to key-only, and explain what every open port is for.

---

## Phase 2: Development vs Production Configuration

**Goal:** Understand why `manage.py runserver` is not a deployment strategy and configure Django correctly for production.

**Concepts:**
- Local dev vs staging vs production
- DEBUG, SECRET_KEY, ALLOWED_HOSTS, CORS/CSRF config
- Environment variables, .env, secrets, never committing them
- Public vs private configuration, especially the trap of assuming frontend env vars are private
- .gitignore discipline

**Prerequisites:** Phase 1.

**Practical project:** Take an existing Django app, split settings into dev and production, move all secrets to environment variables, and confirm DEBUG is off and ALLOWED_HOSTS is correct in production mode.

**Skills gained:** Can configure a Django app safely for production without copying a random .env example blindly.

**What NOT to study yet:** Gunicorn, Nginx, this is config only.

**Exit criteria:** Can explain, for each production setting, what breaks if it is misconfigured.

---

## Phase 3: PostgreSQL Production Deployment

**Goal:** Run PostgreSQL as a real production database connected to Django.

**Concepts:**
- Installing PostgreSQL, creating databases and users, permissions
- Connection config: host, port, database URL
- Django to PostgreSQL, running production migrations safely
- Basic database security, connection limits
- Backups and restore at a practical level (deepened in Phase 13)

**Prerequisites:** Phase 1, 2.

**Practical project:** Install PostgreSQL on the server, create a dedicated database and user with least-privilege permissions, connect Django to it via environment variables, and run migrations.

**Skills gained:** Can stand up a production Postgres instance and connect an app to it safely.

**What NOT to study yet:** Advanced Postgres internals or administration beyond what an engineer needs.

**Exit criteria:** App runs against production Postgres with migrations applied and no hardcoded credentials anywhere in code.

---

## Phase 4: Application Serving, Gunicorn and Nginx

**Goal:** Understand and deploy the real serving layer between the internet and Django.

**Concepts:**
- Why the dev server is unsafe for production, what WSGI is, what an application server does
- Gunicorn: workers, binding to a port, restarting, graceful shutdown, logs
- Nginx: reverse proxy, server blocks, proxying to Gunicorn, serving static files, headers
- Architecture: Internet to Nginx to Gunicorn to Django

**Prerequisites:** Phase 2, 3.

**Practical project:** Run the Django app under Gunicorn, put Nginx in front of it as a reverse proxy, and confirm requests flow correctly end to end.

**Skills gained:** Can explain and deploy the full request path from Nginx to Gunicorn to Django.

**What NOT to study yet:** Advanced Nginx configuration beyond a working reverse proxy.

**Exit criteria:** Killing and restarting Gunicorn does not require touching Nginx, and the reasoning why is clear.

---

## Phase 5: Domains, DNS and HTTPS

**Goal:** Make the app reachable at a real domain, securely.

**Concepts:**
- Domain names, DNS, A records, CNAME, subdomains (example.com vs api.example.com)
- How a domain resolves to the server running the app
- HTTP vs HTTPS, TLS, certificates, certificate authorities, renewal
- HTTP to HTTPS redirects, secure cookies, HSTS concept

**Prerequisites:** Phase 4.

**Practical project:** Point a domain and an api subdomain at the server, configure Nginx to serve both, and enable HTTPS with a real certificate, redirecting all HTTP traffic.

**Skills gained:** Can take a bare server to a domain with working HTTPS.

**What NOT to study yet:** Advanced cryptography, this is applied TLS only.

**Exit criteria:** The app is reachable over HTTPS on a real domain with no certificate warnings.

---

## Phase 6: Static and Media Files

**Goal:** Serve frontend assets and user uploads correctly in production.

**Concepts:**
- Django static files vs media uploads
- Production static file serving through Nginx
- CDN and object storage concepts, when the app server should not own file storage forever
- Public vs private files, file permissions

**Prerequisites:** Phase 5.

**Practical project:** Configure collected static files to be served by Nginx and move user-uploaded media to object storage instead of local disk.

**Skills gained:** Can explain why uploaded files should not live permanently on the app server.

**What NOT to study yet:** Full CDN provider deep dives, concept level is enough here.

**Exit criteria:** Static assets and uploads both load correctly in production with no app-server disk dependency for uploads.

---

## Phase 7: Docker and Docker Compose

**Goal:** Package and run the app as containers, understanding the model, not just the commands.

**Concepts:**
- What problem Docker solves, images, containers, Dockerfile, build, run
- Ports, volumes, networks, environment variables, container lifecycle, logs
- Docker Compose: multiple services (Django, Postgres, Redis, Celery) wired together
- Service dependencies, persistent volumes for the database, restarting services

**Prerequisites:** Phase 2, 3 (Docker can be learned in parallel with Phase 4 to 6, but needs config and database understanding first).

**Practical project:** Containerize Django and PostgreSQL with docker-compose, with a persistent volume for the database and environment variables passed in correctly.

**Skills gained:** Can containerize a real backend and explain what each Docker primitive is for.

**What NOT to study yet:** Kubernetes or any orchestration beyond Compose.

**Exit criteria:** Can tear down and rebuild the whole stack with docker-compose and get back to a working state with no manual steps.

---

## Phase 8: Redis and Celery in Production

**Goal:** Run background jobs reliably in production.

**Concepts:**
- Redis server: connections, auth, host/port, TTL, memory, persistence basics, security
- Redis as a Celery broker
- Celery worker processes, task execution, retries, failed tasks
- Celery Beat for scheduled/periodic tasks
- Task idempotency (ties back to earlier backend work), worker logs, basic task monitoring
- Why background jobs exist separately from the HTTP request lifecycle

**Prerequisites:** Phase 7 (or a working manual deployment from Phase 4 to 6).

**Practical project:** Add Redis and a Celery worker to the docker-compose stack, move one real task (e.g. sending email or an AI call) to the background, and add a Celery Beat scheduled task.

**Skills gained:** Can deploy and operate a real background job pipeline.

**What NOT to study yet:** Advanced Celery patterns like chains and chords, only if a real need appears.

**Exit criteria:** Can kill the worker, watch it restart, and confirm no tasks are silently lost.

---

## Phase 9: Process Management

**Goal:** Keep every production process alive and recoverable.

**Concepts:**
- Processes and services, systemd basics, service files
- Automatic restart, startup on boot, graceful restart
- Managing Django/Gunicorn, Celery, Celery Beat, Nginx, PostgreSQL, Redis as services (or as Docker services with restart policies)

**Prerequisites:** Phase 4, 8.

**Practical project:** Write systemd service files (or Docker restart policies) for every process in the stack, reboot the server, and confirm everything comes back up on its own.

**Skills gained:** Can guarantee a server reboot does not take the app down permanently.

**What NOT to study yet:** Deep systemd internals beyond what is needed to keep services alive.

**Exit criteria:** A full server reboot results in a fully working app with zero manual restarts.

---

## Phase 10: Full-Stack Cloud Deployment

**Goal:** Combine everything so far into one deployed full-stack application.

**Concepts:**
- VPS provisioning, resources, storage, networking basics, firewall
- React production build, static hosting/CDN, environment variables, API URLs
- SPA routing on static hosts, cache invalidation, asset versioning
- Connecting the React build to the Django REST API over HTTPS

**Prerequisites:** Phase 1 to 9.

**Practical project:** Deploy a real full-stack app: React build on static hosting/CDN, Django REST API behind Nginx and Gunicorn, PostgreSQL, Redis, Celery, all under a real domain with HTTPS.

**Skills gained:** Can take a full-stack app from "works on my laptop" to a real deployed system end to end.

**What NOT to study yet:** CI/CD automation, that is next.

**Exit criteria:** A fresh visitor can use the deployed app exactly as they would a normal production product, no manual steps visible.

---

## Phase 11: CI/CD and Deployment Strategies

**Goal:** Automate testing and deployment instead of deploying by hand every time.

**Concepts:**
- CI vs CD, GitHub Actions basics
- Automated tests, build process, deployment triggers, environment secrets in CI
- Deployment failures, rollback concepts, safe migration handling
- Manual vs automated deployment, rolling and blue/green concepts at a conceptual level, zero-downtime ideas
- Workflow: push to GitHub, CI runs tests, build, deploy to production

**Prerequisites:** Phase 10.

**Practical project:** Set up a GitHub Actions pipeline that runs the test suite on every push and deploys automatically to the server on merge to main, including a safe migration step.

**Skills gained:** Can build a real CI/CD pipeline and reason about rollback if a deploy goes wrong.

**What NOT to study yet:** Advanced deployment platforms or strategies beyond what one clean pipeline needs.

**Exit criteria:** A broken test blocks deployment automatically, and a passing one deploys with no manual intervention.

---

## Phase 12: Logging and Monitoring

**Goal:** Know what the system is doing without SSHing in and guessing.

**Concepts:**
- Application logs, Nginx logs, Gunicorn logs, Celery logs, error levels, structured logging, request identifiers
- Difference between application log, transaction record, audit record
- Uptime, CPU, memory, disk, error rate, response time, request rate
- Database, Redis, and Celery worker health checks, health-check endpoints
- Difference between logging, monitoring, and alerting

**Prerequisites:** Phase 10.

**Practical project:** Centralize logs from all services, add a health-check endpoint, and set up basic monitoring dashboards with one real alert (e.g. error rate spike or service down).

**Skills gained:** Can diagnose system state from logs and dashboards without guessing.

**What NOT to study yet:** Full observability engineering (tracing, advanced metrics pipelines).

**Exit criteria:** Given a simulated failure, can identify it from logs/monitoring alone before touching the server directly.

---

## Phase 13: Backups, Recovery and Production Security

**Goal:** Make sure data survives failure and the deployment is not trivially exploitable.

**Concepts:**
- PostgreSQL backups with pg_dump, restore, backup frequency, retention, backup storage
- Uploaded-file backups, disaster recovery thinking
- The principle that a backup is not trustworthy until restore has been tested
- SSH security, firewall, HTTPS, secure cookies, least privilege, exposed ports
- Dependency and server updates, CORS/CSRF, security headers, Django production security settings, secret rotation
- The two standing questions: what is exposed to the internet, and what happens if this credential leaks

**Prerequisites:** Phase 3, 5, 9.

**Practical project:** Automate nightly database backups, actually restore one into a fresh environment to prove it works, and run a security pass on the whole deployment (firewall rules, exposed ports, headers, secrets).

**Skills gained:** Can prove backups work, not just assume it, and can audit a live deployment for basic security gaps.

**What NOT to study yet:** Penetration testing or advanced cybersecurity.

**Exit criteria:** A simulated database loss is fully recovered from backup, and a security checklist pass finds no open critical gaps.

---

## Phase 14: Deploying AI Applications

**Goal:** Deploy the AI-specific parts of a full-stack app safely and reliably.

**Concepts:**
- Backend to AI provider communication, LLM API keys handled as secrets, never in frontend code
- Timeouts, retries, rate limits for AI calls
- Background AI jobs for anything slow (ties back to Phase 8)
- Token/cost monitoring concepts, logging AI failures distinctly from normal errors
- Local model deployment concepts and resource considerations, at a practical level only

**Prerequisites:** Phase 8, 13.

**Practical project:** Add an AI feature (React to Django API to AI provider or local model) with the API key stored as a secret, timeouts and retries on the call, the call itself running as a background job, and failures logged distinctly.

**Skills gained:** Can deploy an AI-integrated feature without leaking keys or letting a slow AI call block a request.

**What NOT to study yet:** GPU infrastructure engineering.

**Exit criteria:** Killing the AI provider connection mid-request degrades gracefully and is visible in logs, not a silent failure.

---

## Phase 15: Production Troubleshooting

**Goal:** Debug production systematically instead of guessing.

**Concepts:**
- Layered debugging: DNS, network, firewall, Nginx, Gunicorn, Django, Redis/PostgreSQL, external API
- Common failures: 502, 404, 403, 500, connection refused, DB connection errors, permission errors, DNS problems, certificate problems, failed migrations, missing env vars, container failures, Celery failures, static files not loading, disk full, memory exhaustion
- The rule: read the actual error first, then find the failing layer, never randomly change config

**Prerequisites:** Phase 1 to 14 (every layer above must exist to practice diagnosing it).

**Practical project:** Deliberately break five different layers of the stack (one at a time, e.g. stop Postgres, misconfigure an env var, break Nginx config) and diagnose and fix each using logs and the layered model, not guessing.

**Skills gained:** Can walk a production outage from symptom to root cause using a repeatable method.

**What NOT to study yet:** N/A, this is a capstone skill applied everywhere from here on.

**Exit criteria:** Given an unannounced simulated failure, correctly identifies the failing layer within a few minutes using logs alone.

---

## Phase 16: Deployment Architecture and Documentation

**Goal:** See the whole system as one architecture and make it operable by someone other than you.

**Concepts:**
- Full architecture: Internet to HTTPS to Nginx to Gunicorn to Django to PostgreSQL/Redis/external APIs, with Celery off Redis for background jobs, and React build served via static hosting/CDN to the API
- Deployment documentation: README, setup, environment variables, deployment steps, architecture diagram, database setup, migrations, backup/restore procedure, troubleshooting, rollback procedure
- Git and deployment discipline: branches, PRs, deployment branches, meaningful commits, secret prevention, release tags, rollback through Git
- The principle that a deployment only one person remembers is folklore, not engineering

**Prerequisites:** All prior phases.

**Practical project (capstone):** Deploy a full real application combining React, TypeScript, Django, DRF, PostgreSQL, Redis, Celery, an external or AI API, Docker, Nginx, Gunicorn, HTTPS, a real domain, CI/CD, logging, monitoring, and backups. Document it fully enough that someone else could deploy and operate it from the README alone.

**Skills gained:** Can take any real application from local development to a documented, reliable production deployment end to end.

**Exit criteria:** Hand the README to someone unfamiliar with the project and have them successfully deploy or restore it using only the docs.

---

## Final Roadmap Requirements

### Learning Timeline
- Phases 1 to 3 (Linux, SSH, config, Postgres): foundation layer
- Phases 4 to 6 (Gunicorn, Nginx, domains, HTTPS, static/media): the core serving layer
- Phases 7 to 9 (Docker, Redis/Celery, process management): packaging and reliability layer
- Phase 10 (full-stack deployment): first real integrated deployment
- Phases 11 to 13 (CI/CD, logging/monitoring, backups/security): production-operations layer
- Phase 14 (AI deployment): domain extension once the base is solid
- Phase 15 (troubleshooting): applied continuously from here on
- Phase 16: capstone

### Portfolio Checklist
- [ ] Phase 1 to 3: hardened Linux server with Postgres running and correct production config
- [ ] Phase 4 to 6: Django served through Gunicorn and Nginx on a real domain with HTTPS
- [ ] Phase 7 to 9: dockerized stack with Redis, Celery, and process restart guarantees
- [ ] Phase 10: full-stack deployment, React plus Django plus Postgres, live on a domain
- [ ] Phase 11: working CI/CD pipeline with automated tests and deploy
- [ ] Phase 12 to 13: logging, monitoring, tested backup/restore, security pass documented
- [ ] Phase 14: AI feature deployed with secrets, timeouts, retries, and background execution
- [ ] Phase 16: capstone deployment with full documentation

### GitHub Project Checklist (per repo)
- [ ] README with architecture diagram and setup instructions that work from a fresh clone
- [ ] .gitignore correctly excluding secrets and build artifacts
- [ ] Documented environment variables (names and purpose, not values)
- [ ] Deployment and rollback instructions
- [ ] Backup and restore procedure documented
- [ ] CI badge showing tests passing

### Interview Preparation Checklist
- [ ] Can explain the full request path from Nginx to Gunicorn to Django
- [ ] Can explain why the Django dev server is unsafe for production
- [ ] Can explain how HTTPS is obtained and renewed
- [ ] Can explain the Docker Compose stack and what each service does
- [ ] Can explain how Celery and Redis fit into background processing
- [ ] Can walk through diagnosing a 502 error layer by layer
- [ ] Can explain a real backup/restore test they performed
- [ ] Can explain how secrets are managed and rotated

### Common Interview Questions
- Walk through what happens from a browser request hitting your domain to a response coming back.
- Why use Gunicorn instead of the Django development server in production?
- How do you handle a failed database migration during deployment?
- How would you diagnose a 502 Bad Gateway error?
- How do you keep API keys out of a frontend build?
- Describe your CI/CD pipeline and what happens if a test fails.
- How do you know a backup actually works?
- How would you deploy a feature that calls an external AI API safely?

### Free Learning Resources
- DigitalOcean Community Tutorials, strong practical Linux and deployment guides
- Django deployment docs (docs.djangoproject.com/en/stable/howto/deployment)
- Nginx docs (nginx.org/en/docs)
- Gunicorn docs (docs.gunicorn.org)
- Docker docs (docs.docker.com)
- Let's Encrypt docs (letsencrypt.org/docs), for HTTPS certificates
- GitHub Actions docs (docs.github.com/actions)
- Redis docs (redis.io/docs) and Celery docs (docs.celeryq.dev)

### Books (optional deep dives)
- The Site Reliability Workbook (Google), for production operations thinking, read selectively, not cover to cover
- Two Scoops of Django (Daniel and Audrey Feldroy), for production Django settings patterns

### Practice Websites
- A real VPS provider sandbox (DigitalOcean, Linode, Hetzner) for hands-on server practice
- Play with Docker (labs.play-with-docker.com), for a free Docker sandbox
- KillerCoda or Katacoda-style Linux scenario sites for troubleshooting practice

### Advanced Topics for After This Roadmap
- Kubernetes and container orchestration
- Infrastructure as code (Terraform)
- Multi-region and high-availability architecture
- Advanced observability: distributed tracing, metrics pipelines
- Advanced database administration and replication

---

## Non-Negotiables

- Never skip the hands-on server or Docker step for a phase, reading about it is not the same as doing it.
- Never move to the next phase until the current deployment actually works and you can rebuild the key step from memory.
- Always read the actual error and identify the failing layer before changing any configuration.
- Never commit a secret, and never assume a frontend environment variable is private.