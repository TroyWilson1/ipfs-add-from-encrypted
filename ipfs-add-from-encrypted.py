#!/usr/bin/env python3
# Takes file in does symmetric encryption with the password you provide
# then  adds it to a running IPFS(ipfs.io) instance.
#
import os
import argparse
import gnupg
import ipfsapi 

# Parse command arguments
parser = argparse.ArgumentParser(description='Encrypt file and add it to IPFS')
parser.add_argument('-i','--input', help='File_To_Encrypt.doc', required=True)
parser.add_argument('-p','--password', help='Password to encrypt with', required=True)
args = parser.parse_args()

# Set GPG Encoding
gpg.encoding = 'utf-8'
# Set GPG Home directory
gpg = gnupg.GPG(homedir='')
# Get fileToEncrypt full path
fileToEncrypt = (os.path.abspath(args.input))
# Setup encrypted filename to end with.gpg
encryptedFile = ("{}.gpg".format(fileToEncrypt))
# Tell module where IPFS instance is located
api = ipfsapi.connect('127.0.0.1', 5001)

def encryptFile():
    passphrase = (args.password)
    with open(fileToEncrypt, 'rb') as f:
        status = gpg.encrypt(f,
            encrypt=False,
            symmetric='AES256',
            passphrase=passphrase,
            armor=False,
            output=fileToEncrypt + ".gpg")

def ipfsFile(encryptedFile):
    # Add encrypted file to IPFS
    ipfsLoadedFile = api.add(encryptedFile, wrap_with_directory=True)
    # Return Hash of new IPFS File
    hashDict = (ipfsLoadedFile[1])
    ipfsHash = (hashDict['Hash'])
    return(ipfsHash)
    
def delEncryptedFile(encryptedFile):
    try:
        os.remove(encryptedFile)
    except:
        print("Error: %s unable to find or delete file." % encryptedFile)
        
def main():
    encryptFile()
    ipfsFile(encryptedFile)
    print ("File encrypted and added to IPFS with this hash " + ipfsFile(encryptedFile))
    delEncryptedFile(encryptedFile)

if __name__ == "__main__":    
    main()
