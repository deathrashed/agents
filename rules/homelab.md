# Homelab

Sources: MEM (`areas/homelab-access-map.md`, verified 2026-11-08).

Full map with addresses, ports, shares and services: cachy
`~/downloads/memory/areas/homelab-access-map.md` (Mac: `/Volumes/home/downloads/memory/...`)
and `~/docker/HOMELAB-GUIDE.md` / `ACCESS-AND-STATUS.md` on cachy. Read it
before networking, mounts, Docker or SSH work. Never copy addresses, hostnames
or ports into this public repo.

- Both machines are reachable (`ssh mac` from cachy; LAN at home, Tailscale
  away). Never say you can't access cachy or the Mac: run the command and
  report the real error text. Run as user `rd`. [MEM]
- Never mount or unmount in loops, and never `umount -f` anything under
  `/mnt/mac/*` or `/Volumes/*`. A watcher manages those mounts; if the Mac is
  asleep, wait and they recover. [MEM]
- Hermes runs natively on cachy. Don't start the Docker `hermes` copy. [MEM]
- Don't start all stopped containers (RAM is tight). Media containers start
  only via `mac-media@<name>.service` when the Mac's storage is mounted. [MEM]
- Don't push `deathrashed/tailscale-policy` without rd's OK: a push to main
  applies live. [MEM]
- Credentials live in `~/docker/*/.env`, `/etc/samba/creds/` and
  `~/.config/tailscale/keys/`. Know where they are; never print them (see
  rule 7 in `main.md`). [MEM]
- Troubleshooting order: `tailscale status` / `tailscale ping`; a short
  `ssh -o BatchMode=yes -o ConnectTimeout=5` test; mounts (`findmnt -t cifs`
  on cachy, `mount | grep smbfs` on the Mac); then `docker ps`, compose logs
  and `systemctl status`. [MEM]
