# Phase 1 VPS Lab

Real Linux server practice using an Ubuntu 24.04 DigitalOcean VPS.

## Completed

- Connected using an Ed25519 SSH key
- Updated and upgraded server packages
- Created non-root `deploy` user
- Added `deploy` to the sudo group
- Configured SSH key access for `deploy`
- Disabled root SSH login
- Disabled password authentication
- Verified public-key authentication
- Enabled UFW
- Allowed only SSH (`22/tcp`)
- Installed and enabled Fail2Ban for SSH
- Inspected listening ports with `ss`
- Inspected memory with `free`
- Inspected disk usage with `df`
- Inspected processes and CPU usage with `top`
- Executed commands remotely through SSH

## Current SSH Policy

```text
permitrootlogin no
pubkeyauthentication yes
passwordauthentication no
```

## Public Network Access

```text
22/tcp → SSH
```

Other observed port `53` listeners are bound to localhost for local DNS resolution.

## Remaining

- Practice copying a file with `scp`
- Complete the Phase 1 exit check
