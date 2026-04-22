portList = []

portList.append(21)
portList.append(51)
portList.append(11)
portList.append(91)
portList.append(443)

print(portList)

portList.pop(-1)
pos = portList.index(91)

print(str(pos))
portList.sort()
print(portList)
print(portList[::-1])
print(portList[:2])
print(portList[2:])


services = {'ftp': 21,
            'ssh':22,
            'smtp':25,
            'http':80
        }
print(services.keys())
print(services.items())
print(services['ftp'])


import socket
# s = socket.socket()

# socket.setdefaulttimeout(2)

# try:
#     s.connect(("192.168.95.148",21))
# except Exception as e:
#     print("[-] Error = " + str(e))
# ans = s.recv(1024)

def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip,port))
        banner = s.recv(1024).decode(errors="ignore")
        return banner
    except Exception as e:
        return None

def checkVulns(banner):
    if 'FreeFloat Ftp Server (Version 1.00)' in banner:
        print('[+] FreeFloat FTP Server is vulnerable.')
        return True
    else:
        return False

def iteration_example():
    portList = [21,22,25,80,110]
    for x in range(1,255):
        ip = "192.168.1.95." + str(x)
        for port in portList:
            print("[+] Checking 192.168.95." + str(x) + ": "+ str(port))
            retBanner(ip,port)


def main():
    ip1 = '192.168.95.148'
    ip2 = '192.168.95.149'
    port = 21
    
    banner1 = retBanner(ip1,port)
    banner2 = retBanner(ip2,port)

    if banner1:
        print('[+]' + ip1 + ': ' + banner1)
        checkVulns(banner1)
    if banner2:
        print('[+]' + ip2 + ': ' + banner2)
    
    if __name__ == '__main__':
        main()
