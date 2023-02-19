import urllib3
import urllib
import logging
import json
import webbrowser
import time

def dealWithLogin(url, pool):
    parsedUrl = urllib.parse.urlparse(url)
    if parsedUrl.netloc=="172.20.30.1":
        logging.info("DLUTEDA detected.")
        userip=urllib.parse.parse_qs(parsedUrl.query)["userip"][0]
        wlanacip=urllib.parse.parse_qs(parsedUrl.query)["wlanacip"][0]
        getssourl="http://172.20.30.1:801/eportal/portal/cas_auth/login?callback=dr1003&login_method=1&wlan_user_ip="+userip+"&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip="+wlanacip+"&wlan_ac_name=&authex_enable=&mac_type=1&jsVersion=4.X&v=2433&lang=zh"
        logging.info(getssourl)
        r = pool.request('GET', getssourl)
        jsonstr = r.data.decode()[7:-2]
        js = json.loads(jsonstr)
        print("Attention: If browser jumps to dashboard after starting, visit the link below in incognito mode:")
        print("注意：如果打开浏览器后跳转到面板而非登录页面，请在隐身模式下访问以下链接：")
        print(js["cas_login_uri"])
        time.sleep(5)
        webbrowser.open(js["cas_login_uri"])
        input()
    else:
        logging.info("Not in DLUTEDA, exiting...")

def main():
    retries = urllib3.Retry(connect=2, redirect=False)
    http = urllib3.PoolManager()
    r = http.request('GET', "http://baidu.com", retries=False)
    print(r.status)
    if r.status == 302:
        logging.info("Login need detected.")
        dealWithLogin(r.get_redirect_location(), http)
    if r.status == 200:
        logging.info("Seems no need to login, exiting...")

logging.basicConfig(level=logging.INFO, filename="log.txt")
main()
