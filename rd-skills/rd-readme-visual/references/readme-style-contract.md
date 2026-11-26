# README Style Contract

Use this reference while generating the final README. For detailed icon and badge mechanics, read `icons-and-shields.md` and `local-visual-archetypes.md`.

---

## 1. Centered Hero Block Requirement

Every README generated with this skill MUST start with a centered header block inside a `<div align="center">` tag. Each child also needs its own `align="center"`. The classic shape is below; the modern shieldcn shape is in `shieldcn-recipes.md`:

```html
<div align="center">
  <img src="assets/icon.png" alt="Project Icon" width="120">

  <h1 align="center">PROJECT TITLE</h1>

  <p align="center"><strong>A single-sentence bold summary statement of core utility.</strong></p>

  <p>
    [![BADGE1](https://img.shields.io/badge/LABEL-MSG-1e1e1e?style=for-the-badge&logo=slug&logoColor=white)](LINK)
    [![BADGE2](https://img.shields.io/badge/LABEL-MSG-1e1e1e?style=for-the-badge&logo=slug&logoColor=white)](LINK)
  </p>

  <p>
    [Quick Start](#quick-start) • [Features](#features) • [Structure](#structure) • [Usage](#usage)
  </p>
</div>

---
```

---

## 2. Iconify & SVG Section Headers

Section headings (`##`) must include an inline Iconify SVG or readmecodegen icon for visual accents matching the project's color theme:

```markdown
## <img src="https://api.iconify.design/mdi:rocket-launch-outline.svg?color=%2301acd7" height="22"> Quick Start
```

Or readmecodegen icons:

```markdown
## ![terminal](https://www.readmecodegen.com/api/social-icon?name=terminal&size=18&animation=fade&color=%23ff2a1f) Quick Start
```

URL-encoded hex colors (`#` becomes `%23`):
- Cyan: `%2301acd7` or `%2306B6D4`
- Red: `%23ff2a1f` or `%23FF5A52`
- Green: `%2311c866` or `%234EAA25`
- Gold: `%23faa701`

---

## 3. Dark Badge Palette Signature (classic family)

Modern READMEs use adaptive shieldcn badges (`shieldcn-recipes.md`). In the classic family, prefer dark background shield badges (`#1e1e1e` or `#111111`) with `style=for-the-badge` and vibrant brand logos (`logoColor=white` or `logoColor=faa701`):

```markdown
[![ZSH](https://img.shields.io/badge/shell%20—%20zsh-1e1e1e?style=for-the-badge&logo=gnu-bash&logoColor=white)](https://www.zsh.org/)
[![PLATFORM](https://img.shields.io/badge/System%20—%20macOS-1e1e1e?style=for-the-badge&logo=apple&logoColor=white)](https://www.apple.com/macos/)
```

---

## 4. Visual Structure Elements

### Directory Tree Codeblocks
Always present project structures in fenced codeblocks with inline comments explaining file responsibilities:

```text
my-project/
├── bin/                       # Executable CLI binaries
├── config/                    # Configuration settings & defaults
├── src/                       # Primary runtime application source code
└── README.md                  # Comprehensive visual documentation
```

### Structured Data Tables
Use Markdown tables for configurations, commands, features, providers, modules, keyboard macros, and flags:

```markdown
| Parameter | Default | Description |
| --- | --- | --- |
| `DRY_RUN` | `false` | Preview mode without modifying system state |
```

### Collapsible Section Cards (`<details><summary>`)
Wrap verbose command lists, deep reference documentation, secondary configurations, or layout presets inside collapsible summary cards:

```html
<details>
<summary><strong>Show full directory tree…</strong></summary>

```text
...
```

</details>
```

### GitHub Alert Callouts
Use alerts strictly for setup requirements, warnings, or tips:

```markdown
> [!TIP]
> Run `./configure` on fresh installs to automatically populate environment settings.
```

---

## 5. Media & Showcase Grids

For repositories with visual outputs, videos, or UI components, present demo assets in side-by-side HTML tables:

```html
<table>
  <tr>
    <td width="50%" align="center">
      <img src="assets/demo1.png" width="100%" alt="Demo 1">
      <br>
      <strong>Demo 1 - Feature A</strong>
    </td>
    <td width="50%" align="center">
      <img src="assets/demo2.png" width="100%" alt="Demo 2">
      <br>
      <strong>Demo 2 - Feature B</strong>
    </td>
  </tr>
</table>
```
