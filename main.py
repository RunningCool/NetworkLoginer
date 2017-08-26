import requests, json, getpass, time, sys

auth_page_url='https://controller.shanghaitech.edu.cn:8445/PortalServer/customize/1478262836414/pc/auth.jsp'
auth_url="https://controller.shanghaitech.edu.cn:8445/PortalServer/Webauth/webAuthAction!login.action"
retry_seconds=10
heartbeat_seconds=60

class LoginResult:
    SUCCESS = 1
    NETWORK_FAILURE = 2
    AUTHENTICATION_FAILURE = 3

def login(username, password):
    session = requests.Session()
    try:
        session.get(auth_page_url)
    except Exception:
        print 'Connection fails.'
        return LoginResult.NETWORK_FAILURE
    post_data={
      "userName": username,
      "password": password,
      "hasValidateCode": False
    }
    try:
        response = session.post(auth_url, data=post_data)
    except Exception:
        print 'Connection fails.'
        return LoginResult.NETWORK_FAILURE
    json_ = json.loads(response.text)
    if json_['success'] == True:
        print 'Network authentication succeeeds.'
        print 'Client ip: ' + json_['data']['ip']
        print 'Login time: ' + json_['data']['loginDate']
        return LoginResult.SUCCESS
    else:
        print 'Network authentication fails.'
        print 'Remote reason: ' + json_['message']
        return LoginResult.AUTHENTICATION_FAILURE

def human_login():
    username = raw_input('Plese input username: ')
    password = getpass.getpass(prompt='Plese input password: ')
    return username, password

def controller():
    # print "This is the name of the script: ", sys.argv[0]
    if len(sys.argv) == 3:
        username = sys.argv[1]
        password = sys.argv[2]
    elif len(sys.argv) == 1:
        print 'Tips: run \'' + sys.argv[0] + ' username password\' next time to enable easy login.'
        username, password = human_login()
    else:
        print 'Invalid number of arguments.'
    while True:
        result = login(username, password)
        if result == LoginResult.SUCCESS:
            print 'Will check authentication again in ' + str(heartbeat_seconds) + ' seconds.'
            time.sleep(heartbeat_seconds)
            continue
        if result == LoginResult.NETWORK_FAILURE:
            print 'Will retry authentication in ' + str(retry_seconds) + ' seconds.'
            time.sleep(retry_seconds)
            continue
        else:
            print 'Please try again.'
            username, password = human_login()

controller()
