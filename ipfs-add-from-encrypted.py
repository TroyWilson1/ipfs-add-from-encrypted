#!/usr/bin/env python3
# Takes file in does symmetric encryption with the password you provide
# then  adds it to a running IPFS(ipfs.io) instance.
#
import os
import argparse
import gnupg
import ipfsapi
import tarfile

# Parse command arguments
parser = argparse.ArgumentParser(description='Encrypt file/directory and add it to IPFS')
parser.add_argument('-i','--input', help='File.txt or Directory', required=True)
parser.add_argument('-p','--password', help='Password to encrypt with', required=True)
args = parser.parse_args()

# Set GPG Home directory
gpg = gnupg.GPG(homedir='')
# Set GPG Encoding
gpg.encoding = 'utf-8'
# Get dataToEncrypt full path
dataToEncrypt = (os.path.abspath(args.input))
# Setup tar filename to end with .zip
tarFile = ("{}.tgz".format(dataToEncrypt))
# Setup encrypted filename to end with .gpg
encryptedFile = ("{}.tgz.gpg".format(dataToEncrypt))
# Tell module where IPFS instance is located
api = ipfsapi.connect('127.0.0.1', 5001)

def dataTar():
    if os.path.isfile(dataToEncrypt):
        return
    else:
        with tarfile.open(tarFile, 'w:gz') as tar:
            tar.add(dataToEncrypt)
            tar.close()
            
def encryptFile():
    passphrase = (args.password)
    if os.path.isfile(dataToEncrypt):
        with open(dataToEncrypt, 'rb') as f:
            status = gpg.encrypt_file(f,
               encrypt=False,
               symmetric='AES256',
               passphrase=passphrase,
               armor=False,
               output=dataToEncrypt + ".gpg")

    else:
        with open(tarFile, 'rb') as f:
            status = gpg.encrypt(f,
               encrypt=False,
               symmetric='AES256',
               passphrase=passphrase,
               armor=False,
               output=dataToEncrypt + ".tgz.gpg")
        print ('ok: ', status.ok)
        print ('status: ', status.status)
        print ('stderr: ', status.stderr)

            
def ipfsFile(encryptedFile):
    # Add encrypted file to IPFS
    ipfsLoadedFile = api.add(encryptedFile, wrap_with_directory=True)
    # Return Hash of new IPFS File
    fullHash = (ipfsLoadedFile[1])
    ipfsHash = fullHash['Hash']
    return(ipfsHash)
    
def delEncryptedFile(encryptedFile):
    try:
        os.remove(encryptedFile)
    except:
        print("Error: %s unable to find or delete file." % encryptedFile)

    
def main():
    dataTar()
    encryptFile()
    #ipfsFile(encryptedFile)
    #print ("File encrypted and added to IPFS with this hash " + ipfsFile(encryptedFile))
    #delEncryptedFile(encryptedFile)

if __name__ == "__main__":    
    main()
