# COMP-6461-Assignment-1
COMP-6461-Assignment-1

### commands
    - python httpc.py -h
    - python httpc.py get -h
    - python httpc.py post -h
    - python httpc.py get 'http://httpbin.org/get?course=networking&assignment=1'
    - python httpc.py get 'http://httpbin.org/get?course=networking&assignment=1' -o output.txt
    - python httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1' 
    - python httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1' -o output.txt
    - python httpc.py post --h Content-Type:application/json -d '{"Assignment": 1}' \
        http://httpbin.org/post
    - python httpc.py post --h Content-Type:application/json -d '{"Assignment": 1}' \
        http://httpbin.org/post -o output.txt
    - python httpc.py post -v --h Content-Type:application/json -d '{"Assignment": 1}' \
        http://httpbin.org/post
    - python httpc.py post -v --h Content-Type:application/json -d '{"Assignment": 1}' \
        http://httpbin.org/post -o output.txt
    - python httpc.py post --h Content-Type:application/json -f "data.txt" \
        "http://httpbin.org/post"
    - python httpc.py post --h Content-Type:application/json -f "data.txt" \
        "http://httpbin.org/post" -o output.txt
    - python httpc.py post -v --h Content-Type:application/json -f "data.txt" \
        "http://httpbin.org/post"
    - python httpc.py post -v --h Content-Type:application/json -f "data.txt" \
        "http://httpbin.org/post" -o output.txt
    - python httpc.py get -v "http://google.com/"

