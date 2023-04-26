import binascii
import subprocess
import json

# Convert a stringifiable value to a hexadecimal string with a '0x' prefix
def stringifiableToHex(value):
    value_json = json.dumps(value)
    value_bytes = value_json.encode('utf-8')
    value_hex = binascii.hexlify(value_bytes)
    return '0x' + value_hex.decode('utf-8')

# Encrypt a message using the specified encryption public key and the 'encrypt.js' Node.js script
def encrypt_message(encryption_public_key, message):
    # Use the subprocess module to run the 'encrypt.js' script with the specified encryption public key and message
    result = subprocess.run(
        ["node", "encrypt.js", encryption_public_key, message],
        capture_output=True,
        universal_newlines=True,
        check=True
    )
    # Convert the encrypted message from a JSON string to a hexadecimal string with a '0x' prefix
    encrypted_message = stringifiableToHex(json.loads(result.stdout))
    return encrypted_message


# Test the encrypt_message function with an example
encryption_public_key = "aZ3R43O3NNwoOJlMwPXw6Jd0nIFhStflXVEork1JfGQ="
message = "Jiawei"

try:
    encrypted_message = encrypt_message(encryption_public_key, message)
    print(encrypted_message)
except subprocess.CalledProcessError as e:
    print(f"Error: {e.returncode}\nOutput: {e.output}\nError output: {e.stderr}")
