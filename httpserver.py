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
        self.response = ""
        self.file = ""
        self.content = ""
        self.proto = " HTTP/1.0"
        self.query = self.url.query if self.url.query else ""
        self.count = 0

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
        request = "{} {}?{}{}{}\r\n".format(
            self.method.upper(), self.url.path, self.query,
            self.proto, self.buildRequestheaders()
        )
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
            request = "{} {}{}{}\r\n{}".format(
                self.method.upper(), self.url.path, self.proto,
                self.buildRequestheaders(), self.data
            )
        elif self.file:
            request = "{} {}{}{}\r\n{}".format(
                self.method.upper(), self.url.path, self.proto, 
                self.buildRequestheaders(), self.file
            )
        else:
            request = "{} {}{}{}\r\n".format(
                self.method.upper(), self.url.path, self.proto, 
                self.buildRequestheaders()
            )
        self.content = request

    def checkredirection(self):
        response_list = self.response.split("\n")
        status_code = response_list[0].split(" ")[1].strip()
        if status_code in ["301", "302"]:
            print("HTTP Response : ", response_list[0])
            location = response_list[1].split(":", 1)[1].strip()
            self.url = urlparse(location)
            self.host = self.url.netloc
            self.header.update({'Host': self.host})
            self.buildGETrequest()
            return True
        return False

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
            self.count+=1
            self.response = s.recv(2048, socket.MSG_WAITALL).decode("utf-8")
            while self.checkredirection():
                print("=============== Redirecting... ===============")
                self.sendresponse()
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
