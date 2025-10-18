# Development Guide

This document provides an overview of the project structure and explains how the pieces fit together so that new contributors can start working on **FileMeQuietly**.

## Repository layout

```
filemequietly/
├── assets/                   # Images and audio used by the UI
├── host/                     # Classes responsible for hosting a file
├── pages/                    # Flet page implementations
├── tools/                    # Helper utilities (file downloader, sound player)
├── ui_kit/                   # Reusable UI widgets and theme helpers
├── utils/                    # Miscellaneous helper functions
├── main.py                   # Flet application entry point
└── requirements.txt          # Runtime dependencies
```
Other project files live in the repository root:

- `README.md` – short project description and basic usage.
- `requirements.txt` – same dependencies as the copy inside the package. When running from source, install these.

## Getting started

1. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```
2. **Run the app**
   Execute the main module:
   ```bash
   python filemequietly/main.py
   ```
   Flet will launch the GUI and you can start interacting with the pages.

The project does not currently include automated tests or a dedicated build script. Running `main.py` is enough to start a development instance.

## Code overview

### `main.py`
Creates the Flet application and handles page navigation. The `App` class stores some runtime state (like the Ngrok token and a host instance). It also provides helper methods for storing the token in Flet's client storage.

### Hosting a file
* Located in `host/`.
* `flask_app.py` spins up a minimal Flask server exposing routes for file download and host info.
* `ngrok_bridge.py` wraps the `ngrok` module and forwards the chosen port, returning a public URL.
* `host.py` combines both parts. It runs Flask and Ngrok inside a thread and exposes helper methods to stop sharing or update the file path.

### UI pages
Pages inherit from Flet `Container` or `Column` and implement navigation hooks:

* `start_page.py` – initial screen to pick between downloading or sharing.
* `share_file_page.py` – lets the user choose a file, manage permissions and respond to download requests.
* `download_file_page.py` – prompts for a host link and downloads the file while displaying progress.
* `ask_for_text_page.py` and `sharing_requirements_page.py` – small helper pages for text input and setting the Ngrok token.

### Utilities
* `utils/` holds small helper modules. Examples include `generate_client_code.py` for creating random client codes or `get_host_info.py` for retrieving metadata from a host.
* `tools/` contains higher level helpers such as `FileDownloader` which performs streamed downloads on a background thread.
* `ui_kit/` defines `page_theme` and `SettingsControlsOption` to keep the UI consistent.

## Making changes

1. Create a new branch for your work and commit changes with clear messages.
2. Keep UI code in `pages/` or `ui_kit/`, backend logic in `host/` or `tools/` as appropriate.
3. If you add external libraries, update `requirements.txt` in both the root and in the package directory.
4. Please run the application manually to ensure it still launches; automated tests are not yet in place.

## Contact
For questions about the code or to propose significant changes, open an issue on the repository.
