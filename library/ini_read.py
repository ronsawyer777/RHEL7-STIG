#!/usr/bin/python
# WANT_JSON

DOCUMENTATION = '''
---
module: ini_read
short_description: Reads values from an ini file. 
'''

# Example:
# ini_read:
#   section: org/gnome/desktop
#   option: lock-screen
#   path: /etc/dconf/local.d/00-screensaver

from ansible.constants import mk_boolean
from ansible.module_utils.basic import *
import json
import ConfigParser

def ini_read(data):
    result = {}

    config = ConfigParser.ConfigParser()
    config.readfp(open(data["path"]))
    try:
        value = config.get(data["section"], data["option"])
        if data["state"] == "present":
            result["path"] = data["path"]
            result["value"] = value
    except ConfigParser.NoOptionError, ConfigParser.NoSectionError:
        if data["state"] == "absent":
            result["path"] = data["path"]

    return result

def main():
    fields = {
        "section": {"required": True, "type": "str"},
        "option": {"required": True, "type": "str" },
        "path": {"required": True, "type": "str"},
        "state": {
            "default": "present",
            "choices": ["present", "absent"],
            "type": "str"
        }
    }

    module = AnsibleModule(argument_spec=fields)
    result = ini_read(module.params)
    module.exit_json(ini_read=result)

if __name__ == "__main__":
    main()


