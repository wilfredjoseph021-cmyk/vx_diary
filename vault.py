# vault.py
from cryptography.fernet import Fernet
import os
from datetime import datetime
from ghost_agent import ghost_reply  # AI Ghost Agent
# --------------------------
# Load or generate encryption key
if os.path.exists("key.key"):
    with open("key.key", "rb") as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open("key.key", "wb") as f:
        f.write(key)

cipher = Fernet(key)

# --------------------------
# Auto-tagging function
def auto_tag(note):
    tags = []
    keywords = {
        "idea": ["plan", "concept", "project", "idea"],
        "task": ["todo", "task", "do", "finish"],
        "secret": ["password", "hidden", "secret"]
    }
    for tag, words in keywords.items():
        for word in words:
            if word.lower() in note.lower():
                tags.append(f"#{tag}")
    return " ".join(tags)

# --------------------------
# Add note function
def add_note():
    note = input("Enter new note: ")
    tags = auto_tag(note)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = f"{timestamp} | {note} | {tags}"
    encrypted = cipher.encrypt(data.encode())
    with open("vault.txt", "ab") as f:
        f.write(encrypted + b"\n")
    print("✅ Note added with tags:", tags)

    # Ghost Agent reply
    try:
        agent_response = ghost_reply(note)
        print("👻 Ghost Agent:", agent_response)
    except Exception as e:
        print("⚠️ Ghost Agent error:", e)

# --------------------------
# Read notes
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

# --------------------------
# Search notes
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

# --------------------------
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
