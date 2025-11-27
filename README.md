# Surface WiFi Fix Home Assistant Integration

This repository now follows the Home Assistant core component layout (see [`homeassistant/components/blink`](https://github.com/home-assistant/core/tree/dev/homeassistant/components/blink) for a reference). The integration lives under `custom_components/surface_wifi_fix/` so it can be dropped directly into your Home Assistant configuration or added through HACS as a custom repository.

## What it does
- Disables Wi-Fi power saving on Microsoft Surface devices by issuing `iw`/`iwconfig` commands for the configured interface (default: `wlp3s0`).
- Exposes an admin-only service **`surface_wifi_fix.disable_power_save`** so you can re-run the commands on demand or target a different interface temporarily.

## Installation
1. Copy the `custom_components/surface_wifi_fix/` directory into your Home Assistant `config/custom_components/` folder (the same structure Home Assistant Core uses for integrations like Blink or SmartThings), or add this repository as a custom HACS source and install it.
2. Restart Home Assistant.
3. Go to **Settings → Devices & Services → + Add Integration** and pick **Surface WiFi Fix**.
4. Enter the Wi-Fi interface name (default `wlp3s0`) and finish the flow. The integration immediately applies the power-save fix for that interface and registers the service.

## Service usage
Call `surface_wifi_fix.disable_power_save` from **Developer Tools → Services**. Optionally pass `interface: <name>` to override the configured interface for a single run.

## Repository layout
- `custom_components/surface_wifi_fix/` — Home Assistant integration package following the same layout as core components.
- `surface_wifi_fix/` — Legacy Supervisor add-on assets (retained for reference; the new integration supersedes the add-on for applying the Wi-Fi fix from inside Home Assistant).
