import requests, json, getpass, time

auth_page_url='https://controller.shanghaitech.edu.cn:8445/PortalServer/customize/1478262836414/pc/auth.jsp'
auth_url="https://controller.shanghaitech.edu.cn:8445/PortalServer/Webauth/webAuthAction!login.action"
sleep_seconds=60

def login(username, password):
    session = requests.Session()
    session.get(auth_page_url)
    post_data={
      "userName": username,
      "password": password,
      "hasValidateCode": False,
      "validCode": "",
      "authLan": "zh_CN",
      "hasValidateNextUpdatePassword": "true",
      "rememberPwd": "false",
      "browserFlag": "zh",
      "hasCheckCode": False,
      "checkcode": "",
      "saveTime": "14",
      "autoLogin": "false",
      "userMac": "",
      "isBoardPage": False,
      "clientIp": "10.20.196.23"
    }
    response = session.post(auth_url, data=post_data)
    json_ = json.loads(response.text)
    if json_['success'] == True:
        print 'Network authentication succeeeds.'
        print 'Client ip: ' + json_['data']['ip']
        print 'Login time: ' + json_['data']['loginDate']
        return True
    else:
        print 'Network authentication fails.'
        print 'Remote reason: ' + json_['message']
        return False

def human_login():
    username = raw_input('Plese input username: ')
    password = getpass.getpass(prompt='Plese input password: ')
    return username, password

def controller():
    username, password = human_login()
    while True:
        if login(username, password):
            print 'Will check authentication again in ' + str(sleep_seconds) + ' seconds.'
            time.sleep(sleep_seconds)
            continue
        else:
            print 'Please try again.'
            username, password = human_login()

controller()
