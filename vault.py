from cryptography.fernet import Fernet
import os
from datetime import datetime

# Load or generate key
if os.path.exists("key.key"):
    with open("key.key", "rb") as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open("key.key", "wb") as f:
        f.write(key)

cipher = Fernet(key)

# Functions
def add_note():
    note = input("Enter new note: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = f"{timestamp} | {note}"
    encrypted = cipher.encrypt(data.encode())
    with open("vault.txt", "ab") as f:
        f.write(encrypted + b"\n")
    print("✅ Note added with timestamp.")

def read_notes():
    if not os.path.exists("vault.txt"):
        print("Vault is empty.")
        return
    with open("vault.txt", "rb") as f:
        lines = f.readlines()
    print("\n📖 Vault Notes:")
    for line in lines:
        try:
            decrypted = cipher.decrypt(line.strip()).decode()
            print(decrypted)
        except:
            print("❌ Corrupted note found.")

def search_notes():
    if not os.path.exists("vault.txt"):
        print("Vault is empty.")
        return
    keyword = input("Enter search keyword: ").lower()
    with open("vault.txt", "rb") as f:
        lines = f.readlines()
    print(f"\n🔍 Search results for '{keyword}':")
    for line in lines:
        try:
            decrypted = cipher.decrypt(line.strip()).decode()
            if keyword in decrypted.lower():
                print(decrypted)
        except:
            pass

# Main menu
while True:
    print("\n=== VX Ghost Vault ===")
    choice = input("1) Add Note  2) Read Notes  3) Search Notes  4) Exit : ")
    if choice == "1":
        add_note()
    elif choice == "2":
        read_notes()
    elif choice == "3":
        search_notes()
    else:
        break
