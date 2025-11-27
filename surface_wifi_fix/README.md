# Surface WiFi Fix Add-on (legacy)

> **Note:** The repository now ships a Home Assistant integration under `custom_components/surface_wifi_fix/` (matching the core component layout). This add-on directory is retained for reference; the integration is the recommended way to apply the Wi-Fi power-save fix from within Home Assistant itself.

This Home Assistant Supervisor add-on disables Wi-Fi power saving on Surface devices (interface `wlp3s0` by default) to reduce random disconnects and timeouts.

## How It Works

- Builds from the Supervisor-provided base image for your architecture (`ghcr.io/home-assistant/{arch}-base:3.19`, defined in `build.json`) and installs `iw`, `wireless-tools`, `ethtool`, and `busybox-extras` at image build time.
- Runs `run.sh` at startup, which waits for the Wi-Fi interface, applies `iw dev <iface> set power_save off` and `iwconfig <iface> power off`, then stays running.
- Uses `host_network: true` and `NET_ADMIN` privileges so it can manage the host Wi-Fi interface from inside the add-on container.

## Configuration

- Defaults to interface `wlp3s0`.
- Override the interface by setting the **wifi_interface** option in the add-on configuration UI (persisted in `/data/options.json`).

## Installation

1. Add this repository to Home Assistant: **Settings → Add-ons → Add-on Store → ⋮ → Repositories** → `https://github.com/Abe-Telo/ha-addon-surface-wifi-fix`.
2. Install **Surface WiFi Fix** from the add-on list.
3. Enable **Start on boot** and optionally **Watchdog**.
4. Click **Start**.

If the repository syncs but you still do not see the add-on, use **⋮ → Reload** in the Add-on Store, then check **Settings → System → Logs → Supervisor** for any repository fetch errors. A missing or invalid `build.json` can prevent the repository from listing.

## Verification

1. SSH to HAOS (or use Terminal & SSH add-on).
2. Run `iwconfig wlp3s0` (or your chosen interface).
3. Confirm the output shows `Power Management:off`.

## Files

- `config.json` — Add-on manifest (auto start, services stage, host networking, `NET_ADMIN`).
- `Dockerfile` — Base image and tool installation.
- `build.json` — Architecture-specific base images supplied to the Docker build.
- `run.sh` — Wi-Fi power-save disable script with retry loop and idle tail.

## Assets

The Supervisor UI icon and logo live in `icon.png` and `logo.png` respectively.
If you need to download them without pushing binaries, decode the included Base64
files:

```bash
base64 -d surface_wifi_fix/icon_base64.txt > surface_wifi_fix/icon.png
base64 -d surface_wifi_fix/logo_base64.txt > surface_wifi_fix/logo.png
```
