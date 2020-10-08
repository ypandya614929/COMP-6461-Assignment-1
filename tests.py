from httplibrary import HTTPLibrary
import unittest

class TestCases(unittest.TestCase):

    def test_getrequest(self):
        http_lib_obj = HTTPLibrary("http://httpbin.org/get?course=networking&assignment=1")
        http_lib_obj.setMethod('get')
        http_lib_obj.setVerbose(True)
        http_lib_obj.buildRequest()
        response_obj = http_lib_obj.sendresponse()
        # print(response_obj.getResponse())
        self.assertEqual(response_obj.getStatusCode(), '200')

    def test_postrequest(self):
        http_lib_obj = HTTPLibrary("http://httpbin.org/post")
        http_lib_obj.setMethod('post')
        data = '{"Assignment":"1"}'
        http_lib_obj.setData(data)
        http_lib_obj.setHeader("User-Agent", "COMP-6461/1.0")
        http_lib_obj.setHeader("Content-Type", "application/json")
        http_lib_obj.setHeader("Content-Length",str(len(data)))
        http_lib_obj.setVerbose(False)
        http_lib_obj.buildRequest()
        response_obj = http_lib_obj.sendresponse()
        # print(response_obj.getResponse())
        self.assertEqual(response_obj.getStatusCode(), '200')
    
    def test_redirection(self):
        http_lib_obj = HTTPLibrary("http://google.com/")
        http_lib_obj.setMethod('get')
        http_lib_obj.setVerbose(False)
        http_lib_obj.buildRequest()
        response_obj = http_lib_obj.sendresponse()
        # print(response_obj.getResponse())
        self.assertEqual(response_obj.getStatusCode(), '200')

        
if __name__ == '__main__':
    unittest.main()