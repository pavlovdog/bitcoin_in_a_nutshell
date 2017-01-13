import time
import socket
import struct
import random
import hashlib
import base58
import ecdsa

def coinbaseMessage(previous_output, receiver_address, my_address, private_key):
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
    tx_in["outpoint_index"] = struct.pack("<L", 4294967295)
    tx_in["script"] = ("76a914%s88ac" % my_hashed_pubkey).decode("hex")
    tx_in["script_bytes"] = struct.pack("<B", (len(tx_in["script"])))
    tx_in["sequence"] = "ffffffff".decode("hex")

    # Transaction output
    tx_out_count = struct.pack("<B", 1)

    tx_out = {}
    tx_out["value"]= struct.pack("<Q", 100000000 * 12.50033629)
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
    tx_in["sequence"] + tx_out_count + tx_out["value"] + tx_out["pk_script_bytes"] + tx_out["pk_script"] + lock_time)

    return real_tx

if __name__ == "__main__":

    # Transaction options
    previous_output = "0000000000000000000000000000000000000000000000000000000000000000"
    receiver_address = "1C29gpF5MkEPrECiGtkVXwWdAmNiQ4PBMH"
    my_address = "1LwPhYQi4BRBuuyWSGVeb6kPrTqpSVmoYz"
    private_key = "28da5896199b85a7d49b0736597dd8c0d0c0293f130bf3e3e1d102e0041b1293"

    txn = coinbaseMessage(previous_output, receiver_address, my_address, private_key)
    print "Coinbase txn:", txn.encode('hex')
