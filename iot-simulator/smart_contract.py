# Import necessary libraries
import json
import os
from web3 import Web3

# Get the path of the current script's directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# Construct the path of the ABI file
file_path = os.path.join(dir_path, 'abi.json')

# Load the contract's ABI from the ABI file
with open(file_path, 'r') as f:
    abi = json.load(f)

# Connect to the RPC server using the HTTPProvider
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Get an instance of the smart contract using its address and ABI
contract = w3.eth.contract(address='0x3611b04d7090b713797639512601A1195FEcD249', abi=abi)

# Check if a device owner exists for a given device address
def check_device_owner_exist(_address):
    # Convert the device address to a checksum address
    checksum_address = Web3.toChecksumAddress(_address)
    
    # Call the ownerOf() function of the smart contract to get the device owner's address
    owner_address = contract.functions.ownerOf(checksum_address).call()
    
    # Check if the owner's address is the zero address, which means the device has no owner
    if owner_address == "0x0000000000000000000000000000000000000000":
        return False
    else:
        return True

# Get the address of the device owner for a given device address
def get_device_owner_address(_address):
    # Convert the device address to a checksum address
    checksum_address = Web3.toChecksumAddress(_address)
    
    # Call the ownerOf() function of the smart contract to get the device owner's address
    owner_address = contract.functions.ownerOf(checksum_address).call()
    
    return owner_address

# Get the public key of the device owner for a given device address
def get_device_owner_public_key(_address):
    # Convert the device address to a checksum address
    checksum_address = Web3.toChecksumAddress(_address)
    
    # Call the getPublicKey() function of the smart contract to get the device owner's public key
    public_key = contract.functions.getPublicKey(checksum_address).call()
    
    return public_key
