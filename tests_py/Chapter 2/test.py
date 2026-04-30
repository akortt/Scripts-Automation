def clean_shadow(filename):
    users = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            # print(line)

            if not line: #empty
                continue 

            parts = line.split(":")
            if len(parts) != 4:
                continue
            # print(parts)

            username = parts[0].strip()
            hsh = parts[1].strip()
            uid = parts[2].strip()
            homedir = parts[3].strip()

            users[username] = {
                "uid": int(uid),
                "home": homedir,
                "hash": hsh
            }
        
    return(users)


users = clean_shadow("messy_shadow.txt")

for username, data in users.items():
    print(username + " " + str(data["uid"]))

# users.items() gives you key-value pair as a tuple
# E.g. ("alice", {"uid": 1001, "home": "/home/alice", "hash": "abc123"})
#         ↑                    ↑
#     username           user data (dict)