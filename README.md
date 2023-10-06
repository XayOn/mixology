# mixology

[![PyPI - Version](https://img.shields.io/pypi/v/mixology.svg)](https://pypi.org/project/mixology)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mixology.svg)](https://pypi.org/project/mixology)

---

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [Usage](#Usage)

## Installation

```console
pip install mixology
```

## License

`mixology` is distributed under the terms of the [GPL-3.0](https://spdx.org/licenses/GPL-3.0.html) license.

## Usage

Mixology sets up an API to interface with a relay-based tasmota device.
This in turn can be integrated in tools such as a [Drinkable fork](https://github.com/XayOn/mixologist)
wich allows you to setup the API URL for this.

All this, setup with MQTT using mqtt authorization, inspired on most esp-based devices,
allowing easy configuration

Configuration setup is as follows:

- Generate random uuids
- Setup tasmota (see setup tasmota section)
- Setup mongodb configuration

### Setup tasmota

Flash tasmota into your 8-relay generic tasmota-ready device with the following user-config.h:

```c

# ifdef MQTT_HOST
#undef  MQTT_HOST
#endif

#define MQTT_HOST         "your.mqtt-host.com"
#ifdef MQTT_PORT
#undef  MQTT_PORT
#endif
#define MQTT_PORT         18917
#
#ifdef MQTT_USER
#undef  MQTT_USER
#endif
#define MQTT_USER         "random_uuid_1"
#
#ifdef MQTT_PASS
#undef  MQTT_PASS
#endif
#define MQTT_PASS         "random_uuid_2"
#
#
#ifdef FRIENDLY_NAME
#undef FRIENDLY_NAME
#endif
#define FRIENDLY_NAME          "Mixology"
#
#
#ifdef APP_LEDSTATE
#undef APP_LEDSTATE
#endif
#define APP_LEDSTATE           LED_OFF
#
#ifdef APP_LEDMASK
#undef APP_LEDMASK
#endif
#define APP_LEDMASK            0xFFFF
#
#
#
#ifdef MODULE
#undef MODULE
#endif
#define MODULE                 USER_MODULE
#
#ifdef FALLBACK_MODULE
#undef FALLBACK_MODULE
#endif
#define FALLBACK_MODULE        USER_MODULE
#
#ifdef USER_TEMPLATE
#undef USER_TEMPLATE
#endif
#define USER_TEMPLATE "{\"NAME\":\"ESP12F_Relay_X8\",\"GPIO\":[229,1,1,1,230,231,0,0,226,227,225,228,224,1],\"FLAG\":0,\"BASE\":18}"

```

- Now, setup a mongodb document like so:

```json
{
    "key" : "random_uuid_1",
    "token" : "random_uuid_2",
    "tasmotas" : [
        {
            "name" : "tasmota_name",
            "wifi" : "tasmota_name",
            "relays" : [
                NumberInt(2),
                NumberInt(3),
                NumberInt(4),
                NumberInt(5),
                NumberInt(6),
                NumberInt(7)
            ]
        }
    ]
}
```

Note that the relays might vary.

Now, generate a QR code pointing to `your-mixology-url/setup/?key={random_uuid_1}&token={random_uuid_2}`
Note that you should build the drinkable for with your own mixologist API url.
