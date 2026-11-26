# Homelab

Sources: MEM (`areas/homelab-access-map.md`, verified 2026-11-08).

Full map with addresses, ports, shares and services: cachy
`~/downloads/memory/areas/homelab-access-map.md` (Mac: `/Volumes/home/downloads/memory/...`)
and `~/docker/HOMELAB-GUIDE.md` / `ACCESS-AND-STATUS.md` on cachy. Read it
before networking, mounts, Docker or SSH work. Never copy addresses, hostnames
or ports into this public repo. They live in `homelab.local.md` in this
folder (gitignored): every IP, the MagicDNS names, ports and mounts, verified
from both machines. Read it with this file.

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

## SSH: cachy to Mac

- Connect with `ssh mac` (aliases `m3`, `ts-m3`, and the MagicDNS name and
  IPs in `homelab.local.md`, which all share one config block). Remote user
  is `rd`, and
  the host is macOS arm64. Config is in `~/.ssh/config`. Don't pass a user,
  host, port or `-i`.
- Auth is public key only, with `IdentitiesOnly yes`. The Mac accepts
  `~/.ssh/m3`. `cachy.ssh` is offered first and rejected, which is harmless.
- No ssh-agent is running and `SSH_AUTH_SOCK` is empty. Don't start one or
  add keys.
- Aliases resolve over Tailscale. Direct IP connections stay direct. Don't
  rewrite the config blocks.
- Always use `-o BatchMode=yes -o ConnectTimeout=5` for non-interactive runs.
- If ssh fails, check in this order:
  1. `tailscale ping ts-m3`.
  2. `ssh -o BatchMode=yes -o ConnectTimeout=5 mac true`.
  3. `ssh -v mac true 2>&1 | grep -E 'Offering|accepts|Authenticated'`.
  4. Report the real error text. If the Mac is asleep, wait.
- Never print, copy or edit private keys in `~/.ssh/`. List them by name,
  size and date only. Don't edit `~/.ssh/config` or the Mac's
  `authorized_keys` without asking, and back up first.
- File access to the Mac goes over SMB at `/mnt/mac/*`, not ssh. See the
  mount rules above.

## SSH: Mac to cachy

Verified from the Mac on 2026-11-26. [M3]

- Connect with `ssh cachy` (aliases `death-thrash`, `ts-cachy`, and the
  MagicDNS name in `homelab.local.md`). Remote user is `rd`, and the host is
  CachyOS Linux x86_64. Config is in the Mac's `~/.ssh/config`.
  Don't pass a user, host, port or `-i`.
- The name `cachy` comes from a line in the Mac's `/etc/hosts`. The SMB
  watcher (below) points it at the LAN address at home and the Tailscale
  address away, so `ssh cachy` works in both places. If that line is stale,
  `cachy-vscode` (same host, reached by its full Tailscale name) still works.
- In Tailscale, cachy is the device `ts-cachy`. Don't confuse it with other
  devices that report cachy's LAN address as their endpoint.
- Auth is public key only: `~/.ssh/cachy` with `IdentitiesOnly yes`. Unlike
  cachy, the Mac runs the macOS ssh-agent, which loads that key from
  Keychain (`UseKeychain`, `AddKeysToAgent`). Don't add or remove agent keys.
- **cachy's login shell is fish.** Remote commands run in fish, so POSIX
  syntax can fail (`. /etc/os-release` errors). Wrap shell scripts:
  `ssh cachy "bash -c '…'"`, or copy a script over and run it with `bash`.
- Always use `-o BatchMode=yes -o ConnectTimeout=5` for non-interactive runs.
- `cachy-agents`, `cachy-codex`, `cachy-claude` and `cachy-opencode` log in
  as user `dev` to Docker dev containers on cachy. Those containers were
  stopped on 2026-11-26, so "Connection refused" means they are down, not
  that ssh is broken. Don't start them without asking (RAM is tight).
- If ssh fails, check in this order:
  1. `tailscale ping ts-cachy`. The Homebrew CLI's "client version !=
     tailscaled server version" warning is harmless.
  2. `ssh -o BatchMode=yes -o ConnectTimeout=5 cachy true`.
  3. `ssh -o BatchMode=yes -o ConnectTimeout=5 cachy-vscode true`. If this
     works and step 2 doesn't, the `/etc/hosts` line is stale.
  4. `ssh -v cachy true 2>&1 | grep -E 'Offering|accepts|Authenticated'`.
  5. Report the real error text. If cachy is off or asleep, wait.
- The key rules from the section above apply on the Mac too.

## Files: Mac to cachy

- File access to cachy goes over SMB, not ssh. The share `home` (cachy's
  `/home/rd`) is mounted at `/Volumes/home`, and `mnt` (cachy's `/mnt`) at
  `/Volumes/mnt`. So cachy's `~/x` is `/Volumes/home/x` on the Mac.
- The LaunchAgent `com.rd.cachy-smb` runs `~/.local/bin/cachy-reconnect.py`
  every 60 s. It tries the LAN first and Tailscale second, mounts the shares,
  unmounts them after about 3 offline checks so Finder doesn't hang, and
  refuses to stack more than 4 cachy mounts. SMB passwords are in Keychain.
  Log: `~/Library/Logs/cachy-smb.log`. Status:
  `python3 ~/.local/bin/cachy-reconnect.py --status`.
- Don't mount or unmount by hand (see the mount rule above). cachy's root
  `/` is deliberately not automounted, because scanning it hung Finder. Mount
  it only when rd asks: `open smb://cachy/root`.
