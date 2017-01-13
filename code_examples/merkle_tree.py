import hashlib
import Crypto.Hash.SHA256 as hash
import binascii
import hashlib

# Hash pairs of items recursively until a single value is obtained
def merkle(hashList):
    if len(hashList) == 1:
        return hashList[0]
    newHashList = []
    # Process pairs. For odd length, the last is skipped
    for i in range(0, len(hashList)-1, 2):
        newHashList.append(hash2(hashList[i], hashList[i+1]))
    if len(hashList) % 2 == 1: # odd, hash last item twice
        newHashList.append(hash2(hashList[-1], hashList[-1]))
    return merkle(newHashList)

def hash2(a, b):
    # Reverse inputs before and after hashing
    # due to big-endian / little-endian nonsense
    a1 = a.decode('hex')[::-1]
    b1 = b.decode('hex')[::-1]
    h = hashlib.sha256(hashlib.sha256(a1+b1).digest()).digest()
    return h[::-1].encode('hex')

def getTxnHash(txn):
    return hash.new(hash.new(binascii.unhexlify(txn)).digest()).digest().encode('hex_codec')[::1]

txn_pool = [
    "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff8c493046022100f89c52e29e0d3236a5904b2be8fdc1343d21fa776f92b870bcbd01b1275c297c022100d072ac5cbb5ee548d0966d6bca612ad7fd338c0633534105be62e819ceb5298601410497e922cac2c9065a0cac998c0735d9995ff42fb6641d29300e8c0071277eb5b4e770fcc086f322339bdefef4d5b51a23d88755969d28e965dacaaa5d0d2a0e09ffffffff01ddff814a000000001976a91478e10cf8e4bd38266d8fd4ed5c8b430d30a3cde888ac00000000",
    "0100000001440d795fa6267cbae00ae18e921a7b287eaa37d7f41b96ccbc61ef9a323a003d010000006a47304402204137ef9ca79bcd8a953c0def89578838bbe882fe7814d6a7144eaa25ed156f66022043a4ab91a7ee3bf58155d08e5f3f221a783f645daf9ac54fed519e18ca434aea012102965a03e05b2e2983c031b870c9f4afef1141bf30dc5bb993197ee4a52f1443e0feffffff0200a3e111000000001976a914f1cfa585d096ea3c759940d7bacd8c7259bbd4d488ac4e513208000000001976a9146701f2540186d4135eec14dad6cb25bf757fc43088accbd50600",
    "0100000001517063b3d932693635999b8daaed9ebf020c66c43abf504f3043850bca5a936d010000006a47304402207473cda71b68a414a53e01dc340615958d0d79dd67196c4193a0ebcf0d9f70530220387934e7317b60297f5c6e0ca4bf527faaad830aff45f1f5522e842595939e460121031d53a2c228aedcde79b6ccd2e8f5bcfb56e2046b4681c4ea2173e3c3d7ffc686ffffffff0220bcbe00000000001976a9148cc3704cbb6af566598fea13a3352b46f859581188acba2cfb09000000001976a914b59b9df3700adae0ea819738c89db3c2af4e47d188ac00000000"
]

txn_hashes = map(getTxnHash, txn_pool)

print "Txn hashes:", txn_hashes

print "Merkle root: ", merkle(txn_hashes)
