from storage_utils import StorageUtil

if __name__ == '__main__':
    # Azure location
    queue_name = 'intern-queue-quickstart'

    # Azure clients
    queue_client = StorageUtil.get_and_make_auth_queue_client(queue_name)

    queue_client.send_message("This is a message sent from local python env")

    for message in queue_client.peek_messages(max_messages=5):
        # Display the message
        print("Message: " + message.content)

