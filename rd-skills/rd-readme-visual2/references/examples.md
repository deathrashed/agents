# Before / After Examples

Common mistakes and their fixes. Load when reviewing a draft.

### Badge Organization

**❌ BAD: All badges crammed together**
```html
<p><img src="...badge1..."> <img src="...badge2..."> <img src="...badge3..."> <img src="...badge4..."> <img src="...badge5..."> <img src="...badge6..."></p>
```
→ Wraps badly on mobile, hard to scan, no organization

**✅ GOOD: Themed rows with links**
```html
<p align="center">
  <a href="..."><img src="...badge1..." alt="Platform"></a>
  <a href="..."><img src="...badge2..." alt="Runtime"></a>
  <a href="..."><img src="...badge3..." alt="License"></a>
</p>

<p align="center">
  <a href="..."><img src="...badge4..." alt="Tool"></a>
  <a href="..."><img src="...badge5..." alt="Status"></a>
</p>
```
→ Organized by category, clickable, mobile-friendly

---

### Hero Block Centering

**❌ BAD: Only wrapper centered**
```html
<div align="center">
  <img src="logo.png" width="200">
  <h1>Project Name</h1>
  <p>Description</p>
</div>
```
→ GitHub doesn't inherit `align` to children; looks left-aligned

**✅ GOOD: Every element centered**
```html
<div align="center">
  <img src="logo.png" width="200" align="center">
  <h1 align="center">Project Name</h1>
  <p align="center"><strong>Description</strong></p>
</div>
```
→ Everything actually centers on GitHub

---

### Code Examples

**❌ BAD: No context, no language tag**
```
git clone https://github.com/user/repo.git
cd repo
npm install
npm start
```
→ No syntax highlighting, unclear what language

**✅ GOOD: Clear context, language specified**
```bash
# Clone and setup
git clone https://github.com/user/repo.git
cd repo

# Install dependencies
npm install

# Start development server
npm start
```
→ Syntax highlighting, comments explain each step

---

### Badge & Reference Links

**❌ BAD: Broken links**
```html
<a href="https://example.com/doesnt/exist"><img src="badge.svg" alt="Tool"></a>
<a href="#configuration"><img src="badge.svg" alt="Config"></a>

<!-- But section is actually called "Configure" not "Configuration" -->
## Configure
```
→ Badges click to 404; internal links lead nowhere

**✅ GOOD: All links validated**
```html
<!-- External links point to real resources -->
<a href="https://www.python.org/downloads/"><img src="badge.svg" alt="Python 3"></a>
<a href="https://github.com/user/repo/blob/main/docs/CONTRIBUTING.md"><img src="badge.svg" alt="Contributing"></a>

<!-- Internal links match actual section headers exactly -->
<a href="#configuration"><img src="badge.svg" alt="Config"></a>

... content ...

## Configuration
```
→ Every link is live; TOC anchors work; trust preserved

---

### Section Headers

**❌ BAD: Plain text**
```markdown
## Installation
## Usage
## Configuration
```
→ Looks boring, no visual hierarchy

**✅ GOOD: Iconify headers**
```markdown
## <img src="https://api.iconify.design/mdi:download.svg?color=%23622284" height="22"> Installation
## <img src="https://api.iconify.design/mdi:play.svg?color=%23622284" height="22"> Usage
## <img src="https://api.iconify.design/mdi:cog.svg?color=%23622284" height="22"> Configuration
```
→ Visual scanning is faster, colors match brand

---

## Red Flags & Corrections

| Claim | Reality |
| --- | --- |
| Plain `# Title` header is enough | Every reference README opens with a centred `<div align="center">` top block |
| `align="center"` on the wrapper div is enough | GitHub does not inherit it — every hero child needs its own `align="center"` |
| Standard GitHub badges are fine | Adaptive shieldcn outline badges (modern) or dark `#1e1e1e` shields (classic), in the README's palette |
| Any badge colors will do | Badge + Iconify colors should derive from the header image palette (or be confirmed with the user) |
| **NEVER: Emojis in headers** | ❌ `## 🚀 Quick Start` ❌ Emojis render differently on each OS/device. Use Iconify SVG only. |
| **NEVER: Emoji anywhere visual** | ❌ Emoji bullets, emoji badges, emoji section markers. They look broken on Linux/old browsers. Iconify + SVG only. |
| All badges in one giant row | Split into themed rows (integrations, platform, dependencies, license) for readability |
| Using shields.io for everything | Modern READMEs use shieldcn; `custom-icon-badges.demolab.com` covers logos neither has |
| Broken badge/reference links | Every badge `<a href>` must point to real resource; every internal link must match actual header |
| Bullets links wrapping badges | Always wrap badges in `<a>` tags so they're clickable and semantic |
| Bullet lists replace ASCII trees | Trees in code blocks are faster to scan |
| 50 lines of setup inline | Wrap in `<details><summary>` collapsible cards |
| Single archetype for all projects | Vary header, sections, and signature elements per project (see SKILL.md "§4 Style" and `local-visual-archetypes.md`) |
| Plain text license at bottom | Centred, clickable license block from the gupload library (`references/licenses.md`) |
| License text only | Make logo, text, and badge all clickable for better UX |
