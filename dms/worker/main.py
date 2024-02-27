import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

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


async def main():
    client = await Client.connect(
        "localhost:7233"
    )

    worker = Worker(
        client,
        task_queue="dms-task-queue",
        workflows=[EnsureServerHasIP],
        activities=[
            find_server_activity,
            find_primary_interface_activity,
            find_ip_for_interface_activity,
            find_vlan_activity,
            get_prefixes_activity,
            get_primary_tag_activity,
            find_dms_tag_activity,
            create_available_ips_activity,
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
