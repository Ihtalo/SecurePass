import json
import hashlib
import os
from cryptography.fernet import Fernet

CONFIG_PATH = "data/config.json"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def master_password_exists() -> bool:
    if not os.path.exists(CONFIG_PATH):
        return False

    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    return bool(data.get("master_password"))

def generate_key():
    return Fernet.generate_key().decode()

def set_master_password(password: str):
    data = {
        "master_password": hash_password(password),
        "key": generate_key()
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)

def verify_master_password(password: str) -> bool:
    if not master_password_exists():
        return False

    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    return data["master_password"] == hash_password(password)

def get_cipher():
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    key = data["key"].encode()
    return Fernet(key)