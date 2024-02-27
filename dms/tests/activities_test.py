import pytest
from temporalio.testing import ActivityEnvironment

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


class TestClass:
    activity_environment = ActivityEnvironment()


class TestFindServerActivity(TestClass):
    @pytest.mark.asyncio
    async def test_server_exists(self, requests_mock):
        requests_mock.get('http://localhost:8001/api/dcim/devices/?name=TEST-1', json=NetboxMocks.get_server_fixture())
        assert NetboxMocks.get_server_fixture()['results'][0] == await self.activity_environment.run(
            find_server_activity,
            'TEST-1',
        )

    @pytest.mark.asyncio
    async def test_server_does_not_exists(self, requests_mock):
        requests_mock.get('http://localhost:8001/api/dcim/devices/?name=TEST-1', json=NetboxMocks.get_empty_response())
        assert None == await self.activity_environment.run(
            find_server_activity,
            'TEST-1',
        )


class TestFindPrimaryInterfaceActivity(TestClass):
    @pytest.mark.asyncio
    async def test_primary_interface_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/dcim/interfaces/?device_id=18&tag=primary',
            json=NetboxMocks.get_interface_fixture(),
        )
        assert NetboxMocks.get_interface_fixture()['results'][0] == await self.activity_environment.run(
            find_primary_interface_activity,
            '18',
        )

    @pytest.mark.asyncio
    async def test_primary_interface_does_not_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/dcim/interfaces/?device_id=18&tag=primary',
            json=NetboxMocks.get_empty_response(),
        )
        assert None == await self.activity_environment.run(
            find_primary_interface_activity,
            '18',
        )


class TestFindIpForInterfaceActivity(TestClass):
    @pytest.mark.asyncio
    async def test_ip_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/ipam/ip-addresses/?interface_id=94&tag=primary',
            json=NetboxMocks.get_ip_address_fixture(),
        )
        assert NetboxMocks.get_ip_address_fixture()['results'][0] == await self.activity_environment.run(
            find_ip_for_interface_activity,
            '94',
        )

    @pytest.mark.asyncio
    async def test_ip_does_not_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/ipam/ip-addresses/?interface_id=94&tag=primary',
            json=NetboxMocks.get_empty_response(),
        )
        assert None == await self.activity_environment.run(
            find_ip_for_interface_activity,
            '94',
        )


class TestFindVlanActivity(TestClass):
    @pytest.mark.asyncio
    async def test_vlan_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/dcim/interfaces/?id=94',
            json=NetboxMocks.get_interface_fixture(),
        )
        assert NetboxMocks.get_interface_fixture()['results'][0] == await self.activity_environment.run(
            find_vlan_activity,
            '94',
        )

    @pytest.mark.asyncio
    async def test_vlan_does_not_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/dcim/interfaces/?id=94',
            json=NetboxMocks.get_empty_response(),
        )
        assert None == await self.activity_environment.run(
            find_vlan_activity,
            '94',
        )


class TestGetPrefixesActivity(TestClass):
    @pytest.mark.asyncio
    async def test_prefixes_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/ipam/prefixes/?vlan_id=1&children=0&family=4&role=public-customer-primary&status=active',
            json=NetboxMocks.get_prefixes_fixture(),
        )
        assert NetboxMocks.get_prefixes_fixture()['results'][0] == await self.activity_environment.run(
            get_prefixes_activity,
            '1',
        )

    @pytest.mark.asyncio
    async def test_prefixes_does_not_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/ipam/prefixes/?vlan_id=1&children=0&family=4&role=public-customer-primary&status=active',
            json=NetboxMocks.get_empty_response(),
        )
        assert None == await self.activity_environment.run(
            get_prefixes_activity,
            '1',
        )


class TestGetPrimaryTagActivity(TestClass):
    @pytest.mark.asyncio
    async def test_tag_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/extras/tags/?name=primary',
            json=NetboxMocks.get_tags_fixture(),
        )
        assert NetboxMocks.get_tags_fixture()['results'][0] == await self.activity_environment.run(
            get_primary_tag_activity,
        )

    @pytest.mark.asyncio
    async def test_tag_does_not_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/extras/tags/?name=primary',
            json=NetboxMocks.get_empty_response(),
        )
        assert None == await self.activity_environment.run(
            get_primary_tag_activity,
        )


class TestFindDmsTagActivity(TestClass):
    @pytest.mark.asyncio
    async def test_tag_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/extras/tags/?name=dms',
            json=NetboxMocks.get_tags_fixture(name='dms'),
        )
        assert NetboxMocks.get_tags_fixture(name='dms')['results'][0] == await self.activity_environment.run(
            find_dms_tag_activity,
        )

    @pytest.mark.asyncio
    async def test_tag_does_not_exists(self, requests_mock):
        requests_mock.get(
            'http://localhost:8001/api/extras/tags/?name=dms',
            json=NetboxMocks.get_empty_response(),
        )
        assert None == await self.activity_environment.run(
            find_dms_tag_activity,
        )


class TestCreateAvailableIpsActivity(TestClass):
    @pytest.mark.asyncio
    async def test_create_ip_success(self, requests_mock):
        requests_mock.post(
            'http://localhost:8001/api/ipam/prefixes/1/available-ips/',
            json=NetboxMocks.post_create_ip(),
        )
        assert NetboxMocks.post_create_ip() == await self.activity_environment.run(
            create_available_ips_activity,
            '1', ['1', '1'], '1',
        )

    @pytest.mark.asyncio
    async def test_create_ip_fail(self, requests_mock):
        requests_mock.post(
            'http://localhost:8001/api/ipam/prefixes/1/available-ips/',
            json=NetboxMocks.get_empty_response(),
        )
        assert NetboxMocks.get_empty_response() == await self.activity_environment.run(
            create_available_ips_activity,
            '1', ['1', '1'], '1',
        )
