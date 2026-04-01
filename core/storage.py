import json
import os
from core.auth import get_cipher

PASSWORD_PATH = "data/passwords.json"

def load_passwords():
    if not os.path.exists(PASSWORD_PATH):
        return []

    with open(PASSWORD_PATH, "r") as f:
        data = json.load(f)

    cipher = get_cipher()

    for entry in data:
        try:
            entry["password"] = cipher.decrypt(
                entry["password"].encode()
            ).decode()
        except:
            entry["password"] = "ERRO"

    return data

def save_passwords(passwords):
    cipher = get_cipher()

    encrypted = []
    for entry in passwords:
        enc = entry.copy()
        enc["password"] = cipher.encrypt(
            entry["password"].encode()
        ).decode()
        encrypted.append(enc)

    with open(PASSWORD_PATH, "w") as f:
        json.dump(encrypted, f, indent=4)

def add_password(entry):
    passwords = load_passwords()
    passwords.append(entry)
    save_passwords(passwords)

def delete_password(service_name):
    passwords = load_passwords()
    passwords = [p for p in passwords if p["service"] != service_name]
    save_passwords(passwords)