import time
import socket
import struct
import random
import hashlib

def makeMessage(cmd, payload):
    magic = "F9BEB4D9".decode("hex") # Main network ID
    command = cmd + (12 - len(cmd)) * "\00"
    length = struct.pack("I", len(payload))
    check = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return magic + command + length + check + payload

def versionMessage():
    version = struct.pack("i", 60002)
    services = struct.pack("Q", 0)
    timestamp = struct.pack("q", time.time())

    addr_recv = struct.pack("Q", 0)
    addr_recv += struct.pack(">16s", "127.0.0.1")
    addr_recv += struct.pack(">H", 8333)

    addr_from = struct.pack("Q", 0)
    addr_from += struct.pack(">16s", "127.0.0.1")
    addr_from += struct.pack(">H", 8333)

    nonce = struct.pack("Q", random.getrandbits(64))
    user_agent = struct.pack("B", 0) # Anything
    height = struct.pack("i", 0) # Block number, doesn't matter

    payload = version + services + timestamp + addr_recv + addr_from + nonce + user_agent + height

    return payload

if __name__ == "__main__":

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("93.170.187.9", 8333))

    sock.send(makeMessage("version", versionMessage()))
    sock.recv(1024) # receive version message
    sock.recv(1024) # receive verack message
