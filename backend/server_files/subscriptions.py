import asyncio
from ariadne import SubscriptionType
from store import queues

subscription = SubscriptionType()


@subscription.source("clusterProgress")
async def cluster_progress_source(obj, info):
    """
    A generator for returning status updates to the client
    :param obj: unused parameter
    :param info: unused parameter
    """
    queue = asyncio.Queue()
    queues.append(queue)
    try:
        while True:
            status = await queue.get()
            queue.task_done()
            yield status
    except asyncio.CancelledError:
        queues.remove(queue)
        raise


@subscription.field("clusterProgress")
async def messages_resolver(status, info):
    """
    Sends the status message to the client via websockets
    :param status: the status message
    :param info: unused parameter
    :return: the status message sent to the client
    """
    return status
