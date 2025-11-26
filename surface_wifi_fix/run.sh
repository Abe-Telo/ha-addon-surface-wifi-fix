#!/bin/sh

IFACE_DEFAULT="wlp3s0"
IFACE="${WIFI_INTERFACE:-${IFACE_DEFAULT}}"

# Prefer the Supervisor options file when available
if [ -r /data/options.json ]; then
  OPTION_IFACE=$(jq -er '.wifi_interface // empty' /data/options.json 2>/dev/null || true)
  if [ -n "${OPTION_IFACE}" ]; then
    IFACE="${OPTION_IFACE}"
  fi
fi

echo "Surface WiFi Fix: starting up, target interface: ${IFACE}"

# Try up to 10 times (about 50s) to find the WiFi interface
for i in $(seq 1 10); do
  if iw dev "${IFACE}" info >/dev/null 2>&1; then
    echo "Surface WiFi Fix: ${IFACE} detected, applying power-save fixes"

    iw dev "${IFACE}" set power_save off \
      && echo "Surface WiFi Fix: iw power_save off applied" \
      || echo "Surface WiFi Fix: power_save off not supported via iw"

    iwconfig "${IFACE}" power off \
      && echo "Surface WiFi Fix: iwconfig power off applied" \
      || echo "Surface WiFi Fix: power off not supported via iwconfig"

    break
  else
    echo "Surface WiFi Fix: ${IFACE} not found yet (attempt ${i}/10), retrying in 5s..."
    sleep 5
  fi

done

# Keep container running so Supervisor sees it as 'running'
echo "Surface WiFi Fix: entering idle loop (tail -f /dev/null)"
tail -f /dev/null
