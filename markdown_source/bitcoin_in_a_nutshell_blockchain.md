

![meme](https://svbtleusercontent.com/xpk4h3gh3zoq_small.png)

### Table of content

1. Public ledger
2. Block
3. Technical side
4. Links

### Blockchain for dummies

Хорошая иллюстрация блокчейна - это книга бухгалтерского учета, в которую записаны все транзакции в сети Bitcoin. Более того, такая книга присутствует у каждого участника сети, а значит любой при желании может проверить 

И если блокчейн целиком - это книга, то отдельные блоки можно представлять как страницы, на которых "записываются" транзакции.

### Structure

Привычным движением руки открываем [спецификацию протокола](https://en.bitcoin.it/wiki/Protocol_documentation#block) и смотрим на структуру блока.

![](https://habrastorage.org/files/0e5/0d3/059/0e50d30597f942e7abc2083edfc4eecb.png)

- *version* - 
- *prev_block* - хэш предыдущего блока, его еще называют *parent block*.
- *merkle_root* 
- timestamp - дата и время создания блока
- *bits*, *nonce* - про эти параметры я подробно расскажу в отдельной главе [Bitcoin in a nutshell - Mining](), пока что считайте их просто какими-то натуральными числами
- *txn_count*, *txns* - число транзакций в блоке и сам список транзакций

#### Merkle tree

![merkle](https://i.imgur.com/m26QGtS.jpg)

### Technical side

### Links

- [Basic operations with LevelDB](http://codeofrob.com/entries/basic-operations-with-leveldb.html)
- [Having a look at LevelDB](http://skipperkongen.dk/2013/02/14/having-a-look-at-leveldb/)
- [Documentation of the physical Bitcoin blockchain](http://2.bp.blogspot.com/-DaJcdsyqQSs/UsiTXNHP-0I/AAAAAAAATC0/kiFRowh-J18/s1600/blockchain.png)
- [What are the keys used in the blockchain levelDB](http://bitcoin.stackexchange.com/questions/28168/what-are-the-keys-used-in-the-blockchain-leveldb-ie-what-are-the-keyvalue-pair)
