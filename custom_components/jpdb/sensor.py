"""Sensor platform for JPDB.io integration."""

from homeassistant.components.sensor import SensorEntity, CONF_STATE_CLASS, \
    SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_UNIT_OF_MEASUREMENT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import ICON, DOMAIN, DATA_DUE_ITEMS
from .entity import JPDBEntity


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback
) -> None:
    """Set up sensor platform for config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        JPDBDueItemsSensor(coordinator=coordinator, entry=entry),
    ], True)


class JPDBDueItemsSensor(JPDBEntity, SensorEntity):
    """Sensor class reporting the number of items due for review."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'JPDB Due Items'

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator.data[DATA_DUE_ITEMS]

    @property
    def extra_state_attributes(self):
        """Return the attributes of the sensor."""
        return {
            CONF_STATE_CLASS: SensorStateClass.MEASUREMENT,
            CONF_UNIT_OF_MEASUREMENT: 'cards',
        }
