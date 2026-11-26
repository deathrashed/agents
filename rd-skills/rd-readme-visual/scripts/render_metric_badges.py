#!/usr/bin/env python3
"""Generate GitHub README-safe adaptive ShieldCN badge snippets from metric names."""
import argparse
import html
from urllib.parse import quote, urlencode

ICONS = {
    'skills': 'lu:Zap', 'plugins': 'ri:BsPlugin', 'scripts': 'ri:TbScript',
    'rules': 'lu:ListCollapse', 'marketplaces': 'ri:TbShoppingBagCheck',
    'agents': 'ri:BsRobo', 'tests': 'lu:FlaskConical', 'commands': 'lu:Terminal',
    'docs': 'lu:BookOpen', 'workflows': 'lu:Workflow', 'integrations': 'lu:Plug',
    'languages': 'lu:Code', 'assets': 'lu:Images', 'examples': 'lu:FileCode',
}


def badge_url(owner, repo, key, dark, logo):
    remote = f'https://raw.githubusercontent.com/{owner}/{repo}/main/stats/badges.json'
    params = dict(url=remote, query=f'$.{key}', label=key.replace('_', ' ').title(),
                  variant='outline', mode='dark' if dark else 'light', color='ffffff',
                  logo=logo, logoColor='ffda00', labelTextColor='ffffff', valueColor='ffda00')
    return 'https://shieldcn.dev/badge/dynamic/json.svg?' + urlencode(params)


def chart_url(owner, repo, key, dark):
    remote = f'https://raw.githubusercontent.com/{owner}/{repo}/main/stats/history.json'
    params = dict(url=remote, query=f'$.history[*].{key}', dateQuery='$.history[*].date',
                  title=f'{key.replace("_", " ").title()} Growth', mode='dark' if dark else 'light',
                  color='ffda00', bg='transparent', width=800, height=350)
    return 'https://shieldcn.dev/chart/json.svg?' + urlencode(params)


def picture(url1, url2, alt):
    esc = lambda u: html.escape(u, quote=True)
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{esc(url1)}">\n'
            f'  <img alt="{html.escape(alt, quote=True)}" src="{esc(url2)}">\n</picture>')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('owner_repo', help='e.g. deathrashed/agents')
    p.add_argument('metrics', nargs='+', help='metric names from badges.json')
    p.add_argument('--chart', action='store_true')
    p.add_argument('--logo', default='', help='override logo for all badge names')
    args = p.parse_args()
    owner, repo = args.owner_repo.split('/', 1)
    print('<p align="center">')
    for key in args.metrics:
        logo = args.logo or ICONS.get(key, 'lu:ChartColumn')
        if args.chart:
            dark, light = chart_url(owner, repo, key, True), chart_url(owner, repo, key, False)
        else:
            dark, light = badge_url(owner, repo, key, True, logo), badge_url(owner, repo, key, False, logo)
        print(f'<a href="#{key.replace("_", "-")}">')
        print(picture(dark, light, key.replace('_', ' ').title()))
        print('</a>')
    print('</p>')


if __name__ == '__main__':
    main()
