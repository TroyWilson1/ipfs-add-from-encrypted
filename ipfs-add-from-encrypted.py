#!/usr/bin/env python3
# Takes file in does symmetric encryption with the password you provide
# then  adds it to a running IPFS(ipfs.io) instance.
#
import os
import argparse
import gnupg
import ipfsapi
import tarfile
import subprocess

# Parse command arguments
parser = argparse.ArgumentParser(description='Encrypt file/directory and add it to IPFS')
parser.add_argument('-i','--input', help='File.txt or Directory', required=True)
parser.add_argument('-p','--password', help='Password to encrypt with', required=True)
parser.add_argument('-c','--cluster', help='Add hash to ipfs-cluster-ctl', action="store_true")
args = parser.parse_args()

# Set GPG Home directory
gpg = gnupg.GPG(homedir='')
# Set GPG Encoding
gpg.encoding = 'utf-8'
# Get dataToEncrypt full path
dataToEncrypt = (os.path.abspath(args.input))
# Setup tar filename to end with .tar
tarFile = ("{}.tar".format(dataToEncrypt))
# Setup encrypted filename to end with .gpg
encryptedFile = ("{}.gpg".format(dataToEncrypt))
# Setup encrypted tar directory to end with .tar.gpg
tarEncryptedFile = ("{}.tar.gpg".format(dataToEncrypt))
# Tell module where IPFS instance is located
api = ipfsapi.connect('127.0.0.1', 5001)

def dataTar():
    if os.path.isfile(dataToEncrypt):
        return
    else:
        with tarfile.open(tarFile, 'w') as tar:
            tar.dereference=False
            tar.add(dataToEncrypt)
            tar.close()
            
def encryptFile():
    passphrase = (args.password)
    if os.path.isfile(dataToEncrypt):
        with open(dataToEncrypt, 'rb') as f:
            status = gpg.encrypt(f.read(),
               None,
               encrypt=False,
               symmetric='AES256',
               passphrase=passphrase,
               armor=False,
               output=dataToEncrypt + ".gpg")

    else:
        with open(tarFile, 'rb') as f:
            status = gpg.encrypt(f.read(),
               None,
               encrypt=False,
               symmetric='AES256',
               passphrase=passphrase,
               armor=False,
               output=dataToEncrypt + ".tar.gpg")

def ipfsFile(encryptedFile):
    try:
        # Add encrypted file to IPFS
        ipfsLoadedFile = api.add(encryptedFile, wrap_with_directory=True)
        # Return Hash of new IPFS File
        fullHash = (ipfsLoadedFile[1])
        ipfsHash = fullHash['Hash']
        return(ipfsHash)
    except:
        # Add encrypted directory to IPFS
        ipfsLoadedFile = api.add(tarEncryptedFile, wrap_with_directory=True)
        # Return Hash of new IPFS File
        fullHash = (ipfsLoadedFile[1])
        ipfsHash = fullHash['Hash']
        return(ipfsHash)
    
def delEncryptedFile():
    if os.path.isfile(encryptedFile):
        os.remove(encryptedFile)
    elif os.path.isfile(tarFile):
        os.remove(tarFile)
        os.remove(tarEncryptedFile)

def clusterAdd():
     if args.cluster:
        print (ipfsFile)
        #completed = subprocess.run(
        #['ipfs-cluster-ctl', 'pin', 'add', ipfsFile(encryptedFile) ],
        #stdout=subprocess.PIPE,
    #)
    
    #print('Have {} bytes in stdout:\n{}'.format(
    #    len(completed.stdout),
    #    completed.stdout.decode('utf-8'))
    #)

    
def main():
    dataTar()
    encryptFile()
    ipfsFile(encryptedFile)
    print ("File encrypted and added to IPFS with this hash " + ipfsFile(encryptedFile))
    delEncryptedFile()
    clusterAdd()

    
if __name__ == "__main__":    
    main()
