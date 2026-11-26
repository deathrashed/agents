# Reusable recipes

## White/yellow status row

```sh
python3 scripts/shieldcn_visual.py badge --label macOS --value '✓' --logo apple --style presets/white-yellow-outline.json
python3 scripts/shieldcn_visual.py badge --label CachyOS --value '✓' --logo cachyos --style presets/white-yellow-outline.json
```

## Branded hero and live GitHub activity

```sh
python3 scripts/shieldcn_visual.py header --preset graph --title 'MY PROJECT' --subtitle 'Actual one-line value proposition' --logo lu:Zap --style presets/white-yellow-outline.json
python3 scripts/shieldcn_visual.py chart --kind github-issues --repo owner/repo --title 'Issue activity' --style presets/white-yellow-outline.json
```

## Dynamic category total

```sh
python3 scripts/shieldcn_visual.py dynamic --json-url https://raw.githubusercontent.com/owner/repo/main/stats/badges.json --query '$.skills' --label Skills --logo lu:Zap --style presets/white-yellow-outline.json
```

## Badge group

```sh
python3 scripts/shieldcn_visual.py group --segments github/stars/owner/repo github/forks/owner/repo --style presets/zinc-minimal.json
```

## Generate a composed hero fragment

```sh
python3 scripts/compose_readme_hero.py templates/hero.example.json > /tmp/hero.md
```

Replace placeholders only after inspecting actual repo data. The example hero's language, licence, and platform claims are *not verified facts*. A banner should not duplicate an existing project logo without purpose.
