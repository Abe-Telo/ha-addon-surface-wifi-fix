# Surface WiFi Fix Home Assistant Add-on Repository

This repository hosts a custom Home Assistant Supervisor add-on that disables Wi-Fi power saving on Microsoft Surface devices running Home Assistant OS.

## Add-on Contents

The add-on lives in `surface_wifi_fix/` and includes:

- `config.json` — Home Assistant add-on manifest configured for automatic startup with host networking and `NET_ADMIN` privileges.
- `Dockerfile` — Builds from the Home Assistant base image and installs `iw`, `wireless-tools`, `ethtool`, and `busybox-extras`.
- `run.sh` — Applies Wi-Fi power-save fixes to `wlp3s0` (or a user-specified interface) and keeps the container alive.
- `README.md` — Usage instructions for the add-on itself.

## Installation in Home Assistant

1. In Home Assistant, open **Settings → Add-ons → Add-on Store**.
2. Click the three dots (⋮) → **Repositories**.
3. Add this repository URL: `https://github.com/YOUR_GITHUB/ha-addon-surface-wifi-fix`.
4. After the repository refreshes, install **Surface WiFi Fix**.
5. On the add-on page, enable **Start on boot** and optionally enable **Watchdog**.
6. Click **Start** to apply the fix.

> **Tip:** The add-on will only appear in the store if your Home Assistant hardware matches one of the supported architectures (AMD64, AArch64, ARMv7, or ARMhf). Make sure your system is on one of these platforms when browsing the repository.

## Verifying the Fix

1. SSH to the HAOS host (or use the Terminal & SSH add-on).
2. Run:
   ```sh
   iwconfig wlp3s0
   ```
3. Confirm the output shows `Power Management:off` for the interface.

If your Wi-Fi interface is not `wlp3s0`, set the `WIFI_INTERFACE` environment variable in the add-on options and restart the add-on.
