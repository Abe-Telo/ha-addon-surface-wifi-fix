# Surface WiFi Fix Home Assistant Add-on

This add-on is designed for Home Assistant OS running on Microsoft Surface devices
using the Marvell/mwifiex WiFi chipset. It disables WiFi power saving on boot to
reduce random disconnects and timeouts.

## Features

- Runs on HAOS as a Supervisor add-on
- Uses `iw` and `iwconfig` to turn off WiFi power saving on interface `wlp3s0`
- Starts automatically on system boot
- Requires `host_network: true` and `NET_ADMIN` privileges

## Installation

1. In Home Assistant, go to **Settings → Add-ons → Add-on Store**.
2. Click the three dots (⋮) → **Repositories**.
3. Add this repo URL: `https://github.com/YOUR_GITHUB/ha-addon-surface-wifi-fix`.
4. Click **Add**, then search for **Surface WiFi Fix** in the add-on list.
5. Install the add-on.
6. Open the add-on page:
   - Enable **Start on boot**
   - Enable **Watchdog** (optional)
   - Click **Start**.

## Verification

1. SSH to the HAOS host (or use the Terminal & SSH add-on).
2. Run:
   ```sh
   iwconfig wlp3s0
