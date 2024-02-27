from .netbox import NetboxHttp
from temporalio import activity
from requests.exceptions import HTTPError


NETBOX_TOKEN = '0123456789abcdef0123456789abcdef01234567'


@activity.defn
async def find_server_activity(name: str):
    netbox = NetboxHttp('localhost:8001', NETBOX_TOKEN)
    
    result = netbox.run('get', 'dcim/devices', name=name)
    
    if result['count'] > 0:
        return result['results'][0]
    return None

@activity.defn
async def find_primary_interface_activity(device_id: str):
    netbox = NetboxHttp('localhost:8001', NETBOX_TOKEN)
    
    result = netbox.run('get', 'dcim/interfaces', device_id=device_id, tag='primary')
    
    if result['count'] > 0:
        return result['results'][0]
    return None

@activity.defn
async def find_ip_for_interface_activity(interface_id: str):
    netbox = NetboxHttp('localhost:8001', NETBOX_TOKEN)
    
    result = netbox.run('get', 'ipam/ip-addresses', interface_id=interface_id, tag='primary')
    
    if result['count'] > 0:
        return result['results'][0]
    return None

@activity.defn
async def find_vlan_activity(id: str):
    netbox = NetboxHttp('localhost:8001', NETBOX_TOKEN)
    
    result = netbox.run('get', 'dcim/interfaces', id=id)
    
    if result['count'] > 0:
        return result['results'][0]
    return None

@activity.defn
async def get_prefixes_activity(vlan_id: str):
    netbox = NetboxHttp('localhost:8001', NETBOX_TOKEN)
    
    result = netbox.run(
        'get',
        'ipam/prefixes',
        vlan_id=vlan_id,
        children='0',
        family='4',
        role='public-customer-primary',
        status='active',
    )
    
    if result['count'] > 0:
        return result['results'][0]
    return None

@activity.defn
async def get_primary_tag_activity():
    netbox = NetboxHttp('localhost:8001', NETBOX_TOKEN)
    
    result = netbox.run('get', 'extras/tags', name='primary')
    
    if result['count'] > 0:
        return result['results'][0]
    return None

@activity.defn
async def find_dms_tag_activity():
    netbox = NetboxHttp('localhost:8001', NETBOX_TOKEN)
    
    result = netbox.run('get', 'extras/tags', name='dms')
    
    if result['count'] > 0:
        return result['results'][0]
    return None

@activity.defn
async def create_available_ips_activity(
    prefix_id: str,
    tag_ids: list,
    interface_id: str,
):
    netbox = NetboxHttp('localhost:8001', NETBOX_TOKEN)
    
    result = netbox.run(
        'post',
        f'ipam/prefixes/{prefix_id}/available-ips',
        tags=tag_ids,
        assigned_object_id=interface_id,
        assigned_object_type='dcim.interface'
    )
    
    if result:
        return result
    return None
