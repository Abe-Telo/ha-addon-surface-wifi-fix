"""Surface WiFi Fix integration."""

from __future__ import annotations

import logging
import shutil
import subprocess
from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.helpers.typing import ConfigType

from .const import ATTR_INTERFACE, CONF_INTERFACE, DEFAULT_INTERFACE, DOMAIN, SERVICE_DISABLE_POWER_SAVE

_LOGGER = logging.getLogger(__name__)


SERVICE_SCHEMA = vol.Schema({vol.Optional(ATTR_INTERFACE): cv.string})


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Surface WiFi Fix integration (YAML not supported)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Surface WiFi Fix from a config entry."""

    interface = entry.options.get(CONF_INTERFACE, entry.data.get(CONF_INTERFACE, DEFAULT_INTERFACE))

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {CONF_INTERFACE: interface}

    _LOGGER.info("Setting up Surface WiFi Fix for interface %s", interface)

    if not hass.services.has_service(DOMAIN, SERVICE_DISABLE_POWER_SAVE):
        _LOGGER.debug("Registering %s.%s admin service", DOMAIN, SERVICE_DISABLE_POWER_SAVE)
        async_register_admin_service(
            hass,
            DOMAIN,
            SERVICE_DISABLE_POWER_SAVE,
            _async_handle_disable_service,
            schema=SERVICE_SCHEMA,
        )

    interface = entry.options.get(CONF_INTERFACE, entry.data.get(CONF_INTERFACE, DEFAULT_INTERFACE))
    _LOGGER.debug("Applying WiFi power-save fix during setup for %s", interface)
    await _async_disable_power_save(hass, interface)

    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))
    _LOGGER.debug("Surface WiFi Fix setup complete for entry %s", entry.entry_id)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    hass.data[DOMAIN].pop(entry.entry_id, None)
    if not hass.data[DOMAIN]:
        hass.data.pop(DOMAIN)
        hass.services.async_remove(DOMAIN, SERVICE_DISABLE_POWER_SAVE)

    return True


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle config entry updates by reapplying the power-save fix."""

    interface = entry.options.get(CONF_INTERFACE, entry.data.get(CONF_INTERFACE, DEFAULT_INTERFACE))
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {CONF_INTERFACE: interface}
    _LOGGER.info("Reloading Surface WiFi Fix entry %s for interface %s", entry.entry_id, interface)
    await _async_disable_power_save(hass, interface)


async def _async_handle_disable_service(hass: HomeAssistant, call: ServiceCall) -> None:
    """Handle manual service calls to reapply the WiFi fix."""

    interface = call.data.get(ATTR_INTERFACE) or _active_interface(hass)
    if not interface:
        raise HomeAssistantError("No interface configured for Surface WiFi Fix.")

    _LOGGER.info("Manual disable_power_save service invoked for interface %s", interface)
    await _async_disable_power_save(hass, interface)


def _active_interface(hass: HomeAssistant) -> str | None:
    """Return the active interface from the first loaded entry."""

    domain_entries: Mapping[str, Any] | None = hass.data.get(DOMAIN)
    if not domain_entries:
        return None

    first_entry: Mapping[str, Any] = next(iter(domain_entries.values()))
    return first_entry.get(CONF_INTERFACE)


async def _async_disable_power_save(hass: HomeAssistant, interface: str) -> None:
    """Run the power-save disable commands in the executor."""

    if not interface:
        raise HomeAssistantError("WiFi interface is required to disable power saving.")

    try:
        _LOGGER.info("Disabling WiFi power saving on %s", interface)
        await hass.async_add_executor_job(_disable_power_save, interface)
    except (HomeAssistantError, subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as err:
        _LOGGER.error("Failed to disable power saving on %s: %s", interface, err)
        raise HomeAssistantError(f"Failed to disable power saving on {interface}: {err}") from err


def _disable_power_save(interface: str) -> None:
    """Execute the commands that disable WiFi power saving."""

    commands = [
        ("iw", ["iw", "dev", interface, "set", "power_save", "off"]),
        ("iwconfig", ["iwconfig", interface, "power", "off"]),
    ]

    available_commands = 0
    for executable, cmd in commands:
        if not shutil.which(executable):
            _LOGGER.warning(
                "Skipping WiFi power-save command because %s is not available in the container.",
                executable,
            )
            continue

        _LOGGER.debug("Running WiFi power-save command: %s", " ".join(cmd))
        process = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=15)
        if process.stdout:
            _LOGGER.debug("%s output: %s", executable, process.stdout.strip())
        if process.stderr:
            _LOGGER.debug("%s errors: %s", executable, process.stderr.strip())
        available_commands += 1

    if available_commands == 0:
        _LOGGER.warning(
            "Surface WiFi Fix could not run because neither iw nor iwconfig is installed. "
            "Install wireless tools on the host or container to allow the integration to disable WiFi power saving."
        )

