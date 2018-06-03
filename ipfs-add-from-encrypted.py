#!/usr/bin/env python3
# Takes file in does symmetric encryption with the password you provide
# then  adds it to a running IPFS(ipfs.io) instance.
#
import os
import argparse
import ipfsapi
import subprocess

# Parse command arguments
parser = argparse.ArgumentParser(description='Encrypt file/directory and add it to IPFS')
parser.add_argument('-i','--input', help='File.txt or Directory', required=True)
parser.add_argument('-n','--name', help='Set encrypted output filename', required=True)
args = parser.parse_args()

# Get dataToEncrypt full path
dataToEncrypt = (os.path.abspath(args.input))

# File
fileReady = (args.name + ".gpg")
# Tar
tarReady = (args.name + ".tgz.gpg")

# Tell module where IPFS instance is located
api = ipfsapi.connect('127.0.0.1', 5001)


def packageData():
    if os.path.isfile(dataToEncrypt):
        subprocess.run(["gpg", "-o", args.name + ".gpg", "-c", dataToEncrypt])
    else:
        ps = subprocess.Popen(("tar", "-cz", dataToEncrypt),stdout=subprocess.PIPE)
        output = subprocess.check_output(("gpg", "-c", "-o", args.name + ".tgz.gpg"), stdin=ps.stdout)
        ps.wait() 

def ipfsFile():
    try:
        # Add encrypted file to IPFS
        ipfsLoadedFile = api.add(fileReady, wrap_with_directory=True)
        # Return Hash of new IPFS File
        fullHash = (ipfsLoadedFile[1])
        ipfsFile.ipfsHash = fullHash['Hash']
        return(ipfsFile.ipfsHash)
    except:
        # Add encrypted directory to IPFS
        ipfsLoadedFile = api.add(tarReady, wrap_with_directory=True)
        # Return Hash of new IPFS File
        fullHash = (ipfsLoadedFile[1])
        ipfsFile.ipfsHash = fullHash['Hash']
        return(ipfsFile.ipfsHash)

def delEncryptedFile():
    if os.path.isfile(fileReady):
        os.remove(fileReady)
    elif os.path.isfile(tarReady):
        os.remove(tarReady)

def main():
    packageData()
    ipfsFile()
    print ("File encrypted and added to IPFS with this hash " + ipfsFile.ipfsHash)
    delEncryptedFile()
    
    
if __name__ == "__main__":    
    main()
