import httplib, urllib, re, string

server = None
cp_auth = False

def auth(username, password):
    if not server:
        raise ValueError("Server not set")
    
    response = do_post("/login.pl", {'username': username, 'password': password, 'login': 1, 'return': ''})
    
    auth_cookie = response.getheader('set-cookie', None)
    if auth_cookie:
        m = re.match('cp_auth=(.+); path=/', auth_cookie)
        if m:
            global cp_auth
            cp_auth = m.group(1)
            return True

    return False
    
def do_get(url, params={}):
    conn = httplib.HTTPConnection(server)
    headers = {}
    
    if cp_auth:
        headers['Cookie'] = 'cp_auth=%s' % cp_auth
        
    conn.request("POST", url + '?' + urllib.urlencode(params), headers=headers)
    return conn.getresponse()
    
def do_post(url, params):
    conn = httplib.HTTPConnection(server)
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    
    if cp_auth:
        headers['Cookie'] = 'cp_auth=%s' % cp_auth
        
    conn.request("POST", url, urllib.urlencode(params), headers)
    return conn.getresponse()
    
def _check_auth():
    if not server:
        raise ValueError("Server not set")
    elif not cp_auth:
        raise ValueError("Not authed")
    
def list_accounts():
    _check_auth()
    
    more_pages = True
    start = 0
    accounts = []
    
    while more_pages:
        response = do_post("/reselleraccounts.cp?start=%d" % start, {'page': 99})
        body = response.read()
        
        matches = re.findall(r'=(\w+)"><img src="/images/webfusion/list_(linux|windows)\.gif" align=middle border=0></a></td><td>([^<]+)<', body, re.S)
        for m in matches:
            accounts.append(m)
        
        more_pages = body.find('Next &gt;</a>') > -1
        start += 99
        
    return accounts

def create_acct(username, password, disk=None, mailboxes=None, responders=None, mra=None, transfer=None, cp=True, ssl=False, mysql=False, mssql=False, frontpage=True, ftp=True, stats=True, dns=False, platform='windows'):
    _check_auth()
        
    params = {
        'user': username,
        'pass': password,
        'confirm': password,
        'space': 'unlimited',
        'mailboxes': 'unlimited',
        'responders': 'unlimited',
        'mra': 'unlimited',
        'transfer': 'unlimited',
        'cp': 1 if cp else 0,
        'ssl': 1 if ssl else 0,
        'mysql': 1 if mysql else 0,
        'mssql': 1 if mssql else 0,
        'fp': 1 if frontpage else 0,
        'ftp': 1 if ftp else 0,
        'stats': 1 if stats else 0,
        'dns': 1 if dns else 0,
        'create': 2,
        'type': platform,
        'level': '',
    }
    
    if disk is not None:
        params['space'] = 'amount'
        params['space_value'] = disk
    if mailboxes is not None:
        params['mailboxes'] = 'amount'
        params['mailboxes_value'] = mailboxes
    if responders is not None:
        params['responders'] = 'amount'
        params['responders_value'] = responders
    if mra is not None:
        params['mra'] = 'amount'
        params['mra_value'] = mra
    if transfer is not None:
        params['transfer'] = 'amount'
        params['transfer_value'] = transfer
    
    response = do_post("/addaccount.cp", params)
    body = response.read()
    
    if string.find(body, "Your account was created successfully") > -1:
        return True, None
    else:
        m = re.search('<p class="message">(.+)</p> <p><a href="javascript', body, re.S)
        if m:
            return False, re.sub('\s{2,}', ' ', m.group(1))
        else:
            return False, None    
    
def add_domain(domain, account, regtype='domain'):
    _check_auth()
        
    params = {
        'domain': domain,
        'regtype': 'transfer' if regtype == 'domain' else 'subdomain',
        'map': account,
        'create': 1,
        'submit': 'Next',
    }
    
    response = do_post("/adddomain.cp", params)
    body = response.read()
    
    if string.find(body, "Your domain name was added successfully") > -1:
        return True, None
    else:
        m = re.search('<p class="message">(.+)</p> <p><a href="javascript', body, re.S)
        if m:
            return False, re.sub('\s{2,}', ' ', m.group(1))
        else:
            return False, None