import os

from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage
from azure.core.exceptions import ResourceExistsError

def auth_queue_client(queue_name: str) -> QueueClient:
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    queue_client = QueueClient.from_connection_string(conn_str=connect_str, queue_name=queue_name)
    try:
        queue_client.create_queue()
    except ResourceExistsError:
        pass

    return queue_client


# Azure location
queue_name = 'intern-queue-quickstart'

# Azure clients
queue_client = auth_queue_client(queue_name)

queue_client.send_message("This is a message sent from local python env")

for message in queue_client.peek_messages(max_messages=5):
    # Display the message
    print("Message: " + message.content)

