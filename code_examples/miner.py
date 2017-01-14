import hashlib
import struct
import time
import sys

# ======= Header =======
ver = 2
prev_block = "000000000000000000e5fb3654e0ae9a2b7d7390e37ee0a7c818ca09fde435f0"
mrkl_root = "6f3ef687979a1f4866cd8842dcbcebd2e47171e54d1cc76c540faecafe133c39"
bits = 0x10004379
time_ = 0x58777e25
# Calculate current time with this code:
# hex(int(time.mktime(time.strptime('2017-01-12 13:01:25', '%Y-%m-%d %H:%M:%S'))) - time.timezone)

exp = bits >> 24
mant = bits & 0xffffff
target_hexstr = '%064x' % (mant * (1 << (8 * (exp - 3))))
target_str = target_hexstr.decode('hex')
# ======== Header =========

nonce = 0
while nonce < 0x100000000:
    header = ( struct.pack("<L", ver) + prev_block.decode('hex')[::-1] +
          mrkl_root.decode('hex')[::-1] + struct.pack("<LLL", time_, bits, nonce))
    hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()

    sys.stdout.write("\rNonce: {}, hash: {}".format(nonce, hash[::-1].encode('hex')))
    sys.stdout.flush()

    if hash[::-1] < target_str:
        print 'Success!'
        break
    nonce += 1
