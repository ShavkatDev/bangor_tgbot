from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()
fernet = Fernet(os.getenv("FERNET_KEY").encode())

def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
