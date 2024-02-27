import uuid
import pytest

from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from temporalio import activity

from tests.mocks.netbox import NetboxMocks
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
from workflows.ensure_server_has_ip_workflow import EnsureServerHasIP


@activity.defn(name='find_server_activity')
async def find_server_activity_exists_mocked(name: str):
    return NetboxMocks.get_server_fixture()['results'][0]

@activity.defn(name='find_server_activity')
async def find_server_activity_does_not_exists_mocked(name: str):
    return None

@activity.defn(name='find_primary_interface_activity')
async def find_primary_interface_exists_mocked(device_id: str):
    return NetboxMocks.get_interface_fixture()['results'][0]

@activity.defn(name='find_primary_interface_activity')
async def find_primary_interface_exists_no_ip_mocked(device_id: str):
    return NetboxMocks.get_interface_fixture(count_ipaddresses=0)['results'][0]

@activity.defn(name='find_primary_interface_activity')
async def find_primary_interface_does_not_exists_mocked(device_id: str):
    return None

@activity.defn(name='find_ip_for_interface_activity')
async def find_ip_for_interface_exists_mocked(interface_id: str):
    return NetboxMocks.get_ip_address_fixture()['results'][0]

@activity.defn(name='find_ip_for_interface_activity')
async def find_ip_for_interface_does_not_exists_mocked(interface_id: str):
    return None

@activity.defn(name='find_vlan_activity')
async def find_vlan_exists_mocked(id: str):
    return NetboxMocks.get_interface_fixture(
        id=99,
        untagged_vlan={
            "id": 1,
            "url": "http://localhost:8001/api/ipam/vlans/1/",
            "display": "104003 (4003)",
            "vid": 4003,
            "name": "104003"
        }
    )['results'][0]

@activity.defn(name='get_prefixes_activity')
async def find_prefixes_exists_mocked(vlan_id: str):
    return NetboxMocks.get_prefixes_fixture()['results'][0]

@activity.defn(name='get_prefixes_activity')
async def find_prefixes_does_not_exists_mocked(vlan_id: str):
    return None

@activity.defn(name='get_primary_tag_activity')
async def find_primary_tag_exists_mocked():
    return NetboxMocks.get_tags_fixture(name='primary')['results'][0]

@activity.defn(name='get_primary_tag_activity')
async def find_primary_tag_does_not_exists_mocked():
    return None

@activity.defn(name='find_dms_tag_activity')
async def find_dms_tag_exists_mocked():
    return NetboxMocks.get_tags_fixture(name='dms')['results'][0]

@activity.defn(name='find_dms_tag_activity')
async def find_dms_tag_does_not_exists_mocked():
    return None

@activity.defn(name='create_available_ips_activity')
async def post_create_ip_success_mocked(prefix_id, tag_ids, interface_id):
    return NetboxMocks.post_create_ip()


class TestEnsureServerHasIPWorkflow:
    task_queue_name = str(uuid.uuid4())

    def worker(self, env, activities: list):
        return Worker(
            env.client,
            task_queue=self.task_queue_name,
            workflows=[EnsureServerHasIP],
            activities=activities,
        )

    @pytest.mark.asyncio
    async def test_server_has_ip(self):
        expected_output = {
            "ip_address": "192.168.2.3",
            "message": None,
            "server_id": "18",
            "server_status": "active",
            "success": True,
        }

        # There are two ways to mock Activities, by mocking the request's reponses, or mocking the return statement of
        # Activity as done above
        # requests_mock.get('http://localhost:8001/api/dcim/devices/?name=TEST-1', json=NetboxMocks.get_server_fixture())
        # requests_mock.get(
        #     'http://localhost:8001/api/dcim/interfaces/?device_id=18&tag=primary',
        #     json=NetboxMocks.get_interface_fixture(),
        # )
        # requests_mock.get(
        #     'http://localhost:8001/api/ipam/ip-addresses/?interface_id=94&tag=primary',
        #     json=NetboxMocks.get_ip_address_fixture(),
        # )

        mocked_activities = [
            find_server_activity_exists_mocked,
            find_primary_interface_exists_mocked,
            find_ip_for_interface_exists_mocked,
        ]

        async with await WorkflowEnvironment.start_time_skipping() as env:
            async with self.worker(env, mocked_activities):
                assert expected_output == await env.client.execute_workflow(
                    EnsureServerHasIP.run,
                    "TEST-1",
                    id=str(uuid.uuid4()),
                    task_queue=self.task_queue_name,
                )

    @pytest.mark.asyncio
    async def test_server_not_found(self):
        expected_output = {
            "ip_address": None,
            "message": 'Server not found',
            "server_id": None,
            "server_status": None,
            "success": False,
        }

        mocked_activities = [
            find_server_activity_does_not_exists_mocked,
        ]

        async with await WorkflowEnvironment.start_time_skipping() as env:
            async with self.worker(env, mocked_activities):
                assert expected_output == await env.client.execute_workflow(
                    EnsureServerHasIP.run,
                    "TEST-1",
                    id=str(uuid.uuid4()),
                    task_queue=self.task_queue_name,
                )

    @pytest.mark.asyncio
    async def test_primary_interface_not_found(self):
        expected_output = {
            "ip_address": None,
            "message": 'No primary interface found',
            "server_id": '18',
            "server_status": 'active',
            "success": False,
        }

        mocked_activities = [
            find_server_activity_exists_mocked,
            find_primary_interface_does_not_exists_mocked,
        ]

        async with await WorkflowEnvironment.start_time_skipping() as env:
            async with self.worker(env, mocked_activities):
                assert expected_output == await env.client.execute_workflow(
                    EnsureServerHasIP.run,
                    "TEST-1",
                    id=str(uuid.uuid4()),
                    task_queue=self.task_queue_name,
                )

    @pytest.mark.asyncio
    async def test_ip_on_interface_not_primary(self):
        expected_output = {
            "ip_address": None,
            "message": 'IP on interface is not primary IP',
            "server_id": '18',
            "server_status": 'active',
            "success": False,
        }

        mocked_activities = [
            find_server_activity_exists_mocked,
            find_primary_interface_exists_mocked,
            find_ip_for_interface_does_not_exists_mocked,
        ]

        async with await WorkflowEnvironment.start_time_skipping() as env:
            async with self.worker(env, mocked_activities):
                assert expected_output == await env.client.execute_workflow(
                    EnsureServerHasIP.run,
                    "TEST-1",
                    id=str(uuid.uuid4()),
                    task_queue=self.task_queue_name,
                )

    @pytest.mark.asyncio
    async def test_no_prefixes_found(self):
        expected_output = {
            "ip_address": None,
            "message": 'No prefixes found',
            "server_id": '18',
            "server_status": 'active',
            "success": False,
        }

        mocked_activities = [
            find_server_activity_exists_mocked,
            find_primary_interface_exists_no_ip_mocked,
            find_vlan_exists_mocked,
            find_prefixes_does_not_exists_mocked,
        ]

        async with await WorkflowEnvironment.start_time_skipping() as env:
            async with self.worker(env, mocked_activities):
                assert expected_output == await env.client.execute_workflow(
                    EnsureServerHasIP.run,
                    "TEST-1",
                    id=str(uuid.uuid4()),
                    task_queue=self.task_queue_name,
                )

    @pytest.mark.asyncio
    async def test_no_primary_tag_found(self):
        expected_output = {
            "ip_address": None,
            "message": "'primary' tag not found",
            "server_id": '18',
            "server_status": 'active',
            "success": False,
        }

        mocked_activities = [
            find_server_activity_exists_mocked,
            find_primary_interface_exists_no_ip_mocked,
            find_vlan_exists_mocked,
            find_prefixes_exists_mocked,
            find_primary_tag_does_not_exists_mocked,
        ]

        async with await WorkflowEnvironment.start_time_skipping() as env:
            async with self.worker(env, mocked_activities):
                assert expected_output == await env.client.execute_workflow(
                    EnsureServerHasIP.run,
                    "TEST-1",
                    id=str(uuid.uuid4()),
                    task_queue=self.task_queue_name,
                )

    @pytest.mark.asyncio
    async def test_no_dms_tag_found(self):
        expected_output = {
            "ip_address": None,
            "message": "'dms' tag not found",
            "server_id": '18',
            "server_status": 'active',
            "success": False,
        }

        mocked_activities = [
            find_server_activity_exists_mocked,
            find_primary_interface_exists_no_ip_mocked,
            find_vlan_exists_mocked,
            find_prefixes_exists_mocked,
            find_primary_tag_exists_mocked,
            find_dms_tag_does_not_exists_mocked,
        ]

        async with await WorkflowEnvironment.start_time_skipping() as env:
            async with self.worker(env, mocked_activities):
                assert expected_output == await env.client.execute_workflow(
                    EnsureServerHasIP.run,
                    "TEST-1",
                    id=str(uuid.uuid4()),
                    task_queue=self.task_queue_name,
                )

    @pytest.mark.asyncio
    async def test_create_available_ip(self):
        expected_output = {
            "ip_address": '192.168.2.4',
            "message": None,
            "server_id": '18',
            "server_status": 'active',
            "success": True,
        }

        mocked_activities = [
            find_server_activity_exists_mocked,
            find_primary_interface_exists_no_ip_mocked,
            find_vlan_exists_mocked,
            find_prefixes_exists_mocked,
            find_primary_tag_exists_mocked,
            find_dms_tag_exists_mocked,
            post_create_ip_success_mocked,
        ]

        async with await WorkflowEnvironment.start_time_skipping() as env:
            async with self.worker(env, mocked_activities):
                assert expected_output == await env.client.execute_workflow(
                    EnsureServerHasIP.run,
                    "TEST-1",
                    id=str(uuid.uuid4()),
                    task_queue=self.task_queue_name,
                )




