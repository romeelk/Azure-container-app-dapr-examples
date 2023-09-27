import asyncio
import sys
import os
from azure.storage.queue import  QueueClient

async def main():
   
    try:
        print("Azure Python storage queue reader")
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if(connect_str == None):
          print("No storage connection string env var defined. Exiting")
          sys.exit(-1)
    
        # demo purposes use DefaultAzureCredential for all dev and prod code
        queue_client = QueueClient.from_connection_string(connect_str, "daprqueue")

        queue_props = queue_client.get_queue_properties()
        print(queue_props.approximate_message_count)
        response = queue_client.receive_messages(max_messages=5)
        
        messages = queue_client.receive_messages()
        for message in messages:
            print('Message for dequeueing is: ', message.content)
            # Then delete it.
            # When queue is deleted all messages are deleted, here is done for demo purposes 
            # Deleting requires the message id and pop receipt (returned by get_messages)
            queue_client.delete_message(message=message.id, pop_receipt=message.pop_receipt)
            print('Successfully dequeued message')


    except Exception as ex:
        print('Exception:')
        print(ex)

asyncio.run(main())