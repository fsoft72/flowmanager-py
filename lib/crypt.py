import json
import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def get_config():
    """Load configuration from cfg.json"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cfg.json')
    with open(config_path, 'r') as f:
        return json.load(f)

# Constants
ALGORITHM = 'aes-256-ctr'
try:
    cfg = get_config()
    SECRET_KEY = hashlib.md5(cfg['secret'].encode()).hexdigest().encode()
except:
    SECRET_KEY = hashlib.md5(b'l1w3fl0w').hexdigest().encode()

def encrypt(text: str) -> dict:
    """Encrypt text using AES-256-CTR"""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CTR(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    encrypted = encryptor.update(text.encode()) + encryptor.finalize()
    
    return {'iv': iv.hex(), 'content': encrypted.hex()}

def decrypt(hash_data: dict) -> str:
    """Decrypt data using AES-256-CTR"""
    iv = bytes.fromhex(hash_data['iv'])
    content = bytes.fromhex(hash_data['content'])
    
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CTR(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted = decryptor.update(content) + decryptor.finalize()
    return decrypted.decode()

def json_encrypt(data: dict) -> dict:
    """Encrypt JSON data"""
    return encrypt(json.dumps(data))

def json_decrypt(data: dict) -> dict:
    """Decrypt JSON data"""
    text = decrypt(data)
    return json.loads(text)
