# cipher_tool.py
"""
A simple AES-based file encryption and decryption tool for automating code protection.
"""
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

import hashlib

BLOCK_SIZE = 16  # AES block size in bytes
SALT_SIZE = 16   # Salt size in bytes
KEY_SIZE = 32    # AES-256
ITERATIONS = 100_000

def pad(data):
    padding_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([padding_len]) * padding_len

def unpad(data):
    padding_len = data[-1]
    return data[:-padding_len]

def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=KEY_SIZE, count=ITERATIONS)

def encrypt_file(input_path, output_path, password):
    salt = get_random_bytes(SALT_SIZE)
    key = derive_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC)
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    padded = pad(plaintext)
    ciphertext = cipher.encrypt(padded)
    with open(output_path, 'wb') as f:
        f.write(salt + cipher.iv + ciphertext)
    print(f"Encrypted {input_path} -> {output_path}")

def decrypt_file(input_path, output_path, password):
    with open(input_path, 'rb') as f:
        salt = f.read(SALT_SIZE)
        iv = f.read(BLOCK_SIZE)
        ciphertext = f.read()
    key = derive_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    padded = cipher.decrypt(ciphertext)
    plaintext = unpad(padded)
    with open(output_path, 'wb') as f:
        f.write(plaintext)
    print(f"Decrypted {input_path} -> {output_path}")

def generate_checksum(file_path, algo='sha256'):
    """
    Generate a checksum (SHA-256 by default) for a file.
    """
    h = hashlib.new(algo)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()

def verify_checksum(file_path, expected_checksum, algo='sha256'):
    """
    Verify a file's checksum matches the expected value.
    """
    actual = generate_checksum(file_path, algo)
    return actual == expected_checksum, actual

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files using AES.")
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help='Mode: encrypt or decrypt')
    parser.add_argument('input', help='Input file path')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('password', help='Password for encryption/decryption')
    args = parser.parse_args()
    if args.mode == 'encrypt':
        encrypt_file(args.input, args.output, args.password)
    else:
        decrypt_file(args.input, args.output, args.password)

# Example usage:
# checksum = generate_checksum('somefile.py')
# ok, actual = verify_checksum('somefile.py', checksum)
