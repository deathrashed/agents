# Local Visual README Archetypes Reference

This guide details the 6 classic README archetypes. There is no default family: pick from the reference READMEs listed in SKILL.md and borrow ideas from them; use these when matching an existing project family or when the user asks for the classic look. Borrow signatures from them freely, but don't copy a whole layout.

---

## Visual Design Core Components

All 6 archetypes share these structural foundations:

1. **Centered Header Hero Block (`<div align="center">`)**:
   - Primary asset image (Logo, SVG, or project banner).
   - Styled Title (`# 𝗠𝗣𝟯𝗧𝗔𝗚` styled font, `<h1>GO·GENRES</h1>`, `# BLOGGER PIPELINE`, `# CLIPPED`, or `# Project`).
   - One-sentence bold summary statement.
   - Shields.io badge row (Dark `#1e1e1e` / `#111111` base, custom accent logo colors, uppercase or clean labels).
   - Dot (`·`), Bullet (`•`), or Pipe (`|`) separated quick navigation bar links (`[Quick Start](#quick-start) • [Features](#features) ...`).

2. **Visual Section Headers**:
   - Iconify API SVG icons: `## <img src="https://api.iconify.design/mdi:rocket-launch-outline.svg?color=%2301acd7" height="22"> Quick Start`
   - Readmecodegen icons: `## ![terminal](https://www.readmecodegen.com/api/social-icon?name=terminal&size=18&animation=fade&color=%23ff2a1f) Quick Start`

3. **Compact Data Tables & ASCII Trees**:
   - Tables for configuration, providers, modules, CLI flags, dependencies, and keyboard macros.
   - Fenced code block ASCII directory trees with inline comments explaining file purposes.

4. **Collapsible Section Cards (`<details><summary>`)**:
   - Secondary information, verbose setup steps, full layout presets, MTA guides, and developer commands enclosed in styled summary cards.

5. **GitHub Alerts**:
   - `> [!TIP]`, `> [!NOTE]`, `> [!WARNING]`, `> [!CAUTION]` for critical instructions.

---

## The 6 Archetypes

### Archetype 1: Mp3tag Modular Collection (Category-Rich / Collapsible Deep Reference)

**Best for**: Modular tools, action bundles, config repos, multi-source collections.

**Visual Signature**:
- Large icon (`width="400"` or `width="144"`).
- Bold styled title (`# 𝗠𝗣𝟯𝗧𝗔𝗚`).
- Dark shields badges (`1e1e1e`) with yellow/gold `logoColor=faa701` accents.
- Inline dot navigation bar.
- Collapsible `<details><summary>` category blocks with horizontal dividers `────────`.
- Settings & prefix mapping tables inside details blocks.

```html
<div align="center">
<img src="Assets/Icon/logo.png" width="400" alt="Project Logo" />

# 𝗣𝗥𝗢𝗝𝗘𝗖𝗧 𝗡𝗔𝗠𝗘

**A curated collection of tools, tag sources, and configuration for [Tool](https://example.com) on macOS.**

Short description highlighting key features, modularity, and primary use cases.

[![VERSION](https://img.shields.io/badge/Version-v1.0.0-1e1e1e?style=for-the-badge&logo=apple&logoColor=faa701)](https://example.com)
[![PLATFORM](https://img.shields.io/badge/macOS-1e1e1e?style=for-the-badge&logo=apple&logoColor=faa701)](https://apple.com)
[![WIZARD](https://img.shields.io/badge/interactive%20wizard-1e1e1e?style=for-the-badge&logo=gnubash&logoColor=faa701)](#quick-start)

[OVERVIEW](#overview) · [SOURCES](#sources) · [ACTIONS](#actions) · [SETTINGS](#settings) · [FAQ](#faq)

</div>

---

## Quick Start

1. **Configure the environment:**

   ```bash
   ./configure
   ```

> [!TIP]
> **New here?** Run `./configure` first to personalize paths and settings.

<details>
<summary>
<a id="overview"></a><strong><a href="#overview"><img src="Assets/Icon/icon-color.png" height="20" valign="middle" /></a>&nbsp;OVERVIEW</strong>
</summary>

────────

Detailed overview text, feature summary, and visual directory tree.

</details>
```

---

### Archetype 2: Zsh Environment & Shell Config (Feature Grid / Load Order / Workflows)

**Best for**: Shell configurations, CLI environments, modular dotfiles.

**Visual Signature**:
- Centered banner graphic (`width="45%"`).
- Dark shields (`1e1e1e`) with white logo accents.
- Feature highlights with Unicode glyph prefixes (`- **ϟ Lightning Fast**`, `- **⁂ Modular**`, `- **∞ XDG Compliant**`, `- **⌘ Power User**`).
- ASCII load-order pipeline and performance benchmark tables.

```html
<div align="center">
<img src="assets/banner.png" alt="Console Banner" width="45%">
<br>

[![SHELL](https://img.shields.io/badge/shell%20—%20zsh-1e1e1e?style=for-the-badge&logo=gnu-bash&logoColor=white)](https://www.zsh.org/)
[![PLATFORM](https://img.shields.io/badge/System%20—%20macOS-1e1e1e?style=for-the-badge&logo=apple&logoColor=white)](https://www.apple.com/macos/)
[![MODULES](https://img.shields.io/badge/modules%20—%207-1e1e1e?style=for-the-badge&logo=codecrafters&logoColor=white)](#modules)

**Fast, modular, XDG-first configuration environment with lazy loading and power-user automation.**

[Quick Start](#quick-start) • [Features](#features) • [Structure](#structure) • [Performance](#performance)

</div>

---

## Features

- **ϟ Lightning Fast** — Deferred initialization keeps startup under 100ms
- **⁂ Modular** — Focused modules loaded eagerly or lazily
- **∞ XDG Compliant** — Clean home directory, configs in `~/.config`
- **⌘ Power User** — 500+ aliases, 180+ functions
```

---

### Archetype 3: System Knowledge Base (Architecture Matrix / Storage Strategy)

**Best for**: System documentation, infrastructure repos, knowledge bases, architectural indexes.

**Visual Signature**:
- Centered icon image (`width="25%"`).
- Core Architecture table (`Layer | Detail`).
- Storage Strategy table (`Volume | Path | Filesystem | Size | Role`).
- Comprehensive domain mapping matrix (`Domain | File | Covers`).
- Integration points & data flow section.

```html
<div align="center">
<img src="_assets/logo.png" alt="Knowledge Base" width="25%">
<br>

[![KB](https://img.shields.io/badge/knowledge%20—%20base-1e1e1e?style=for-the-badge&logo=readthedocs&logoColor=white)](.)
[![SYSTEM](https://img.shields.io/badge/System%20—%20macOS-1e1e1e?style=for-the-badge&logo=apple&logoColor=white)](https://www.apple.com/macos/)

**Canonical reference documents describing system hardware, software, directory layouts, and workflows.**

</div>

---

## Core Architecture

| Layer | Detail |
|---|---|
| **Hardware** | Apple Silicon M3, 8GB RAM |
| **OS** | macOS 15.7 |
| **Shell** | zsh (~/.config/zsh/) |

## Storage Strategy

| Volume | Path | Filesystem | Size | Role |
|---|---|---|---|---|
| **Internal** | `/` | APFS | 228GB | System & active work |
```

---

### Archetype 4: Go CLI Tool with Iconify (Vibrant Iconify Headers / Provider Grid)

**Best for**: Go binaries, CLI tools, multi-provider utilities, TUI applications.

**Visual Signature**:
- Cyan/Vibrant badges (`01acd7`).
- Pipe navigation bar `<p><a href="#quick-start">Quick Start</a> | ...</p>`.
- Iconify API SVG icons in every section header:
  `## <img src="https://api.iconify.design/mdi:rocket-launch-outline.svg?color=%2301acd7" height="22"> Quick Start`
- Provider/Tool table with Iconify SVG icons in table cells.

```html
<div align="center">
  <img src="assets/icon.png" alt="Project Icon">

  <h1>PROJECT NAME</h1>

  <p><strong>One-sentence clear purpose statement.</strong></p>

  <p>
    <a href="https://go.dev/"><img src="https://img.shields.io/badge/go-1.26+-01acd7?style=for-the-badge&logo=go&logoColor=white" alt="Go 1.26+"></a>
    <a href="https://github.com/user/repo"><img src="https://img.shields.io/badge/version-1.0-01acd7?style=for-the-badge" alt="Version 1"></a>
  </p>

  <p>
    <a href="#quick-start">Quick Start</a> |
    <a href="#usage">Usage</a> |
    <a href="#providers">Providers</a> |
    <a href="#building">Building</a>
  </p>
</div>

---

## <img src="https://api.iconify.design/mdi:rocket-launch-outline.svg?color=%2301acd7" height="22"> Quick Start

```bash
go build -o bin/app .
./bin/app
```

## <img src="https://api.iconify.design/mdi:server.svg?color=%2301acd7" height="22"> Providers

| Source | Description | Binary |
| --- | --- | --- |
| <img src="https://api.iconify.design/mdi:database.svg?color=%2301acd7" height="16"> **Database** | Core data provider | `bin/db-tool` |
```

---

### Archetype 5: Blogger Automation Pipeline (Social Header Icons / Setup / Verification)

**Best for**: Scraping pipelines, posting bots, API automation, python CLI tools.

**Visual Signature**:
- SVG logo icon (`width="120"`).
- Black badges (`black` style for shields).
- Readmecodegen / animated SVG icons in section headers:
  `## ![terminal](https://www.readmecodegen.com/api/social-icon?name=terminal&size=18&animation=fade&color=%23ff2a1f) Quick Start`
- Dependencies table (`Category | Item | Description`).
- Security, Batch, and Verification sections.

```html
<div align="center">
<img src="./data/icon/logo.svg" alt="Project Icon" width="120">
<br>

# Project Pipeline

[![Python](https://img.shields.io/badge/python-black?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Bash](https://img.shields.io/badge/shell%20—%20bash-black?style=for-the-badge&logo=gnu-bash&logoColor=white)](https://gnu.org)

**Automating metadata collection, smart links, and cloud uploads.**

[Quick Start](#quick-start) • [Features](#features) • [Structure](#structure) • [Configuration](#configuration)

</div>

---

## ![terminal](https://www.readmecodegen.com/api/social-icon?name=terminal&size=18&animation=fade&color=%23ff2a1f) Quick Start

```bash
./scripts/setup.sh
./bin/run-pipeline
```
```

---

### Archetype 6: Clipped Multimedia Toolkit (Showcase Grid / Video Preview / Platform Profiles)

**Best for**: Media processing tools, video generators, desktop automation, Keyboard Maestro toolkits.

**Visual Signature**:
- App icon (`width="144"`).
- Styled Version / Platform badges.
- Table of Contents with Green Iconify SVG (`<img src="https://api.iconify.design/mdi:format-list-bulleted.svg?color=%2311c866" height="22">`).
- Side-by-side Video/Image HTML Showcase Grid Table (`<table width="100%">...</table>`).
- Core Technology cards with logo images.
- Platform profiles & template tables.
- Keyboard Maestro macro mapping table (`Macro | Trigger | Purpose`).

```html
<div align="center">
  <img src="assets/icon.png" alt="App icon" width="144">

  <h1>PROJECT TOOLKIT</h1>

  <p><strong>Metadata-aware clipping and video generation for audio workflows.</strong></p>

  <p>
    <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.12+-111111?style=for-the-badge&logo=python&logoColor=white"></a>
    <a href="https://ffmpeg.org"><img src="https://img.shields.io/badge/ffmpeg-required-111111?style=for-the-badge&logo=ffmpeg&logoColor=white"></a>
  </p>

  <p>
    <a href="#quick-start">Quick Start</a> |
    <a href="#examples">Examples</a> |
    <a href="#templates">Templates</a> |
    <a href="#macros">Macros</a>
  </p>
</div>

---

## <img src="https://api.iconify.design/mdi:play-box-multiple-outline.svg?color=%2311c866" height="22"> Examples

<table>
  <tr>
    <td width="50%" align="center">
      <img src="assets/examples/demo1.webp" width="100%" alt="Demo 1: vertical reel generated from an audio clip">
      <br>
      <strong>Demo 1 - Vertical Reel</strong>
    </td>
    <td width="50%" align="center">
      <img src="assets/examples/demo2.webp" width="100%" alt="Demo 2: square spinner clip">
      <br>
      <strong>Demo 2 - Square Spinner</strong>
    </td>
  </tr>
</table>
```

> [!WARNING]
> Do not use `<video src="assets/...">` or a raw.githubusercontent URL. GitHub
> strips the tag and the reader sees a blank gap. Use animated WebP/GIF in
> `<img>`, or upload the mp4 in a repo issue and paste the `user-attachments`
> URL. See `media.md`.

---

## Style Tokens Summary

| Component | Standard Color Hex | Shields Style |
|---|---|---|
| Dark Badge Base | `#1e1e1e` or `#111111` | `for-the-badge` |
| Gold Accent | `#faa701` | `logoColor=faa701` |
| Cyan Accent | `#01acd7` or `#06B6D4` | Iconify SVG color `%2301acd7` |
| Red Accent | `#ff2a1f` or `#FF5A52` | readmecodegen / Iconify `%23ff2a1f` |
| Green Accent | `#11c866` or `#4EAA25` | Iconify SVG color `%2311c866` |
