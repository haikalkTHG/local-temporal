from temporalio import workflow
from datetime import timedelta
with workflow.unsafe.imports_passed_through():
    from activities.activities import (
        find_server_activity,
        find_primary_interface_activity,
        find_ip_for_interface_activity,
        find_vlan_activity,
        get_prefixes_activity,
        get_primary_tag_activity,
        find_dms_tag_activity,
        create_available_ips_activity,
    )


@workflow.defn
class EnsureServerHasIP:
    @workflow.run
    async def run(self, server_name: str) -> dict:
        output = {
            'server_id': None,
            'ip_address': None,
            'server_status': None,
            'message': None,
            'success': False,
        }

        find_server_result = await workflow.execute_activity(
            find_server_activity,
            server_name,
            schedule_to_close_timeout=timedelta(seconds=60),
        )
        if not find_server_result:
            output['message'] = 'Server not found'
            return output
        output['server_id'] = str(find_server_result['id'])
        output['server_status'] = find_server_result['status']['value']

        find_primary_interface_result = await workflow.execute_activity(
            find_primary_interface_activity,
            output['server_id'],
            schedule_to_close_timeout=timedelta(seconds=60),
        )
        if not find_primary_interface_result:
            output['message'] = 'No primary interface found'
            return output
        elif find_primary_interface_result['count_ipaddresses'] > 0:
            find_ip_for_interface_result = await workflow.execute_activity(
                find_ip_for_interface_activity,
                str(find_primary_interface_result['id']),
                schedule_to_close_timeout=timedelta(seconds=60),
            )

            if find_ip_for_interface_result and len(find_ip_for_interface_result) > 0:
                output['ip_address'] = find_ip_for_interface_result['address'].split('/')[0]
                output['success'] = True
                return output
            
            output['message'] = 'IP on interface is not primary IP'
            return output

        find_vlan_result = await workflow.execute_activity(
            find_vlan_activity,
            str(find_primary_interface_result['connected_endpoints'][0]['id']),
            schedule_to_close_timeout=timedelta(seconds=60),
        )
            
        get_prefixes_result = await workflow.execute_activity(
            get_prefixes_activity,
            str(find_vlan_result['untagged_vlan']['id']),
            schedule_to_close_timeout=timedelta(seconds=60),
        )
        if not get_prefixes_result:
            output['message'] = 'No prefixes found'
            return output
        
        get_primary_tag_result = await workflow.execute_activity(
            get_primary_tag_activity,
            schedule_to_close_timeout=timedelta(seconds=60),
        )
        if not get_primary_tag_result:
            output['message'] = "'primary' tag not found"
            return output

        find_dms_tag_result = await workflow.execute_activity(
            find_dms_tag_activity,
            schedule_to_close_timeout=timedelta(seconds=60),
        )
        if not find_dms_tag_result:
            output['message'] = "'dms' tag not found"
            return output

        create_available_ips_result = await workflow.execute_activity(
            create_available_ips_activity,
            args=[
                str(get_prefixes_result['id']),
                [get_primary_tag_result['id'], find_dms_tag_result['id']],
                str(find_primary_interface_result['id'])
            ],
            schedule_to_close_timeout=timedelta(seconds=300),
        )
        output['success'] = True
        output['ip_address'] = create_available_ips_result['address'].split('/')[0]
        return output
