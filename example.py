# Example use case
from xonstatus import *

# Server IP addresses, 300 server, regulars, Feris, localhost
servers = ['45.33.24.39', '168.119.137.110', '157.90.112.225', '127.0.0.1']


for ip in servers:
    client = XonClient(ip=ip)
    status = client.getStatus()

    if not client.error:
        print(status)
    else:
        print(f"Error: {status}")

