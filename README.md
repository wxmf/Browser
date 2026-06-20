# BrowserSpoof

Simple browser launcher made with Python and Selenium.

BrowserSpoof lets you launch Chrome, Firefox or Edge with custom settings such as location, proxy, user-agent, resolution, theme and more.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue">
  <img src="https://img.shields.io/badge/Selenium-Supported-green">
  <img src="https://img.shields.io/badge/License-MIT-yellow">
</p>

## Showcase

https://youtu.be/tI8FNvQv-Bc


## Features

* Chrome, Firefox and Edge support
* HTTP and SOCKS5 proxies
* Random or custom User-Agent
* Location and timezone spoofing
* WebRTC blocking
* Custom resolutions
* Dark and light themes
* Headless mode
* Incognito mode
* Extension support
* Presets system
* Discord Rich Presence

## Installation

```bash
git clone https://github.com/wxmf/BrowserSpoof.git
cd BrowserSpoof

pip install selenium rich pyfiglet pypresence
```

## Usage

```bash
python BrowserSpoof.py
```

## Notes

* Configurations can be saved and loaded with presets.
* Presets are stored in `presets.json`.
* Temporary browser profiles are created automatically.
* Discord Rich Presence is optional.

## License

MIT License © 2026 Dopa
