#!/usr/bin/python

import httpx
import asyncio
import time

async def get_async(url):
    async with httpx.AsyncClient() as client:
        return await client.get(url)

urls = ['https://aca-app-httpscalerule.jollyrock-37fb5a03.westeurope.azurecontainerapps.io'
        'https://aca-app-httpscalerule.jollyrock-37fb5a03.westeurope.azurecontainerapps.io',
        'https://aca-app-httpscalerule.jollyrock-37fb5a03.westeurope.azurecontainerapps.io',
        'https://aca-app-httpscalerule.jollyrock-37fb5a03.westeurope.azurecontainerapps.io']

async def launch():

    resps = await asyncio.gather(*map(get_async, urls))
    data = [resp.status_code for resp in resps]

    for status_code in data:
        print(status_code)

tm1 = time.perf_counter()

asyncio.run(launch())

tm2 = time.perf_counter()
print(f'Total time elapsed: {tm2-tm1:0.2f} seconds')