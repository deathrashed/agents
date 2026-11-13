#!/usr/bin/env python3
"""agents-check: read-only health check for ~/.agents and the agents that read it.

Never writes, never prints secret values (only file names and paths).
Exit 0 = no FAIL, 1 = at least one FAIL, 2 = the check itself could not run.
"""
import hashlib, json, os, platform, re, socket, subprocess, sys

try:
    import tomllib
except ImportError:  # python < 3.11 (stock macOS python3 is 3.9)
    try:
        import tomli as tomllib
    except ImportError:
        sys.stderr.write("agents-check: needs python >= 3.11 (tomllib) or the tomli package\n")
        sys.exit(2)

HOME = os.path.expanduser("~")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_EXT = {".md", ".mdc", ".txt", ".toml", ".json", ".jsonc", ".yaml", ".yml", ".sh", ".py",
            ".js", ".mjs", ".ts", ".fish", ".zsh", ".bash", ".cfg", ".ini", ""}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}
MAX_TEXT = 1_000_000

def X(p):
    return os.path.expanduser(p)

def short(p):
    p = str(p)
    return "~" + p[len(HOME):] if p == HOME or p.startswith(HOME + os.sep) else p

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def tree_hash(path):
    """Content hash of a skill dir (follows links, ignores .git)."""
    h = hashlib.sha256()
    for root, dirs, files in os.walk(path, followlinks=True):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for fn in sorted(files):
            fp = os.path.join(root, fn)
            h.update(os.path.relpath(fp, path).encode())
            try:
                h.update(sha(fp).encode())
            except OSError:
                h.update(b"<unreadable>")
    return h.hexdigest()

def load_json(path):
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    if path.endswith(".jsonc"):
        txt = re.sub(r'("(?:\\.|[^"\\])*")|//[^\n]*|/\*.*?\*/', lambda m: m.group(1) or "", txt, flags=re.S)
        txt = re.sub(r",(\s*[}\]])", r"\1", txt)
    return json.loads(txt)

def load_any(path):
    if path.endswith(".toml"):
        with open(path, "rb") as f:
            return tomllib.load(f)
    return load_json(path)

def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except (OSError, subprocess.SubprocessError):
        return None

class Report:
    def __init__(self):
        self.checks = []
    def add(self, cid, title, status, summary, details=None):
        self.checks.append({"id": cid, "title": title, "status": status,
                            "summary": summary, "details": details or []})

def worst(statuses):
    for s in ("FAIL", "WARN"):
        if s in statuses:
            return s
    return "OK"

# ---------------------------------------------------------------- setup
def pick_machine(cfg):
    host = socket.gethostname().split(".")[0].lower()
    for key, m in cfg.get("machines", {}).items():
        if m.get("hostname", key).lower() == host or key == host:
            return key, m
    return host, {"hostname": host, "os": platform.system().lower(), "unverified": True}

def tool_paths(tool, machine):
    """Merge [tools.x] with an optional [tools.x.<machine>] override."""
    t = {k: v for k, v in tool.items() if not isinstance(v, dict)}
    t.update(tool.get(machine, {}))
    return t

def skill_entries(d):
    """name -> (entry path, realpath) for entries with a SKILL.md."""
    out = {}
    try:
        names = sorted(os.listdir(d))
    except OSError:
        return out
    for n in names:
        p = os.path.join(d, n)
        sk = os.path.join(p, "SKILL.md")
        if not os.path.isfile(sk):
            continue
        name = n
        try:
            with open(sk, encoding="utf-8", errors="replace") as f:
                head = f.read(4096)
            m = re.search(r"^---\s*\n(.*?)\n---", head, re.S)
            if m:
                nm = re.search(r"^name:\s*['\"]?([^'\"\n]+?)['\"]?\s*$", m.group(1), re.M)
                if nm:
                    name = nm.group(1).strip()
        except OSError:
            pass
        out.setdefault(name, []).append((p, os.path.realpath(p)))
    return out

# ---------------------------------------------------------------- checks
def check_broken_links(r, cfg, tools):
    roots = [X(cfg["shared"]["agents_dir"])]
    for t in tools.values():
        roots += [X(s) for s in t.get("skills", [])]
    seen, broken = set(), []
    for root in roots:
        if not os.path.isdir(root):
            continue
        rroot = os.path.realpath(root)
        if rroot in seen and root != X(cfg["shared"]["agents_dir"]):
            continue
        seen.add(rroot)
        deep = root == X(cfg["shared"]["agents_dir"])
        if deep:
            walker = os.walk(root)
        else:
            walker = [(root, [], os.listdir(root))]
        for base, dirs, files in walker:
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for n in list(dirs) + list(files):
                p = os.path.join(base, n)
                if os.path.islink(p) and not os.path.exists(p):
                    broken.append(f"{short(p)} -> {os.readlink(p)}")
    broken = sorted(set(broken))
    r.add("broken_links", "Broken symlinks (~/.agents tree + every tool skills dir)",
          "FAIL" if broken else "OK", f"{len(broken)} broken", broken)

def check_conflicts(r, cfg):
    root = X(cfg["shared"]["agents_dir"])
    hits = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            p = os.path.join(base, fn)
            if os.path.splitext(fn)[1].lower() not in TEXT_EXT or os.path.islink(p):
                continue
            try:
                if os.path.getsize(p) > MAX_TEXT:
                    continue
                with open(p, encoding="utf-8", errors="strict") as f:
                    txt = f.read()
            except (OSError, UnicodeDecodeError):
                continue
            if re.search(r"^<{7}( |$)", txt, re.M) and re.search(r"^>{7}( |$)", txt, re.M):
                n = len(re.findall(r"^<{7}( |$)", txt, re.M))
                hits.append(f"{short(p)} ({n} block(s))")
    r.add("conflict_markers", "Git conflict markers in ~/.agents text files",
          "FAIL" if hits else "OK", f"{len(hits)} file(s)", hits)

def check_duplicates(r, tools):
    details, total = [], 0
    for tid, t in tools.items():
        merged = {}
        for d in t.get("skills", []):
            for name, ents in skill_entries(X(d)).items():
                merged.setdefault(name, []).extend(ents)
        for name, ents in sorted(merged.items()):
            reals = sorted({rp for _, rp in ents})
            if len(reals) < 2:
                continue
            total += 1
            hashes = {tree_hash(rp) for rp in reals}
            kind = "identical" if len(hashes) == 1 else "diverged"
            details.append(f"{tid}: {name} [{kind}] " + " | ".join(short(rp) for rp in reals))
    r.add("duplicate_skills", "Same skill name from two different sources in one agent's dirs",
          "WARN" if total else "OK", f"{total} duplicate(s)", details)

def check_writers(r, cfg, machine_cfg):
    skills_dir = X(cfg["shared"]["agents_dir"]) + "/skills"
    lock = X(machine_cfg.get("npx_lock", "~/.local/state/skills/.skill-lock.json"))
    locked = set()
    try:
        locked = set(load_json(lock).get("skills", {}).keys())
    except (OSError, ValueError) as e:
        r.add("unknown_writers", "~/.agents/skills entries outside npx-skills lock and repo",
              "WARN", f"lockfile unreadable: {short(lock)} ({type(e).__name__})")
        return
    repo_sk = X(cfg["shared"]["repo"]) + "/skills"
    own = set(os.listdir(repo_sk)) if os.path.isdir(repo_sk) else set()
    groups = {}
    try:
        names = sorted(os.listdir(skills_dir))
    except OSError:
        names = []
    for n in names:
        if n.startswith(".") or n in locked or n in own:
            continue
        p = os.path.join(skills_dir, n)
        if os.path.islink(p):
            tgt = os.readlink(p)
            parts = os.path.abspath(os.path.join(skills_dir, tgt)).split(os.sep)
            src = short(os.sep.join(parts[:5])) + " (link)"
        else:
            src = "real dir in ~/.agents/skills"
        if n.startswith("ghostex"):
            src = "ghostex"
        groups.setdefault(src, []).append(n)
    details = [f"{src}: {len(v)}: {', '.join(v)}" for src, v in sorted(groups.items())]
    cnt = sum(len(v) for v in groups.values())
    r.add("unknown_writers", "~/.agents/skills entries outside npx-skills lock and repo",
          "WARN" if cnt else "OK",
          f"{cnt} of {len(names)} entries unmanaged (lock has {len(locked)})", details)

def mentions_shared(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            txt = f.read(MAX_TEXT)
    except OSError:
        return False
    return bool(re.search(r"(~|\$HOME|/home/[^/\s]+|/Users/[^/\s]+)/\.agents/(AGENTS|main)\.md", txt))

def check_pointers(r, cfg, tools):
    shared = X(cfg["shared"]["agents_md"])
    repo_md = X(cfg["shared"]["repo"]) + "/AGENTS.md"
    details, sts = [], []
    try:
        live_h = sha(shared)
        repo_h = sha(repo_md) if os.path.isfile(repo_md) else None
    except OSError:
        r.add("instruction_pointers", "Instruction files point at ~/.agents/AGENTS.md", "FAIL",
              f"{short(shared)} missing")
        return
    if repo_h and repo_h != live_h:
        sts.append("FAIL"); details.append(f"FAIL ~/.agents/AGENTS.md sha {live_h[:12]} != repo {repo_h[:12]}")
    for tid, t in tools.items():
        files = t.get("instructions", [])
        reads = t.get("reads_agents_md")
        if tid == "kilo":
            kj = X("~/.config/kilo/kilo.jsonc")
            try:
                ins = load_json(kj).get("instructions", [])
            except (OSError, ValueError):
                ins = []
            if any(".agents/" in str(i) for i in ins):
                sts.append("OK"); details.append("OK   kilo: kilo.jsonc `instructions` includes ~/.agents")
            else:
                sts.append("WARN"); details.append("WARN kilo: no global instructions (`instructions` in ~/.config/kilo/kilo.jsonc unset), does not read ~/.agents/AGENTS.md")
            continue
        if not files:
            if reads is False:
                details.append(f"INFO {tid}: no local instruction file (by design)")
            continue
        ok_any, notes = False, []
        for f in files:
            p = X(f)
            if os.path.islink(p) and not os.path.exists(p):
                sts.append("FAIL"); notes.append(f"{f} broken link"); continue
            if os.path.isdir(p):
                mds = [os.path.join(p, n) for n in os.listdir(p) if n.endswith((".md", ".mdc"))]
                if any(mentions_shared(m) for m in mds):
                    ok_any = True; notes.append(f"{f}/ mentions shared")
                continue
            if not os.path.exists(p):
                notes.append(f"{f} absent"); continue
            if os.path.realpath(p) == os.path.realpath(shared):
                ok_any = True
                h = sha(p)
                notes.append(f"{f} -> shared (sha {h[:12]}{', = repo' if h == repo_h else ''})")
            elif mentions_shared(p):
                ok_any = True; notes.append(f"{f} mentions ~/.agents (not a link)")
            else:
                notes.append(f"{f} exists, no link/mention")
        st = "OK" if ok_any else "WARN"
        if ok_any and reads == "unverified":
            st = "WARN"; notes.append("whether the tool reads it globally is [UNVERIFIED]")
        sts.append(st)
        details.append(f"{st:<4} {tid}: " + "; ".join(notes))
    r.add("instruction_pointers", "Instruction files point at ~/.agents/AGENTS.md (hash = repo)",
          worst(sts), f"{sum(1 for d in details if d.startswith('OK'))} OK, "
          f"{sum(1 for d in details if d.startswith('WARN'))} WARN, {sum(1 for d in details if d.startswith('FAIL'))} FAIL",
          details)

def redact(cmd):
    """Mask anything that could be a secret in a hook command before printing."""
    cmd = re.sub(r"(Bearer\s+)\S+", r"\1<redacted>", cmd, flags=re.I)
    cmd = re.sub(r"(\b[A-Za-z0-9_]*(KEY|TOKEN|SECRET|PASS|AUTH)[A-Za-z0-9_]*\s*[=:]\s*)\S+", r"\1<redacted>", cmd, flags=re.I)
    cmd = re.sub(r"(--?[A-Za-z-]*(key|token|secret|password|auth)[A-Za-z-]*[=\s]+)\S+", r"\1<redacted>", cmd, flags=re.I)
    return re.sub(r"\b[A-Za-z0-9_\-]{32,}\b", "<redacted>", cmd)

PRE_RE = re.compile(r"pretooluse|beforeshellexecution|beforetool|tool\.execute\.before|pre_tool", re.I)

def hook_commands(obj, path=()):
    """Yield (path tuple, command string) for every 'command' string in a hook config."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("command", "cmd") and isinstance(v, str):
                yield path, v
            elif k == "command" and isinstance(v, list):
                yield path, " ".join(map(str, v))
            else:
                yield from hook_commands(v, path + (str(k),))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, dict) and "matcher" in v:
                yield from hook_commands(v, path + (f"[{v.get('matcher')}]",))
            else:
                yield from hook_commands(v, path)

def check_hooks(r, cfg, tools):
    markers = {"rtk": re.compile(r"(^|[/\s'\"])rtk(\s|$|['\"])|rtk-rewrite|rtk hook"),
               "context-mode": re.compile(r"context-mode", re.I),
               "caveman": re.compile(r"caveman", re.I)}
    details, sts = [], []
    for tid, t in tools.items():
        found, pre = set(), []
        for h in t.get("hooks", []):
            p = X(h)
            files = []
            if os.path.isdir(p):
                for n in sorted(os.listdir(p)):
                    fp = os.path.join(p, n)
                    for mk, rx in markers.items():
                        if rx.search(n):
                            found.add(mk); pre.append(f"{mk} via {short(fp)}")
                    if n.endswith((".json", ".toml")) and os.path.isfile(fp):
                        files.append(fp)
            elif os.path.isfile(p):
                files.append(p)
            for fp in files:
                try:
                    data = load_any(fp)
                except Exception:
                    continue
                whole = "hook" in os.path.basename(fp).lower() or os.path.dirname(fp).endswith("hooks")
                scope = data if whole else (data.get("hooks", {}) if isinstance(data, dict) else {})
                for pth, cmd in hook_commands(scope):
                    # hide anything after a possible secret-ish env assignment
                    safe = redact(cmd)
                    label = "/".join(pth)
                    for mk, rx in markers.items():
                        if rx.search(cmd):
                            found.add(mk)
                    if PRE_RE.search(label) or "[Bash" in label:
                        pre.append(f"{label}: {safe[:110]}  ({short(fp)})")
        st = "FAIL" if len(found) > 1 else "OK"
        sts.append(st)
        details.append(f"{st:<4} {tid}: output tools={sorted(found) or 'none'}; pre-tool/Bash hooks={len(pre)}")
        details += [f"       - {x}" for x in pre]
    r.add("output_hooks", "At most one output-rewriting hook per agent (rtk / context-mode / caveman)",
          worst(sts), f"{sum(1 for s in sts if s == 'FAIL')} agent(s) with >1", details)

def check_plugins(r):
    details, sts = [], []
    sp, ip = X("~/.claude/settings.json"), X("~/.claude/plugins/installed_plugins.json")
    try:
        enabled = load_json(sp).get("enabledPlugins", {}) or {}
        installed = load_json(ip).get("plugins", {}) if os.path.exists(ip) else {}
        for key, on in sorted(enabled.items()):
            if not on:
                continue
            ents = installed.get(key, [])
            if not ents:
                if key.endswith("@synced") and os.path.isdir(X("~/.claude/plugins/synced")):
                    continue
                sts.append("FAIL"); details.append(f"FAIL claude {key}: enabled but not in installed_plugins.json"); continue
            for e in ents:
                path = e.get("installPath", "")
                if path and not os.path.isdir(path):
                    sts.append("FAIL"); details.append(f"FAIL claude {key}: installPath missing {short(path)}")
    except (OSError, ValueError) as e:
        details.append(f"INFO claude settings unreadable ({type(e).__name__})")
    cp = X("~/.codex/config.toml")
    try:
        with open(cp, "rb") as f:
            plugins = tomllib.load(f).get("plugins", {})
        cache = X("~/.codex/plugins/cache")
        for key, v in sorted(plugins.items()):
            if not (isinstance(v, dict) and v.get("enabled")) or "@" not in key:
                continue
            name, mkt = key.split("@", 1)
            if not os.path.isdir(os.path.join(cache, mkt, name)):
                sts.append("WARN"); details.append(f"WARN codex {key}: no ~/.codex/plugins/cache/{mkt}/{name}")
    except (OSError, ValueError) as e:
        details.append(f"INFO codex config unreadable ({type(e).__name__})")
    r.add("stale_plugins", "Enabled plugins that point to nothing", worst(sts),
          f"{len([d for d in details if not d.startswith('INFO')])} stale", details)

def ver(s):
    m = re.search(r"\d+\.\d+\.\d+", s or "")
    return m.group(0) if m else None

def check_manifest(r, cfg):
    mp = X(cfg["shared"]["agents_dir"]) + "/manifest.toml"
    try:
        with open(mp, "rb") as f:
            man = tomllib.load(f).get("tools", {})
    except (OSError, ValueError) as e:
        r.add("manifest_drift", "Installed versions vs manifest.toml pins", "WARN", f"manifest unreadable ({type(e).__name__})")
        return
    def pkg(p):
        try:
            return load_json(X(p)).get("version")
        except (OSError, ValueError):
            return None
    def codex_rea():
        try:
            with open(X("~/.codex/config.toml"), encoding="utf-8") as f:
                m = re.search(r"rea-agents@(\d+\.\d+\.\d+)", f.read())
            return m.group(1) if m else None
        except OSError:
            return None
    def claude_mem():
        try:
            e = load_json(X("~/.claude/plugins/installed_plugins.json"))["plugins"]["claude-mem@thedotmack"][0]
            v = e.get("version")
            return v + ("" if os.path.isdir(e.get("installPath", "")) else " (installPath missing)")
        except (OSError, ValueError, KeyError, IndexError):
            return None
    probes = {
        "rtk": lambda: ver(run(["rtk", "--version"])),
        "context-mode": lambda: pkg("~/.local/share/cc-presets/runtime/node_modules/context-mode/package.json"),
        "rea": codex_rea,
        "caveman": lambda: pkg("~/.local/share/cc-presets/runtime/node_modules/@caveman-ai/cli/package.json"),
        "claude-mem": claude_mem,
    }
    details, sts = [], []
    for name, probe in probes.items():
        pin = ver(str(man.get(name, {}).get("version", "")))
        got = probe()
        if pin is None:
            st, msg = "WARN", f"no pin in manifest, installed {got}"
        elif got is None:
            st, msg = "WARN", f"pin {pin}, installed version not found"
        elif ver(got) != pin:
            st, msg = "WARN", f"pin {pin}, installed {got}"
        elif "missing" in got:
            st, msg = "WARN", f"pin {pin} = installed, but {got.split('(')[1].rstrip(')')}"
        else:
            st, msg = "OK", f"{pin}"
        sts.append(st); details.append(f"{st:<4} {name}: {msg}")
    r.add("manifest_drift", "Installed versions vs ~/.agents/manifest.toml pins", worst(sts),
          f"{sts.count('WARN')} drift", details)

def check_repo(r, cfg, machine):
    live, repo = X(cfg["shared"]["agents_dir"]), X(cfg["shared"]["repo"])
    ignore = set(cfg["shared"].get("repo_ignore", []))
    if not os.path.isdir(repo):
        r.add("repo_drift", "Live ~/.agents vs repo", "WARN", f"repo missing: {short(repo)}")
        return
    pairs = [("AGENTS.md", "AGENTS.md"), ("main.md", "main.md"),
             ("manifest.toml", f"machines/{machine}/manifest.toml")]
    names = set()
    for d in (os.path.join(live, "rules"), os.path.join(repo, "rules")):
        if os.path.isdir(d):
            names |= {n for n in os.listdir(d) if n.endswith(".md")}
    pairs += [(f"rules/{n}", f"rules/{n}") for n in sorted(names) if f"rules/{n}" not in ignore]
    details, linked = [], 0
    for lrel, rrel in pairs:
        lp, rp = os.path.join(live, lrel), os.path.join(repo, rrel)
        if os.path.islink(lp) and os.path.realpath(lp) == os.path.realpath(rp):
            linked += 1; continue
        le, re_ = os.path.isfile(lp), os.path.isfile(rp)
        if le and re_:
            if sha(lp) != sha(rp):
                details.append(f"differs: ~/.agents/{lrel} vs repo/{rrel}")
        elif le:
            details.append(f"live only: ~/.agents/{lrel}")
        elif re_:
            details.append(f"repo only: {rrel}")
    r.add("repo_drift", f"Live ~/.agents vs {short(repo)} (not linked yet)",
          "WARN" if details else "OK",
          f"{len(details)} difference(s), {linked} linked, {len(pairs)} compared"
          + (f", ignored {sorted(ignore)}" if ignore else ""), details)

def check_telemetry(r):
    details, sts = [], []
    out = run(["rtk", "telemetry", "status"])
    if out is None:
        sts.append("WARN"); details.append("WARN rtk: `rtk telemetry status` failed")
    else:
        m = re.search(r"enabled:\s*(\w+)", out)
        on = m and m.group(1).lower() not in ("no", "false", "off")
        sts.append("FAIL" if on else "OK")
        details.append(f"{'FAIL' if on else 'OK':<4} rtk: enabled: {m.group(1) if m else '?'}")
    cp = X("~/.caveman-cloud/config.json")
    try:
        tel = load_json(cp).get("telemetry", {})
        on = tel.get("enabled") is not False
        sts.append("FAIL" if on else "OK")
        details.append(f"{'FAIL' if on else 'OK':<4} caveman: ~/.caveman-cloud/config.json telemetry.enabled={tel.get('enabled')}")
    except (OSError, ValueError):
        if os.environ.get("DO_NOT_TRACK") == "1" or os.environ.get("CAVEMAN_TELEMETRY") in ("0", "off", "false"):
            sts.append("OK"); details.append("OK   caveman: no config, env opt-out set")
        else:
            sts.append("WARN"); details.append("WARN caveman: no ~/.caveman-cloud/config.json and no env opt-out")
    r.add("telemetry", "Telemetry off for rtk and caveman", worst(sts), "", details)

# ---------------------------------------------------------------- main
def main(argv):
    as_json = "--json" in argv
    cfg_path = os.path.join(HERE, "checks", "agents.toml")
    for a in argv:
        if a.startswith("--config="):
            cfg_path = a.split("=", 1)[1]
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip() + "\n\nusage: agents-check [--json] [--config=PATH]")
        return 0
    try:
        with open(cfg_path, "rb") as f:
            cfg = tomllib.load(f)
    except (OSError, ValueError) as e:
        sys.stderr.write(f"agents-check: cannot read {cfg_path}: {e}\n")
        return 2
    machine, mcfg = pick_machine(cfg)
    tools = {tid: tool_paths(t, machine) for tid, t in cfg.get("tools", {}).items()}
    r = Report()
    for fn, args in ((check_broken_links, (r, cfg, tools)), (check_conflicts, (r, cfg)),
                     (check_duplicates, (r, tools)), (check_writers, (r, cfg, mcfg)),
                     (check_pointers, (r, cfg, tools)), (check_hooks, (r, cfg, tools)),
                     (check_plugins, (r,)), (check_manifest, (r, cfg)),
                     (check_repo, (r, cfg, machine)), (check_telemetry, (r,))):
        try:
            fn(*args)
        except Exception as e:  # keep going; report the crash as a FAIL
            r.add(fn.__name__, fn.__name__, "FAIL", f"check crashed: {type(e).__name__}: {e}")
    counts = {s: sum(1 for c in r.checks if c["status"] == s) for s in ("OK", "WARN", "FAIL")}
    overall = worst([c["status"] for c in r.checks])
    if as_json:
        print(json.dumps({"machine": machine, "unverified_machine": bool(mcfg.get("unverified")),
                          "overall": overall, "counts": counts, "checks": r.checks}, indent=2))
    else:
        print(f"agents-check on {machine}" + (" [UNVERIFIED machine profile]" if mcfg.get("unverified") else ""))
        print(f"overall {overall}: {counts['OK']} OK, {counts['WARN']} WARN, {counts['FAIL']} FAIL\n")
        for c in r.checks:
            print(f"[{c['status']:<4}] {c['id']}: {c['summary']}  ({c['title']})")
        for c in r.checks:
            if c["details"] and (c["status"] != "OK" or c["id"] in ("output_hooks", "instruction_pointers")):
                print(f"\n== {c['id']} ({c['status']})")
                for d in c["details"]:
                    print(f"  {d}")
    return 1 if overall == "FAIL" else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
