from passlib.hash import sha512_crypt

def crack_password(shadow_file, wordlist):
    with open(shadow_file, "r") as f:
        for i in f:
            username, hash_val = i.strip().split(":")
            print(f"Cracking password for {username}")

            with open(wordlist, "r") as rf:
                for word in rf:
                    word = word.strip()

                    if sha512_crypt.verify(word, hash_val):
                        print(f"Password found for {username}: {word}")
                        break
                    else:
                        print(f"Password was incorrect for {username}: {word}")

crack_password("shadow.txt","wordlist.txt")
