from passlib.hash import sha512_crypt

password = {
    "alice": "password123",
    "bob": "qwerty",
    "charlie": "letmein2004"
}

with open("shadow.txt", "w") as f:
    for user, passwd in password.items():
        hash_val = sha512_crypt.hash(passwd)
        f.write(f"{user}:{hash_val}\n")

print("Shadow File Created.")




