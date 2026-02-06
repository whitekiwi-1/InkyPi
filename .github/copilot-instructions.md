## InkyPi — Copilot instructions (short & actionable)

Purpose: help an AI coding agent become productive quickly in this repository by surfacing the project's architecture, key workflows, conventions and concrete file examples.

1) Big-picture architecture (what to read first)
- Entrypoint: `src/inkypi.py` — bootstraps Flask, loads `Config`, `DisplayManager`, `RefreshTask` and plugin blueprints.
- Configuration: `src/config.py` (device config lives in `src/config/device.json`; `device_dev.json` for `--dev`).
- Display stack: `src/display/display_manager.py` picks a backend (Mock / Inky / Waveshare). Mock writes images to `mock_display_output/latest.png` (see `src/display/mock_display.py`).
- Plugins: `src/plugins/*` — each plugin is a folder with `plugin-id.py`, `plugin-info.json`, optional `settings.html` and templates in the plugin folder. Plugin loading happens in `src/plugins/plugin_registry.py`.
- Web layer: blueprints in `src/blueprints/` (main, settings, plugin, playlist) and templates in `templates/` + plugin folders.

2) Key developer workflows (concrete commands & locations)
- Local development without hardware (recommended):
  - Create venv and install dev deps: `python3 -m venv venv && source venv/bin/activate && pip install -r install/requirements-dev.txt`.
  - Run dev server: `python src/inkypi.py --dev` — serves on port 8080 and uses `src/config/device_dev.json`.
  - Check rendered output: `mock_display_output/latest.png` and time-stamped PNGs in the same folder.
- Production / device installation:
  - Install the app and systemd service: `sudo bash install/install.sh [-W <waveshare_model>]`.
  - Service: `/etc/systemd/system/inkypi.service`; CLI wrapper copied to `/usr/local/bin/inkypi` by the install script.
  - Update/uninstall: `sudo bash install/update.sh` / `sudo bash install/uninstall.sh`.

3) Project-specific conventions & patterns
- Plugins: plugin directory name == plugin id. `plugin-info.json` is used to discover plugins (`Config.read_plugins_list()`); `plugin_registry.load_plugins()` expects the plugin module to export the class named in the plugin config (`plugin.get("class")`). Example: `plugins/clock/clock.py` with `plugin-info.json`.
- Display selection: `display_type` in device.json controls behavior. Valid values: `mock`, `inky`, or Waveshare models matching `epd*in*` (see `DisplayManager` logic in `src/display/display_manager.py`).
- Config read/write: `Config` caches config and exposes `get_config(key)`, `get_plugins()`, `get_resolution()` and `update_value(key, value, write=True)` — update config through these helpers rather than editing files in-place if possible.
- Image locations: current shown image -> `src/static/images/current_image.png` (Config.current_image_file). Plugin image dir -> `src/static/images/plugins`.

4) Integration points & external dependencies
- Waveshare drivers: installer optionally downloads a driver into `src/display/waveshare_epd/` when you run `install/install.sh -W <model>`; this is handled in the script `install/install.sh`.
- Hardware-only imports are optional and guarded — code intentionally falls back to software (see `display_manager` guards). Use `--dev` to avoid hardware dependencies.
- Web server: uses `waitress` in production; running via `python src/inkypi.py --dev` uses the same code path but different port and config.

5) Where to look for examples
- Plugin example: `src/plugins/clock/` (plugin code, `plugin-info.json`, `settings.html`).
- Mock render: `src/display/mock_display.py` and `mock_display_output/` directory.
- Installer & systemd wiring: `install/install.sh`, `install/inkypi` (CLI), `install/inkypi.service`.
- Config & logging: `src/config.py` and `src/config/logging.conf`.

6) Small contract for code changes (quick checklist for an AI)
- Inputs: change description and target files. Output: minimal, well-tested edits that keep dev mode functional (`python src/inkypi.py --dev`) and do not break installation scripts.
- Edge cases: changes must preserve `--dev` path (no hardware imports at top-level), preserve plugin discovery via `plugin-info.json`, and maintain `device.json` shape (resolution, display_type, playlist_config).

If a section is unclear or you'd like more examples (for instance a sample plugin skeleton or a quick unit-test harness), tell me which area and I'll extend this file.
