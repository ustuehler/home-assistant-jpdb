from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = 'jpdb'

PLATFORMS = [Platform.SENSOR]

ICON = 'mdi:cloud-braces'

CONF_TITLE = 'title'
CONF_USERNAME = 'username'
CONF_PASSWORD = 'password'

SCAN_INTERVAL = timedelta(minutes=15)

DATA_DUE_ITEMS = 'due_items'
