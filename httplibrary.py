#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
from urllib.parse import urlparse


class HTTPLibrary:
    """
    HTTPLibrary class used to represent all the server side operations
    Methods
    -------
    __init__(self, url)
        It is contructor for HTTPLibrary class.
    setMethod(self, method)
        It is used to set HTTP method.
    setData(self, data)
        It is used to set data.
    setStatusCode(self, status_code)
        It is used to set status code of response.
    getStatusCode(self)
        It is used to get status code of response.
    setFile(self, file)
        It is used to set file data.
    setVerbose(self, verbose)
        It is used to set verbose.
    getVerbose(self)
        It is used to get verbose value.
    getResponse(self)
        It is used to get response based on verbose.
    setHeader(self, key, value)
        It is used to set header value.
    buildRequestheaders(self)
        It is used to generate headers.
    buildRequest(self)
        It is used to build a request based on method.
    buildGETrequest(self)
        It is used to build a GET method request.
    buildPOSTrequest(self)
        It is used to build a POST method request.
    sendresponse(self)
        It is used to send the response back to client.
    """

    def __init__(self, url):
        """It is contructor for HTTPLibrary class.

        Parameters
        -------
        url
            a string containing URL
        """
        self.url = urlparse(url)
        self.host = self.url.netloc
        self.header = {"Host": self.host}
        self.method = ""
        self.data = ""
        self.status_code = ""
        self.response = ""
        self.file = ""
        self.verbose = False
        self.content = ""
        self.proto = " HTTP/1.0"
        self.query = self.url.query if self.url.query else ""
        self.count = 0

    def setMethod(self, method):
        """It is used to set HTTP method.

        Parameters
        -------
        method
            a string containing HTTP method
        """
        self.method = method

    def setData(self, data):
        """It is used to set data.

        Parameters
        -------
        data
            a string containing data
        """
        self.data = data

    def setStatusCode(self, status_code):
        """It is used to set status code of response.

        Parameters
        -------
        status_code
            a string containing status code
        """
        self.status_code = status_code

    def getStatusCode(self):
        """It is used to get status code of response.

        Returns
        -------
        string
            a string containing status code
        """
        return self.status_code

    def setFile(self, file):
        """It is used to set file data.

        Parameters
        -------
        file
            a string containing file data
        """
        self.file = file

    def setVerbose(self, verbose):
        """It is used to set verbose.

        Parameters
        -------
        verbose
            a bool value of verbose
        """
        self.verbose = verbose

    def getVerbose(self):
        """It is used to get verbose value.

        Returns
        -------
        bool
            True if verbose is set, False otherwise
        """
        return self.verbose

    def getResponse(self):
        """It is used to get response based on verbose.

        Returns
        -------
        string
            a string response
        """
        response = self.response
        if not self.getVerbose():
            response = response.split("\r\n\r\n")[1]
        return response

    def setHeader(self, key, value):
        """It is used to set header value.

        Parameters
        -------
        key
            a string containing header name
        value
            a string containing header value
        """
        self.header.update({key: value})

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

    def buildRequest(self):
        """It is used to build a request based on method.
        """
        if self.method.upper() == 'GET':
            self.buildGETrequest()
        if self.method.upper() == 'POST':
            self.buildPOSTrequest()

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
        self.setStatusCode(status_code)
        if status_code in ["301", "302"]:
            print("\nHTTP Response : ", response_list[0])
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
        HTTPLibrary
            a HTTPLibrary class object to client
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host, 80))
            s.sendall(self.content.encode("utf-8"))
            self.count += 1
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
