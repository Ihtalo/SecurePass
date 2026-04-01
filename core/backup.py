import json
from core.storage import load_passwords, save_passwords

def export_passwords(file_path):
    data = {
        "format": "SecurePass Backup",
        "passwords": load_passwords()
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def import_passwords(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("format") != "SecurePass Backup":
        raise ValueError("Arquivo inválido")

    save_passwords(data["passwords"])