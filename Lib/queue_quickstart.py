from storage_utils import StorageUtil

if __name__ == '__main__':
    # Azure location
    queue_name = 'intern-queue-quickstart'

    # Azure clients
    storage_util = StorageUtil()
    queue_client = storage_util.get_and_make_auth_queue_client(queue_name)

    queue_client.send_message("This is a message sent from local python env")
    print(f"Added a message to the queue '{queue_name}'\n")

    num_msgs = 20
    print(f"Top {num_msgs} messages in queue:")
    for message in queue_client.peek_messages(max_messages=num_msgs):
        # Display the message
        print("\tMessage: " + message.content)

