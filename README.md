<div align="center">

# 🍚 RiceVault
**The Ultimate KDE Plasma Profile & Theme Manager**

**[🌐 Visit the Official Website to see it in action!](https://ricevault-6ql.pages.dev/)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![KDE Plasma](https://img.shields.io/badge/KDE-Plasma%206-232F3E.svg?logo=kde)](https://kde.org/plasma-desktop/)

RiceVault is a sleek, Git-like CLI tool that lets you backup, swap, and manage your KDE Plasma configurations ("rices") in seconds. Never lose your perfect desktop setup again.

<img src="https://raw.githubusercontent.com/tacenta2k/RiceVault/main/media/screenshots/hero.png" alt="RiceVault Hero" width="800">

</div>

---

## ⚡ Why RiceVault?
If you have ever spent hours customizing your KDE desktop (themes, window rules, panels, widgets) only to break it the next day, RiceVault is for you. 

* **Git-Like Workflow:** Easily backup and restore distinct desktop states.
* **Interactive CLI:** A beautiful, terminal-based wizard built with Typer and Rich.
* **Zero Configuration:** Automatically detects your Plasma config paths and saves backups straight to your `Documents` folder.
* **Safe Restores:** Automatically creates an emergency backup before applying any new theme.

---

## 🚀 Installation

RiceVault is built in Python and is best installed globally using `pipx` to keep its dependencies isolated.

```bash
# Install pipx if you don't have it (Arch/CachyOS)
sudo pacman -S python-pipx

# Clone the repository
git clone [https://github.com/TacentaXT/RiceVault.git](https://github.com/TacentaXT/RiceVault.git)
cd RiceVault

# Install globally
pipx install .
```

---

## 🛠️ Usage

### 1. Backing up a Theme
Run `rice backup` to launch the interactive wizard. It will securely copy your `kdeglobals`, `kwinrc`, and `plasmashellrc` into a secure vault in your Documents folder.

<div align="center">
  <img src="https://raw.githubusercontent.com/tacenta2k/RiceVault/main/media/gifs/backup.gif" alt="RiceVault Backup Demo" width="700">
</div>

### 2. Restoring a Theme
Want to switch back to a previous setup? Run `rice restore`, select your profile, and watch your desktop transform back instantly. 

<div align="center">
  <img src="https://raw.githubusercontent.com/tacenta2k/RiceVault/main/media/gifs/restore.gif" alt="RiceVault Restore Demo" width="700">
</div>

### 3. Managing the Vault
* `rice list` - View a formatted table of all your saved desktop profiles.
* `rice delete` - Safely remove an old backup.
* `rice info` - View developer and project info.

---

## 🗺️ Roadmap (Upcoming Features)
- [x] Core Backup & Restore engine
- [x] Interactive CLI UI
- [ ] **Phase 3:** Automatic Package Detection (Save lists of AUR/Arch packages used in a rice)
- [ ] **Phase 4:** Cloud Sync (Push rices directly to a GitHub gist)

---

## 💖 Support the Project

If RiceVault saved your setup (or just saved you some time), consider buying me a coffee! 

* **Ko-fi:** [ko-fi.com/tacenta](https://ko-fi.com/tacenta)
* **UPI:** `aswingk@ptyes`

<div align="center">
  <i>Built with 💙 for the Linux ricing community.</i>
</div>
