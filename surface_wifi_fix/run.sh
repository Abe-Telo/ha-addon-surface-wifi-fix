#!/bin/sh

IFACE="${WIFI_INTERFACE:-wlp3s0}"

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
