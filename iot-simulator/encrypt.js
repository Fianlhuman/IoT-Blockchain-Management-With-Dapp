// Import the eth-sig-util library
const ethSigUtil = require('eth-sig-util');

// Get the encryption public key and message from the command line arguments
const encryptionPublicKey = process.argv[2];
const message = process.argv[3];

// Use the eth-sig-util library to encrypt the message with the specified algorithm and public key
const encrypted = ethSigUtil.encrypt(encryptionPublicKey, { data: message }, 'x25519-xsalsa20-poly1305');

// Print the encrypted message as a JSON string to the console
console.log(JSON.stringify(encrypted));
