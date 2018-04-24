# ipfs-add-from-encrypted

Still working on the README.md notes

This script takes a file, does symmetric encryption with the password you provide and adds it to IPFS and returns the IPFS hash.

## Usage:
```
./ipfs-add-from-encrypted.py -i test.txt -p test
File encrypted and added to IPFS with this hash QmYjK5jHgYSyeyKZqDZyLCzrziphB18wuM93mXtySEryD1
```

## Help:
```
usage: ipfs-add-from-encrypted.py [-h] -i INPUT -p PASSWORD

Encrypt file and add it to IPFS

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        File_To_Encrypt.doc
  -p PASSWORD, --password PASSWORD
                        Password to encrypt with
```
