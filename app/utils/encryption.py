"""
Encryption utilities for the banking system
"""
import base64
import hashlib
import os
import secrets
from typing import Tuple, Optional


def generate_salt(length: int = 16) -> bytes:
    """
    Generate a random salt for password hashing
    
    Args:
        length: Length of the salt in bytes
        
    Returns:
        bytes: Random salt
    """
    return os.urandom(length)


def hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
    """
    Hash a password with a salt using PBKDF2
    
    Args:
        password: Password to hash
        salt: Salt to use (if None, a new salt will be generated)
        
    Returns:
        Tuple[bytes, bytes]: Tuple containing (hash, salt)
    """
    if salt is None:
        salt = generate_salt()
    
    # Use PBKDF2 with SHA-256, 100,000 iterations
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    
    return key, salt


def verify_password(password: str, stored_hash: bytes, salt: bytes) -> bool:
    """
    Verify a password against a stored hash
    
    Args:
        password: Password to verify
        stored_hash: Stored hash to compare against
        salt: Salt used for hashing
        
    Returns:
        bool: True if password matches, False otherwise
    """
    key, _ = hash_password(password, salt)
    return secrets.compare_digest(key, stored_hash)


def encode_biometric_data(data: bytes) -> str:
    """
    Encode biometric data for storage
    
    Args:
        data: Raw biometric data
        
    Returns:
        str: Encoded data as a string
    """
    return base64.b64encode(data).decode('utf-8')


def decode_biometric_data(encoded_data: str) -> bytes:
    """
    Decode stored biometric data
    
    Args:
        encoded_data: Encoded biometric data
        
    Returns:
        bytes: Decoded raw biometric data
    """
    return base64.b64decode(encoded_data)


def generate_token(length: int = 32) -> str:
    """
    Generate a secure random token
    
    Args:
        length: Length of the token in bytes
        
    Returns:
        str: Secure random token as a hexadecimal string
    """
    return secrets.token_hex(length)


def encrypt_sensitive_data(data: str, key: bytes) -> str:
    """
    Encrypt sensitive data
    
    Note: This is a placeholder. In a real implementation, this would use
    a proper encryption library like cryptography.fernet
    
    Args:
        data: Data to encrypt
        key: Encryption key
        
    Returns:
        str: Encrypted data
    """
    # This is just a placeholder for demonstration
    # In a real implementation, use a proper encryption library
    return f"ENCRYPTED_{data}_WITH_KEY_{key.hex()[:8]}"


def decrypt_sensitive_data(encrypted_data: str, key: bytes) -> str:
    """
    Decrypt sensitive data
    
    Note: This is a placeholder. In a real implementation, this would use
    a proper decryption library like cryptography.fernet
    
    Args:
        encrypted_data: Data to decrypt
        key: Decryption key
        
    Returns:
        str: Decrypted data
    """
    # This is just a placeholder for demonstration
    # In a real implementation, use a proper encryption library
    if encrypted_data.startswith("ENCRYPTED_") and "_WITH_KEY_" in encrypted_data:
        # Extract the original data from our placeholder format
        parts = encrypted_data.split("_WITH_KEY_")
        data = parts[0].replace("ENCRYPTED_", "")
        return data
    
    return "DECRYPTION_FAILED"
