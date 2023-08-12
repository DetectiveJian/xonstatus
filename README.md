# xonstatus
xonstatus is a program to query xonotic game servers for their status. The response contains:
 - Hostname
 - Map name
 - Max no. of clients
 - No. of clients
 - No. of bots
 - Current gamemode
 - Player info
    - Player ping
    - Player score
    - Player team
    - Player nick
 - Other server info

# Uasge
Here is a simple client:
```python
from xonstatus import *

client = XonClient(ip="SERVER IP")  # replace SERVER IP with the real server ip
status = client.getStatus()
print(status)

```
Also see [example](example.py).
