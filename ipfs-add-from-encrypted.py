#!/usr/local/bin/python3
# Takes file in does symmetric encryption with the password you provide
# then  adds it to a running IPFS(ipfs.io) instance.
#
import os
import sys
import gnupg
import ipfsapi 

# Get fileToEncrypt argument
path = sys.argv[1]
# Set GPG Home directory
gpg = gnupg.GPG(homedir='')
# Get fileToEncrypt full path
fileToEncrypt = (os.path.abspath(path))
# Setup encrypted filename to end with.gpg
encryptedFile = (fileToEncrypt + ".gpg")

def encryptFileFunction():
    passphrase = input("Password you would like encrypt with \n:")
    with open(fileToEncrypt, 'rb') as f:
        status = gpg.encrypt(f,
            encrypt=False,
            symmetric='AES256',
            passphrase=passphrase,
            armor=False,
            output=fileToEncrypt + ".gpg")

def ipfsFileFunction(encryptedFile):
    # Tell module where IPFS instance is located
    api = ipfsapi.connect('127.0.0.1', 5001)
    # Add Encrypted file to IPFS
    ipfsLoadedFile = api.add(encryptedFile)
    # Return Hash of new IPFS File
    ipfsHash = (ipfsLoadedFile['Hash'])
    return ipfsHash
    
def delEncryptedFile(encryptedFile):
    if os.path.isfile(encryptedFile):
        os.remove(encryptedFile)
    else:    
        print("Error: %s file not found" % encryptedFile)

def main():
    encryptFileFunction()
    ipfsFileFunction(encryptedFile)
    print ("File encrypted and added to IPFS with this hash " + ipfsFileFunction(encryptedFile))
    delEncryptedFile(encryptedFile)

main()
