import logging

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_TITLE, CONF_USERNAME, CONF_PASSWORD
from jpdb import JPDB, JPDBLoginError

_LOGGER = logging.getLogger(__name__)

USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): str,
    vol.Required(CONF_PASSWORD): str,
})


async def validate_input(
        hass: HomeAssistant,
        user_input: dict
) -> dict[str, any]:
    """Verify that the user input allows us to connect to jpdb.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    username = user_input[CONF_USERNAME]
    password = user_input[CONF_PASSWORD]

    try:
        jpdb = JPDB(username=username, password=password)
        await hass.async_add_executor_job(jpdb.login)
    except JPDBLoginError:
        raise InvalidAuth

    return {
        CONF_TITLE: username,
        'data': {
            CONF_USERNAME: username,
            CONF_PASSWORD: password,
        }
    }


class JPDBConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for jpdb."""

    async def async_step_user(
            self,
            user_input: dict[str, any] or None = None
    ) -> FlowResult:
        errors = {}
        if user_input is not None:
            # noinspection PyBroadException
            try:
                entry = await validate_input(self.hass, user_input)

                await self.async_set_unique_id(entry[CONF_TITLE])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(**entry)
            except InvalidAuth:
                errors['base'] = 'invalid_auth'
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors['base'] = 'unknown'

        return self.async_show_form(
            step_id='user',
            data_schema=USER_DATA_SCHEMA,
            errors=errors
        )


class InvalidAuth(exceptions.ConfigEntryAuthFailed):
    """Error to indicate an invalid username or password."""
