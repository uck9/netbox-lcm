# NetBox Lifecycle Management Plugin

The Netbox Lifecycle Management plugin is a Hardware EOS/EOL, License and Support Contract tracking plugin for NetBox.

Forked from v1.1.3 of netbox_lifecycle (https://github.com/DanSheps/netbox-lifecycle).  Forked to permit some specific 
approaches required for the plugin.  Will attempt to maintain a level of parity+ with the original plugin.

NOT FOR GENERAL PRODUCTION USE AT THIS STAGE - STILL IN DEVELOPMENT AND MAY BE DISCARDED YET

## Features

* Tracking EOL/EOS data
* Tracking License
* Tracking Support Contracts

# Requirements

* Netbox 4.1+
* Python 3.10+

## Compatibility Matrix

|        | Netbox 3.2.x   | NetBox 4.1.x    | NetBox 4.2.x   | NetBox 4.3.x   |
|--------|----------------|-----------------|----------------|----------------|
| 1.0.0+ | Not Compatible |  Compatible     | Compatible     | Not Compatible |
| 1.1.7+ | Not Compatible |  Not Compatible | Not Compatible | Compatible     |

## Installation

To install, simply include this plugin in the plugins configuration section of netbox.

Example:
```python
    PLUGINS = [
        'netbox_lcm'
    ],
```

Note that this plugin does not support simultaeneous installation of the netbox_lifecycle plugin.

## Configuration

To use the sync_cisco_hw_eox_data command, you need to generate a client id and secret in the Cisco API console
for the support API and include them as part of the plugin configuration.  There also other options that can
be configured to manage the data import process from the script.

```python
    PLUGINS_CONFIG = [
        'netbox_lcm': {
            'cisco_support_api_client_id': '',      # Client ID for the Cisco Support API
            'cisco_support_api_client_secret': '',   # Client Secret for the Cisco Support API
            'lifecycle_only_active_pids': True,     # Only keep Lifecycle Data for PIDs we have as defined devices
            'api_is_source_of_truth': True,         # Data received from API is considered the soruce of truth and will overwrite non matching data
            'use_eos_for_missing': True,            # If a date is not returned, use end_of_support as the date to use, otherwise null values retained
            'hw_lcm_migration_calc_month': 6,       # Month used to calc replacement and budget years. Default is 6
        },
    ],
```

## Usage

TBD

## Additional Notes

TBD

## Contribute

Contributions are always welcome!  Please open an issue first before contributing to confirm reqirements.

