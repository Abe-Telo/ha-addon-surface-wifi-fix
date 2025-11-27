"""Surface WiFi Fix integration."""

from __future__ import annotations

import logging
import shutil
import subprocess
from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_INTERFACE
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.helpers.typing import ConfigType

from .const import ATTR_INTERFACE, DEFAULT_INTERFACE, DOMAIN, SERVICE_DISABLE_POWER_SAVE

_LOGGER = logging.getLogger(__name__)


SERVICE_SCHEMA = vol.Schema({vol.Optional(ATTR_INTERFACE): cv.string})


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Surface WiFi Fix integration (YAML not supported)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Surface WiFi Fix from a config entry."""

    interface = entry.options.get(CONF_INTERFACE, entry.data.get(CONF_INTERFACE, DEFAULT_INTERFACE))

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {CONF_INTERFACE: interface}

    if not hass.services.has_service(DOMAIN, SERVICE_DISABLE_POWER_SAVE):
        async_register_admin_service(
            hass,
            DOMAIN,
            SERVICE_DISABLE_POWER_SAVE,
            _async_handle_disable_service,
            schema=SERVICE_SCHEMA,
        )

    interface = entry.options.get(CONF_INTERFACE, entry.data.get(CONF_INTERFACE, DEFAULT_INTERFACE))
    await _async_disable_power_save(hass, interface)

    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))
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
    await _async_disable_power_save(hass, interface)


async def _async_handle_disable_service(hass: HomeAssistant, call: ServiceCall) -> None:
    """Handle manual service calls to reapply the WiFi fix."""

    interface = call.data.get(ATTR_INTERFACE) or _active_interface(hass)
    if not interface:
        raise HomeAssistantError("No interface configured for Surface WiFi Fix.")

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
        await hass.async_add_executor_job(_disable_power_save, interface)
    except (HomeAssistantError, subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as err:
        raise HomeAssistantError(f"Failed to disable power saving on {interface}: {err}") from err


def _disable_power_save(interface: str) -> None:
    """Execute the commands that disable WiFi power saving."""

    commands = [
        ("iw", ["iw", "dev", interface, "set", "power_save", "off"]),
        ("iwconfig", ["iwconfig", interface, "power", "off"]),
    ]

    for executable, cmd in commands:
        if not shutil.which(executable):
            raise HomeAssistantError(f"{executable} is not available in the container.")

        _LOGGER.debug("Running WiFi power-save command: %s", " ".join(cmd))
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=15)

