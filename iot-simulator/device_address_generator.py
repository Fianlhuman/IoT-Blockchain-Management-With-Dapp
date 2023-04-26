import os
import binascii
import hashlib
import ecdsa

def generate_device_address():
    # Generate a private key
    private_key = os.urandom(32)

    # Convert the private key to hexadecimal format
    private_key_hex = binascii.hexlify(private_key).decode()

    # Generate a public key using the private key
    signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    public_key = b"\x04" + verifying_key.to_string()

    # Hash the public key to obtain the device address
    sha3_256 = hashlib.sha3_256()
    sha3_256.update(public_key)
    digest = sha3_256.digest()
    ethereum_address = '0x' + binascii.hexlify(digest[-20:]).decode()

    # Return the private key, public key, public key address, and Ethereum address
    return {
        'private_key': private_key_hex,
        'public_key': public_key.hex(),
        'ethereum_address': ethereum_address
    }
