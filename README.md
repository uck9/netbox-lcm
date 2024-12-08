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

|        | Netbox 3.2.x   | NetBox 4.1.x   | 
|--------|----------------|----------------|
| 1.0.0+ | Not Compatible | Compatible     |

## Installation

To install, simply include this plugin in the plugins configuration section of netbox.

Example:
```python
    PLUGINS = [
        'netbox_lcm'
    ],
```

## Configuration

None

## Usage

TBD

## Additional Notes

TBD

## Contribute

Contributions are always welcome!  Please open an issue first before contributing as the scope is going to be kept
intentionally narrow

