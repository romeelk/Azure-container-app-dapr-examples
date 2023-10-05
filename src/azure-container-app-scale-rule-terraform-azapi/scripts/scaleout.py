from time import sleep
import requests
import concurrent.futures
from threading import current_thread


URL='https://aca-app-httpscalerule.jollyrock-37fb5a03.westeurope.azurecontainerapps.io'
input_message = "Please enter the max concurrent requests for the Azure container app:( > 0 and <= 20):"
no_of_requests = int(input(input_message))

while no_of_requests < 0 or no_of_requests > 20:
    no_of_requests = int(input(input_message))
    

def request_url(id):
    response = requests.get(URL)
    sleep(0.5)
    print(f'Request no:{id} fetching url {URL}')
    return response.status_code

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(request_url, id) for id in range(0,no_of_requests)]
    results = [future.result() for future in concurrent.futures.as_completed(futures)]
for result in results:
    print(f'Status code:{result}')