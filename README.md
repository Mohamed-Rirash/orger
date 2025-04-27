# Orgi – File Organizer CLI

A sleek and intuitive command‑line utility to automatically sort and organize files in your Downloads (or any specified) folder into date‑based directories and type‑based categories. Keep your workspace tidy with minimal effort.

[![PyPI Version](https://img.shields.io/pypi/v/orgi.svg)](https://pypi.org/project/orgi/) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://chatgpt.com/c/LICENSE) [![Build Status](https://github.com/Mohamed-Rirash/orgi/actions/workflows/ci.yml/badge.svg)](https://github.com/Mohamed-Rirash/orgi/actions)

---

## 📋 Table of Contents

1. [Features](https://chatgpt.com/c/680e5669-578c-800e-ae77-616066080827#-features)
    
2. [Quick Start](https://chatgpt.com/c/680e5669-578c-800e-ae77-616066080827#-quick-start)
    
    - [Curl Installer](https://chatgpt.com/c/680e5669-578c-800e-ae77-616066080827#curl-installer)
        
    - [Pip Install](https://chatgpt.com/c/680e5669-578c-800e-ae77-616066080827#pip-install)
        
3. [Usage](https://chatgpt.com/c/680e5669-578c-800e-ae77-616066080827#-usage)
    
4. [Configuration](https://chatgpt.com/c/680e5669-578c-800e-ae77-616066080827#-configuration)
    
5. [Examples](https://chatgpt.com/c/680e5669-578c-800e-ae77-616066080827#-examples)
    
6. [Contributing](https://chatgpt.com/c/680e5669-578c-800e-ae77-616066080827#-contributing)
    
7. [License](https://chatgpt.com/c/680e5669-578c-800e-ae77-616066080827#-license)
    

---

## ✨ Features

- **Source Directory**: Defaults to `~/Downloads`, override with `--src <path>`
    
- **Date‑Based Folders**: Automatically creates a folder named after today’s date (`YYYY-MM-DD`)
    
- **Type Classification**: Files sorted into subfolders:
    
    - `images/` (e.g., `.png`, `.jpg`, `.gif`)
        
    - `videos/` (e.g., `.mp4`, `.mkv`)
        
    - `documents/` (e.g., `.pdf`, `.docx`, `.txt`)
        
    - `music/` (e.g., `.mp3`, `.wav`)
        
    - `others/` (any uncategorized types)
        
- **Cross‑Platform**: Works on Linux, macOS (Windows support coming)
    
- **Lightweight**: No heavy dependencies, easy to install and run
    

---

## ⚡ Quick Start

### Curl Installer

```bash
curl -sSL https://raw.githubusercontent.com/Mohamed-Rirash/orgi/main/install.sh | bash
```

This will download the script, install dependencies, and set up the `orgi` command.

### Pip Install

```bash
pip install orgi
```

Alternatively, clone the repo and install manually:

```bash
git clone https://github.com/Mohamed-Rirash/orgi.git
cd orgi
python3 -m pip install -r requirements.txt
python3 -m pip install .
```

---

## 🚀 Usage

Run the organizer on your default Downloads folder:

```bash
orgi auto
```

Specify a custom source directory:

```bash
orgi auto --src /path/to/your/folder
```

Use `--help` to see all available options:

```bash
orgi --help
```

![Screenshot of Orgi in action](https://chatgpt.com/c/docs/screenshot.png)

---

## ⚙️ Configuration

Orgi supports optional configuration via `~/.orgirc`:

```ini
[src]
path = /Users/you/Downloads

[categories]
images = .png,.jpg,.jpeg,.gif
videos = .mp4,.avi,.mkv
documents = .pdf,.docx,.txt
music = .mp3,.wav
others =
```

Load custom settings with:

```bash
orgi auto --config /path/to/.orgirc
```

---

## 🎬 Examples

Organize today’s downloads in a demo folder:

```bash
orgi auto --src ./demo_downloads
```

![Animated demo of file organization](https://chatgpt.com/c/docs/demo.gif)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Open issues for suggestions or bugs
    
- Submit pull requests with improvements
    

Please follow the [Code of Conduct](https://chatgpt.com/c/CODE_OF_CONDUCT.md) and check our [Contributing Guidelines](https://chatgpt.com/c/CONTRIBUTING.md).

---

## 📄 License

Distributed under the MIT License. See [LICENSE](https://chatgpt.com/c/LICENSE) for details.