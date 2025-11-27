"""Config flow for Surface WiFi Fix."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import CONF_INTERFACE, DEFAULT_INTERFACE, DOMAIN


class SurfaceWiFiFixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Surface WiFi Fix."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""

        self._interface: str = DEFAULT_INTERFACE

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            interface: str = user_input[CONF_INTERFACE]
            self._interface = interface
            return self.async_create_entry(title="Surface WiFi Fix", data={CONF_INTERFACE: interface})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_INTERFACE, default=self._interface): cv.string,
                }
            ),
            errors=errors,
        )

    async def async_step_import(self, user_input: dict) -> FlowResult:
        """Handle import from YAML (not expected)."""

        return await self.async_step_user(user_input)

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Return the options flow handler."""

        return SurfaceWiFiFixOptionsFlow(config_entry)


class SurfaceWiFiFixOptionsFlow(config_entries.OptionsFlow):
    """Handle Surface WiFi Fix options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize Surface WiFi Fix options flow."""

        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> FlowResult:
        """Manage the options."""

        errors: dict[str, str] = {}

        if user_input is not None:
            return self.async_create_entry(title="Surface WiFi Fix", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_INTERFACE,
                        default=self.config_entry.options.get(
                            CONF_INTERFACE, self.config_entry.data.get(CONF_INTERFACE, DEFAULT_INTERFACE)
                        ),
                    ): cv.string,
                }
            ),
            errors=errors,
        )
