# ipfs-add-from-encrypted

This script takes a file or directroy as input, uses tar if a directory and GPG AES256 symmetric encryption with the password you provide and adds it to IPFS and returns the IPFS hash. 

## USAGE:
### Add Single File:
```
./ipfs-add-from-encrypted.py -i test.txt -n Secrets.Out
File encrypted and added to IPFS with this hash QmYjK5jHgYSyeyKZqDZyLCzrziphB18wuM93mXtySEryD1
```
### Add Directory:
```
./ipfs-add-from-encrypted.py -i /home/testing/stuff -n Stuff.Out
File encrypted and added to IPFS with this hash QmYjK5jHgYSyeyKZqDZyLCzrziphB18wuM93mXtySEryD1
```

## Help:
```
usage: ipfs-add-from-encrypted.py [-h] -i INPUT -n NAME

Encrypt file/directory and add it to IPFS

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        File.txt or Directory
  -n NAME, --name NAME  Set encrypted output filename
```
