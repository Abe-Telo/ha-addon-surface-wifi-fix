# Surface WiFi Fix Add-on

This Home Assistant Supervisor add-on disables Wi-Fi power saving on Surface devices (interface `wlp3s0` by default) to reduce random disconnects and timeouts.

## How It Works

- Builds from `ghcr.io/home-assistant/amd64-base:3.19` and installs `iw`, `wireless-tools`, `ethtool`, and `busybox-extras` at image build time.
- Runs `run.sh` at startup, which waits for the Wi-Fi interface, applies `iw dev <iface> set power_save off` and `iwconfig <iface> power off`, then stays running.
- Uses `host_network: true` and `NET_ADMIN` privileges so it can manage the host Wi-Fi interface from inside the add-on container.

## Configuration

- Defaults to interface `wlp3s0`.
- Override the interface by setting the `WIFI_INTERFACE` environment variable in the add-on options.

## Installation

1. Add this repository to Home Assistant: **Settings → Add-ons → Add-on Store → ⋮ → Repositories** → `https://github.com/Abe-Telo/ha-addon-surface-wifi-fix`.
2. Install **Surface WiFi Fix** from the add-on list.
3. Enable **Start on boot** and optionally **Watchdog**.
4. Click **Start**.

## Verification

1. SSH to HAOS (or use Terminal & SSH add-on).
2. Run `iwconfig wlp3s0` (or your chosen interface).
3. Confirm the output shows `Power Management:off`.

## Files

- `config.json` — Add-on manifest (auto start, services stage, host networking, `NET_ADMIN`).
- `Dockerfile` — Base image and tool installation.
- `run.sh` — Wi-Fi power-save disable script with retry loop and idle tail.
