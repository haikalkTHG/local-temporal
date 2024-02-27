class NetboxMocks:
    @staticmethod
    def get_empty_response():
        return {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }

    @staticmethod
    def get_server_fixture():
        return {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 18,
                    "url": "http://localhost:8001/api/dcim/devices/18/",
                    "display": "TEST-1",
                    "name": "TEST-1",
                    "device_type": {
                        "id": 1,
                        "url": "http://localhost:8001/api/dcim/device-types/1/",
                        "display": "Generic 1RU Server",
                        "manufacturer": {
                            "id": 1,
                            "url": "http://localhost:8001/api/dcim/manufacturers/1/",
                            "display": "SuperMicro",
                            "name": "SuperMicro",
                            "slug": "supermicro"
                        },
                        "model": "Generic 1RU Server",
                        "slug": "generic-1ru-server"
                    },
                    "device_role": {
                        "id": 1,
                        "url": "http://localhost:8001/api/dcim/device-roles/1/",
                        "display": "Server",
                        "name": "Server",
                        "slug": "server"
                    },
                    "tenant": None,
                    "platform": None,
                    "serial": "",
                    "asset_tag": None,
                    "site": {
                        "id": 1,
                        "url": "http://localhost:8001/api/dcim/sites/1/",
                        "display": "Dev Lab",
                        "name": "Dev Lab",
                        "slug": "dev-lab"
                    },
                    "location": {
                        "id": 1,
                        "url": "http://localhost:8001/api/dcim/locations/1/",
                        "display": "dev lab",
                        "name": "dev lab",
                        "slug": "dev-lab",
                        "_depth": 0
                    },
                    "rack": None,
                    "position": None,
                    "face": None,
                    "parent_device": None,
                    "status": {
                        "value": "active",
                        "label": "Active"
                    },
                    "airflow": None,
                    "primary_ip": None,
                    "primary_ip4": None,
                    "primary_ip6": None,
                    "cluster": None,
                    "virtual_chassis": None,
                    "vc_position": None,
                    "vc_priority": None,
                    "description": "",
                    "comments": "",
                    "local_context_data": None,
                    "tags": [
                        {
                            "id": 1,
                            "url": "http://localhost:8001/api/extras/tags/1/",
                            "display": "dms",
                            "name": "dms",
                            "slug": "dms",
                            "color": "9e9e9e"
                        }
                    ],
                    "custom_fields": {
                        "BIOS": None,
                        "asn": None,
                        "dms": "1_abc",
                        "latest_executions": {
                            "network.ipmi_reset_credentials": "6426bb60e2846688bf37bee"
                        },
                        "latest_provisioning_end": "2023-01-03T16:36:49.924936",
                        "latest_provisioning_id": "633f4b3cf6c264e31c9c76e7",
                        "latest_provisioning_start": "2022-10-06T21:40:12+00:00",
                        "server_usage": {
                            "cpus": 1,
                            "osType": "CentOS",
                            "endDate": "2022-12-19T18:57:33",
                            "clientId": 987654321,
                            "cpuCores": 0,
                            "osVersion": "7 (latest)",
                            "serviceId": 11656,
                            "startDate": "2022-12-16T14:44:35",
                            "cancelReason": "Cancelled at customer request",
                            "graceEndDate": "2022-12-20T18:57:33"
                        },
                        "service_id": None
                    },
                    "config_context": {},
                    "created": "2023-06-21T10:48:57.162450Z",
                    "last_updated": "2023-09-06T10:01:30.615244Z"
                }
            ]
        }

    @staticmethod
    def get_interface_fixture(device_id=18, count_ipaddresses=1, id=94, untagged_vlan=None):
        return {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": id,
                    "url": "http://localhost:8001/api/dcim/interfaces/94/",
                    "display": "LAN0",
                    "device": {
                        "id": device_id,
                        "url": "http://localhost:8001/api/dcim/devices/18/",
                        "display": "TEST-0001",
                        "name": "TEST-0001"
                    },
                    "vdcs": [],
                    "module": None,
                    "name": "LAN0",
                    "label": "",
                    "type": {
                        "value": "1000base-t",
                        "label": "1000BASE-T (1GE)"
                    },
                    "enabled": True,
                    "parent": None,
                    "bridge": None,
                    "lag": None,
                    "mtu": None,
                    "mac_address": "0C:C4:7B:6C:C2:78",
                    "speed": 1000000,
                    "duplex": None,
                    "wwn": None,
                    "mgmt_only": False,
                    "description": "I350 Gigabit Network Connection",
                    "mode": None,
                    "rf_role": None,
                    "rf_channel": None,
                    "poe_mode": None,
                    "poe_type": None,
                    "rf_channel_frequency": None,
                    "rf_channel_width": None,
                    "tx_power": None,
                    "untagged_vlan": untagged_vlan,
                    "tagged_vlans": [],
                    "mark_connected": False,
                    "cable": {
                        "id": 18,
                        "url": "http://localhost:8001/api/dcim/cables/18/",
                        "display": "#18",
                        "label": ""
                    },
                    "cable_end": "A",
                    "wireless_link": None,
                    "link_peers": [
                        {
                            "id": 99,
                            "url": "http://localhost:8001/api/dcim/interfaces/99/",
                            "display": "swp4",
                            "device": {
                                "id": 4,
                                "url": "http://localhost:8001/api/dcim/devices/4/",
                                "display": "CNL20-THW-J10-LON1-UK",
                                "name": "CNL20-THW-J10-LON1-UK"
                            },
                            "name": "swp4",
                            "cable": 18,
                            "_occupied": True
                        }
                    ],
                    "link_peers_type": "dcim.interface",
                    "wireless_lans": [],
                    "vrf": None,
                    "l2vpn_termination": None,
                    "connected_endpoints": [
                        {
                            "id": 99,
                            "url": "http://localhost:8001/api/dcim/interfaces/99/",
                            "display": "swp4",
                            "device": {
                                "id": 4,
                                "url": "http://localhost:8001/api/dcim/devices/4/",
                                "display": "CNL20-THW-J10-LON1-UK",
                                "name": "CNL20-THW-J10-LON1-UK"
                            },
                            "name": "swp4",
                            "cable": 18,
                            "_occupied": True
                        }
                    ],
                    "connected_endpoints_type": "dcim.interface",
                    "connected_endpoints_reachable": True,
                    "tags": [
                        {
                            "id": 2,
                            "url": "http://localhost:8001/api/extras/tags/2/",
                            "display": "DCA",
                            "name": "DCA",
                            "slug": "dca",
                            "color": "9e9e9e"
                        },
                        {
                            "id": 1,
                            "url": "http://localhost:8001/api/extras/tags/1/",
                            "display": "dms",
                            "name": "dms",
                            "slug": "dms",
                            "color": "9e9e9e"
                        },
                        {
                            "id": 3,
                            "url": "http://localhost:8001/api/extras/tags/3/",
                            "display": "primary",
                            "name": "primary",
                            "slug": "primary",
                            "color": "9e9e9e"
                        },
                        {
                            "id": 4,
                            "url": "http://localhost:8001/api/extras/tags/4/",
                            "display": "public",
                            "name": "public",
                            "slug": "public",
                            "color": "9e9e9e"
                        }
                    ],
                    "custom_fields": {},
                    "created": "2023-08-31T12:17:34.654624Z",
                    "last_updated": "2023-08-31T12:39:39.392554Z",
                    "count_ipaddresses": count_ipaddresses,
                    "count_fhrp_groups": 0,
                    "_occupied": True
                }
            ]
        }

    @staticmethod
    def get_ip_address_fixture():
        return {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 268,
                    "url": "http://localhost:8001/api/ipam/ip-addresses/268/",
                    "display": "192.168.2.3/24",
                    "family": {
                        "value": 4,
                        "label": "IPv4"
                    },
                    "address": "192.168.2.3/24",
                    "vrf": {
                        "id": 3,
                        "url": "http://localhost:8001/api/ipam/vrfs/3/",
                        "display": "public (auto:auto)",
                        "name": "public",
                        "rd": "auto:auto"
                    },
                    "tenant": None,
                    "status": {
                        "value": "active",
                        "label": "Active"
                    },
                    "role": None,
                    "assigned_object_type": "dcim.interface",
                    "assigned_object_id": 94,
                    "assigned_object": {
                        "id": 94,
                        "url": "http://localhost:8001/api/dcim/interfaces/94/",
                        "display": "LAN0",
                        "device": {
                            "id": 18,
                            "url": "http://localhost:8001/api/dcim/devices/18/",
                            "display": "TEST-0001",
                            "name": "TEST-0001"
                        },
                        "name": "LAN0",
                        "cable": 18,
                        "_occupied": True
                    },
                    "nat_inside": None,
                    "nat_outside": [],
                    "dns_name": "",
                    "description": "",
                    "comments": "",
                    "tags": [
                        {
                            "id": 1,
                            "url": "http://localhost:8001/api/extras/tags/1/",
                            "display": "dms",
                            "name": "dms",
                            "slug": "dms",
                            "color": "9e9e9e"
                        },
                        {
                            "id": 3,
                            "url": "http://localhost:8001/api/extras/tags/3/",
                            "display": "primary",
                            "name": "primary",
                            "slug": "primary",
                            "color": "9e9e9e"
                        }
                    ],
                    "custom_fields": {},
                    "created": "2023-08-31T12:29:14.043545Z",
                    "last_updated": "2023-08-31T12:42:38.965541Z"
                }
            ]
        }

    @staticmethod
    def get_prefixes_fixture():
        return {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 4,
                    "url": "http://localhost:8001/api/ipam/prefixes/4/",
                    "display": "192.168.2.0/24",
                    "family": {
                        "value": 4,
                        "label": "IPv4"
                    },
                    "prefix": "192.168.2.0/24",
                    "site": {
                        "id": 1,
                        "url": "http://localhost:8001/api/dcim/sites/1/",
                        "display": "Dev Lab",
                        "name": "Dev Lab",
                        "slug": "dev-lab"
                    },
                    "vrf": {
                        "id": 3,
                        "url": "http://localhost:8001/api/ipam/vrfs/3/",
                        "display": "public (auto:auto)",
                        "name": "public",
                        "rd": "auto:auto"
                    },
                    "tenant": None,
                    "vlan": {
                        "id": 1,
                        "url": "http://localhost:8001/api/ipam/vlans/1/",
                        "display": "104003 (4003)",
                        "vid": 4003,
                        "name": "104003"
                    },
                    "status": {
                        "value": "active",
                        "label": "Active"
                    },
                    "role": {
                        "id": 2,
                        "url": "http://localhost:8001/api/ipam/roles/2/",
                        "display": "Public customer primary",
                        "name": "Public customer primary",
                        "slug": "public-customer-primary"
                    },
                    "is_pool": False,
                    "mark_utilized": False,
                    "description": "",
                    "comments": "",
                    "tags": [],
                    "custom_fields": {},
                    "created": "2023-01-27T10:25:30.673896Z",
                    "last_updated": "2023-01-27T10:25:30.674016Z",
                    "children": 0,
                    "_depth": 0
                },
                {
                    "id": 1,
                    "url": "http://localhost:8001/api/ipam/prefixes/1/",
                    "display": "212.78.92.0/24",
                    "family": {
                        "value": 4,
                        "label": "IPv4"
                    },
                    "prefix": "212.78.92.0/24",
                    "site": None,
                    "vrf": {
                        "id": 3,
                        "url": "http://localhost:8001/api/ipam/vrfs/3/",
                        "display": "public (auto:auto)",
                        "name": "public",
                        "rd": "auto:auto"
                    },
                    "tenant": None,
                    "vlan": {
                        "id": 1,
                        "url": "http://localhost:8001/api/ipam/vlans/1/",
                        "display": "104003 (4003)",
                        "vid": 4003,
                        "name": "104003"
                    },
                    "status": {
                        "value": "active",
                        "label": "Active"
                    },
                    "role": {
                        "id": 2,
                        "url": "http://localhost:8001/api/ipam/roles/2/",
                        "display": "Public customer primary",
                        "name": "Public customer primary",
                        "slug": "public-customer-primary"
                    },
                    "is_pool": False,
                    "mark_utilized": False,
                    "description": "LON2 network (infrastructure)",
                    "comments": "",
                    "tags": [],
                    "custom_fields": {},
                    "created": "2022-09-30T12:27:29.959469Z",
                    "last_updated": "2022-10-13T10:49:59.053043Z",
                    "children": 0,
                    "_depth": 0
                }
            ]
        }

    @staticmethod
    def get_tags_fixture(name='primary'):
        return {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 3,
                    "url": "http://localhost:8001/api/extras/tags/3/",
                    "display": name,
                    "name": name,
                    "slug": name,
                    "color": "9e9e9e",
                    "description": "",
                    "tagged_items": 41,
                    "created": "2022-09-30T12:19:58.733081Z",
                    "last_updated": "2022-09-30T12:19:58.733092Z"
                }
            ]
        }

    @staticmethod
    def post_create_ip():
        return {
            "address": "192.168.2.4/24",
            "assigned_object": {
            "_occupied": True,
            "cable": 22,
            "device": {
                "display": "TEST-1",
                "id": 23,
                "name": "TEST-1",
                "url": "http://localhost:8001/api/dcim/devices/23/"
            },
            "display": "enp9s0f0",
            "id": 32,
            "name": "enp9s0f0",
            "url": "http://localhost:8001/api/dcim/interfaces/32/"
            },
            "assigned_object_id": 32,
            "assigned_object_type": "dcim.interface",
            "comments": "",
            "created": "2024-02-26T15:08:49.924652Z",
            "custom_fields": {},
            "description": "",
            "display": "192.168.2.4/24",
            "dns_name": "",
            "family": {
            "label": "IPv4",
            "value": 4
            },
            "id": 278,
            "last_updated": "2024-02-26T15:08:49.924780Z",
            "nat_inside": None,
            "nat_outside": [],
            "role": None,
            "status": {
            "label": "Active",
            "value": "active"
            },
            "tags": [
            {
                "color": "9e9e9e",
                "display": "dms",
                "id": 1,
                "name": "dms",
                "slug": "dms",
                "url": "http://localhost:8001/api/extras/tags/1/"
            },
            {
                "color": "9e9e9e",
                "display": "primary",
                "id": 3,
                "name": "primary",
                "slug": "primary",
                "url": "http://localhost:8001/api/extras/tags/3/"
            }
            ],
            "tenant": None,
            "url": "http://localhost:8001/api/ipam/ip-addresses/278/",
            "vrf": {
            "display": "public (auto:auto)",
            "id": 3,
            "name": "public",
            "rd": "auto:auto",
            "url": "http://localhost:8001/api/ipam/vrfs/3/"
            }
        }
