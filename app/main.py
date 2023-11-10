import json
import sys
import io
#from io import StringIO,BufferedReader

# import bencodepy - available if you need it!
# import requests - available if you need it!

def peek(f : io.BufferedReader) -> chr:
    return chr(f.peek(1)[0])

def read_int(f : io.BufferedReader) -> int:
    cnt = 0
    sign = 1
    if peek(f) == "-":
        sign = -1
        f.read(1)
    while peek(f).isdigit():
        cnt = cnt*10 + int(f.read(1))
    f.read(1) # skip "e"
    return sign*cnt    

def decode(f : io.BufferedReader) -> str | int | list :    
    head = peek(f)
    if head.isdigit():
        return f.read(read_int(f)) #.decode()
    if head == "i":
        f.read(1) # skip "i"
        return read_int(f)
    if head == "l":
        f.read(1) # skip "["
        ans = []
        while peek(f) != "e":
            ans.append(decode(f))
        return ans
    if head == "d":
        f.read(1) # skip "["
        ans = {}
        while peek(f) != "e":
            key = decode(f).decode()
            # print("key:",key)            
            ans[key] = decode(f)
        return ans
    else:
        return None

# Examples:
#
# - decode_bencode(b"5:hello") -> b"hello"
# - decode_bencode(b"10:hello12345") -> b"hello12345"
# - decode_bencode(b"i52e") -> b"52"
# - decode_bencode(b"i-52e") -> b"-52"

def decode_bencode(bencoded_value : bytes):
    f = io.BufferedReader(io.BytesIO(bencoded_value))
    #f = io.BytesIO(bencoded_value)
    return decode(f)

def main():
    command = sys.argv[1]

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!?")

    if command == "decode":
        bencoded_value = sys.argv[2].encode()

        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #
        # Let's convert them to strings for printing to the console.
        def bytes_to_str(data):
            if isinstance(data, bytes):
                return data.decode()

            raise TypeError(f"Type not serializable: {type(data)}")

        # Uncomment this block to pass the first stage
        print(json.dumps(decode_bencode(bencoded_value), default=bytes_to_str))
    elif command == "info":
        path = sys.argv[2]
        with open(path,"rb") as f:
            info = decode(f)
            print("Tracker URL:",info["announce"].decode())
            print("Length:",info["info"]["length"])
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
