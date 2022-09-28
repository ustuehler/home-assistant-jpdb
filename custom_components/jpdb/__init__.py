"""The jpdb integration."""

import asyncio
import logging

from jpdb import JPDB
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, \
    UpdateFailed

from .const import PLATFORMS, DOMAIN, SCAN_INTERVAL, CONF_USERNAME, \
    CONF_PASSWORD, DATA_DUE_ITEMS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    jpdb = JPDB(username=username, password=password)

    coordinator = JPDBDataUpdateCoordinator(hass, jpdb)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        coordinator.platforms.append(platform)
        await hass.async_add_job(
            hass.config_entries.async_forward_entry_setup(
                entry, platform
            )
        )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )

    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload a config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


class JPDBDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from jpdb."""

    def __init__(self, hass: HomeAssistant, jpdb: JPDB) -> None:
        """Initialize the data update coordinator."""
        self.jpdb = jpdb
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN,
                         update_interval=SCAN_INTERVAL)

    async def _async_update_data(self) -> dict[str, any]:
        """Update data via library."""
        try:
            return {
                DATA_DUE_ITEMS: await self.hass.async_add_executor_job(
                    lambda: self.jpdb.due_items)
            }
        except Exception as exception:
            raise UpdateFailed() from exception
