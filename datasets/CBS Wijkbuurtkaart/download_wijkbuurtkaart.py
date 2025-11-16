"""Download CBS "WijkBuurtkaart" file from CBS site"""

import os
import urllib.request
import requests
import httpx
import time

filename = 'WijkBuurtkaart_2024_v1.zip'

base_url = 'https://geodata.cbs.nl/files/Wijkenbuurtkaart'
url = '/'.join([base_url, filename])

current_directory = os.path.dirname(__file__)
destination = os.path.join(current_directory, filename)

print('Downloading ...', url)

t0 = time.time()

# urllib
r = urllib.request.urlopen(url)
data = r.read()
with open(destination, 'wb') as f:
    f.write(data)

# # using requests
# r = requests.get(url)
# with open(destination, mode="wb") as file:
#     file.write(r.content)

# # using requests with streaming
# r = requests.get(url, stream=True)
# with open(destination, mode="wb") as file:
#     for chunk in r.iter_content(chunk_size=10 * 1024):
#         file.write(chunk)

# # using httpx
# r = httpx.get(url)
# with open(destination, mode="wb") as file:
#     file.write(r.content)

t1 = time.time()

print(f'Done. File saved as {destination}')
print(f'Duration: {t1 - t0:.1f} seconds')
