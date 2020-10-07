#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
from urllib.parse import urlparse


class HTTPServer:
    """
    HTTPServer class used to represent all the server side operations
    Methods
    -------
    __init__(self, url)
        It is contructor for HTTPServer class.
    buildRequestheaders(self)
        It is used to generate headers.
    buildGETrequest(self)
        It is used to build a GET method request.
    buildPOSTrequest(self)
        It is used to build a POST method request.
    sendresponse(self)
        It is used to send the response back to client.
    """

    def __init__(self, url):
        """It is contructor for HTTPServer class.

        Parameters
        -------
        url
            a string containing URL
        """
        self.url = urlparse(url)
        self.host = self.url.netloc
        self.header = {"Host": self.host}
        self.data = ""
        self.body = ""
        self.file = ""
        self.content = ""
        self.proto = " HTTP/1.0"
        self.query = self.url.query if self.url.query else ""

    def buildRequestheaders(self):
        """It is used to generate headers.

        Returns
        -------
        str
            a string containing header information
        """
        header = "\r\n"
        for key, value in self.header.items():
            header += (key + ": " + value + "\r\n")
        return header

    def buildGETrequest(self):
        """It is used to build a GET method request.

        Returns
        -------
        str
            a string containing GET request
        """
        request = self.method.upper() + " " + self.url.path + "?" + self.query + \
            self.proto + self.buildRequestheaders() + "\r\n"
        self.content = request

    def buildPOSTrequest(self):
        """It is used to build a POST method request.

        Returns
        -------
        str
            a string containing POST request
        """
        request = ""
        if self.data:
            request = self.method.upper() + " " + self.url.path + self.proto + \
                self.buildRequestheaders() + "\r\n" + self.data
        elif self.file:
            request = self.method.upper() + " " + self.url.path + self.proto + \
                self.buildRequestheaders() + "\r\n" + self.file
        else:
            request = self.method.upper() + " " + self.url.path + self.proto + \
                self.buildRequestheaders() + "\r\n"
        self.content = request

    def sendresponse(self):
        """It is used to send the response back to client.

        Returns
        -------
        HTTPServer
            a HTTPServer class object to client
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host, 80))
            s.sendall(self.content.encode("utf-8"))
            response = s.recv(2048, socket.MSG_WAITALL)
            self.body = response.decode("utf-8")
            return self
        except Exception as e:
            pass
        finally:
            try:
                s.shutdown(socket.SHUT_RDWR)
            except Exception as e:
                pass
            try:
                s.close()
            except Exception as e:
                pass
