"""
MIT License

Copyright (c) 2023 tofh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#---------------------------------------------------

# Author: tofh
# Last Updated: 12-08-2023
# Xonotic server status utility

#---------------------------------------------------

import socket
import parser

class XonClient:
    """
    Xonotic status client, for querying xonotic server status information
        XonClient(ip, port, timeout)

        ip = target server's IP address
        port = target server's port
        timeout = time to wait for response

    Example:
            client = XonClient(ip='45.33.24.39')  # 300's xonotic server, using default port and timeout
            print(client.getStatus())  # response dict
    """
    # Supported requests
    STATUS = b"\xff\xff\xff\xffgetstatus"  # server status request

    def __init__(self, ip='localhost', port=26000, timeout=5):
        self.ip = ip            # server ip to send query to
        self.port = port        # quried server's port
        self.timeout = timeout  # request timeout limit, time to wait for response
        self.filter_colors = True # filters xon color code from the nicks
        self.error = False      # whether a query resulted in some sort of error

    def query(self, query_type):
        """
        Handles requests and response
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # using ipv4 and UDP
        client.settimeout(self.timeout)  # set timeout
        try:
            client.sendto(query_type, (self.ip, self.port))  # sending query to the server
            return client.recvfrom(4096)  # waiting for server to respond back
        except Exception as e:
            return ('error', e)

    def getStatus(self):
        """
        Get server Info status, dict output
        """
        response, query_info = self.query(self.STATUS)
        if response == 'error':
            self.error = True
            return query_info
        else:
            status = parser.Parser(response)
            status.remove_colors = self.filter_colors
            return status.parse()

