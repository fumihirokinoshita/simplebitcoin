# simplebitcoin
自作ブロックチェーン

参照
https://peaks.cc/books/cryptocurrency

## 環境構築(Mac)
```
$ git clone github.com/fumihirokinoshita/simplebitcoin
# cd simplebitcoin
```

## 仕様概要
- SampleServer1.py : Core Node 1
- SampleServer2.py : Core Node 2

- SampleClient1.py : Edge Node 1
- SampleClient2.py : Edge Node 2

## 動作確認

Core Nodeの立ち上げとCore Node間での接続
```
$ python3 SampleServer1.py
$ pytnon3 SampleServer2.py // 別shell
```

Blockchainに参加するクライアント(Edge Node)の立ち上げ
```
$ python3 SampleClient1.py // 別shell
$ python3 SampleClient2.py // 別shell
```