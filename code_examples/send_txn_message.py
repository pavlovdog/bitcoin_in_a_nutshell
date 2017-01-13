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

def txnMessage(previous_output, receiver_address, my_address, private_key):
    receiver_hashed_pubkey= base58.b58decode_check(receiver_address)[1:].encode("hex")
    my_hashed_pubkey = base58.b58decode_check(my_address)[1:].encode("hex")

    # Transaction stuff
    version = struct.pack("<L", 1)
    lock_time = struct.pack("<L", 0)
    hash_code = struct.pack("<L", 1)

    # Transactions input
    tx_in_count = struct.pack("<B", 1)
    tx_in = {}
    tx_in["outpoint_hash"] = previous_output.decode('hex')[::-1]
    tx_in["outpoint_index"] = struct.pack("<L", 0)
    tx_in["script"] = ("76a914%s88ac" % my_hashed_pubkey).decode("hex")
    tx_in["script_bytes"] = struct.pack("<B", (len(tx_in["script"])))
    tx_in["sequence"] = "ffffffff".decode("hex")

    # Transaction output
    tx_out_count = struct.pack("<B", 1)

    tx_out = {}
    tx_out["value"]= struct.pack("<Q", 1000) # Send 1000 satoshis
    tx_out["pk_script"]= ("76a914%s88ac" % receiver_hashed_pubkey).decode("hex")
    tx_out["pk_script_bytes"]= struct.pack("<B", (len(tx_out["pk_script"])))

    tx_to_sign = (version + tx_in_count + tx_in["outpoint_hash"] + tx_in["outpoint_index"] +
                  tx_in["script_bytes"] + tx_in["script"] + tx_in["sequence"] + tx_out_count +
                  tx_out["value"] + tx_out["pk_script_bytes"] + tx_out["pk_script"] + lock_time + hash_code)

    # Signing txn
    hashed_raw_tx = hashlib.sha256(hashlib.sha256(tx_to_sign).digest()).digest()
    sk = ecdsa.SigningKey.from_string(private_key.decode("hex"), curve = ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = ('\04' + vk.to_string()).encode("hex")
    sign = sk.sign_digest(hashed_raw_tx, sigencode=ecdsa.util.sigencode_der)

    # Complete txn
    sigscript = sign + "\01" + struct.pack("<B", len(public_key.decode("hex"))) + public_key.decode("hex")

    real_tx = (version + tx_in_count + tx_in["outpoint_hash"] + tx_in["outpoint_index"] +
    struct.pack("<B", (len(sigscript) + 1)) + struct.pack("<B", len(sign) + 1) + sigscript +
    tx_in["sequence"] + tx_out_count + tx_ou["value"] + tx_out["pk_script_bytes"] + tx_out["pk_script"] + lock_time)

    return real_tx


if __name__ == "__main__":

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("70.68.73.137", 8333))

    sock.send(makeMessage("version", versionMessage()))
    sock.recv(1024) # version
    sock.recv(1024) # verack

    # Transaction options
    previous_output = "60ee91bc1563e44866c66937b141e9ef4615a272fa9d764b9468c2a673c55e01"
    receiver_address = "1C29gpF5MkEPrECiGtkVXwWdAmNiQ4PBMH"
    my_address = "1LwPhYQi4BRBuuyWSGVeb6kPrTqpSVmoYz"
    private_key = "28da5896199b85a7d49b0736597dd8c0d0c0293f130bf3e3e1d102e0041b1293"

    txn = txnMessage(previous_output, receiver_address, my_address, private_key)
    print "Signed txn:", txn

    sock.send(makeMessage("tx", txn))
    sock.recv(1024) # inv
