__FILENAME__ = gen_cacert
#!/usr/bin/env python
# Lib\site-packages\pip\_vendor\requests\cacert.pem

import base64, hashlib, re, sys
try: from OpenSSL import crypto
except ImportError: crypto = None

PY3 = sys.version_info[0] >= 3

print('read CA.crt')
with open('CA.crt', 'U') as fp:
    data = fp.read().strip()

if crypto:
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, data)
    issuer = cert.get_issuer(); subj = cert.get_subject()
    info = '''\
# Issuer: CN=%s O=%s OU=%s
# Subject: CN=%s O=%s OU=%s
# Label: "%s"
# Serial: %d''' % (issuer.CN, issuer.O, issuer.OU,
        subj.CN, subj.O, subj.OU, subj.CN, cert.get_serial_number())
else:
    info = '''\
# Issuer: CN=WallProxy CA O=WallProxy OU=WallProxy Root
# Subject: CN=WallProxy CA O=WallProxy OU=WallProxy Root
# Label: "WallProxy CA"
# Serial: 0'''

hexf = lambda s:':'.join('%02x'%i for i in bytearray(s))
d = re.compile(r'(?ms)BEGIN CERTIFICATE[^\n]+\n(.+?)\n[^\n]+END CERTIFICATE')
d = base64.b64decode(d.search(data).group(1))
data = '''%s
# MD5 Fingerprint: %s
# SHA1 Fingerprint: %s
# SHA256 Fingerprint: %s
%s
''' % (info,
       hexf(hashlib.md5(d).digest()),
       hexf(hashlib.sha1(d).digest()),
       hexf(hashlib.sha256(d).digest()),
       data)

print('write cacert.pem')
with open('cacert.pem', 'wb') as fp:
    fp.write(data.encode('latin-1') if PY3 else data)

########NEW FILE########
__FILENAME__ = make_config
# -*- coding: utf-8 -*-
from __future__ import with_statement

PUBLIC_APPIDS = '''
smartladder8|sandaojushi3|ftencentuck|baidufirefoxtieba|chromeichi|aitaiyokani|smartladder3|smartladder4|chrome360q|smartladder6|goagent-dup001|kawaiiushioplus|smartladdercanada|gongongid02|goagent-dup003|goagent-dup002|gonggongid03|ippotsukobeta|gonggongid01|gonggongid07|gonggongid06|kawaiiushionoserve|gonggongid04|kawaiiushio2|chromelucky|gonggongid09|yanlun001|smartladderchina|smartladder1|kawaiiushio1|kawaiiushio6|kawaiiushio7|saosaiko|kawaiiushio5|smartladderjapan|bakajing600|sekaiwakerei|yugongxisaiko|gonggongid08|smartladder2|baiduchrometieba|kawaiiushio4|gonggongid05|bakabaka300|fangbingxingtodie|f360uck|chromesaiko|chromeqq|kawaiiushio|ilovesmartladder|smartladder7|gongmin700|qq325862401|kawaiiushio8|smartladderkoera|gonggongid10|kawaiiushio9|smartladderuk|smartladderhongkong|chrometieba|flowerwakawaii|feijida600|window8saiko|gfwdies|smartladdertaiwan|akb48daisukilove|smartladderus|diaoyudaobelongtochinasaiko|jianiwoxiangni|freegoagent160|freegoagent198|freegoagent205|freegoagent292|freegoagent334|freegoagent358|freegoagent494|freegoagent526|freegoagent547|freegoagent553|freegoagent576|freegoagent577|freegoagent578|freegoagent583|freegoagent585|freegoagent586|freegoagent591|freegoagent599|freegoagent603|freegoagent607|freegoagent616|freegoagent623|freegoagent624|freegoagent625|freegoagent628|freegoagent631|freegoagent633|freegoagent638|freegoagent641|freegoagent644|freegoagent650|freegoagent654|freegoagent655|freegoagent657|freegoagent666|freegoagent670|freegoagent671|freegoagent674|freegoagent685|freegoagent686|freegoagent698|freegoagent699|freegoagent701|freegoagent702|freegoagent703|freegoagent707|freegoagent710|freegoagent718|freegoagent730|freegoagent734|freegoagent737|freegoagent742|freegoagent744|freegoagent746|freegoagent753|freegoagent758|freegoagent760|freegoagent762|freegoagent766|freegoagent771|freegoagent773|freegoagent774|freegoagent777|freegoagent780|freegoagent781|freegoagent784|freegoagent785|freegoagent786|freegoagent789|freegoagent791|freegoagent793|freegoagent794|freegoagent799|freegoagent802|freegoagent807|freegoagent809|freegoagent810|freegoagent811|freegoagent812|freegoagent813|freegoagent818|freegoagent822|freegoagent825|freegoagent827|freegoagent828|freegoagent830|freegoagent831|freegoagent832|freegoagent836|freegoagent837|freegoagent840|freegoagent847|freegoagent851|freegoagent852|freegoagent855|freegoagent859|freegoagent861|freegoagent863|freegoagent866|freegoagent867|freegoagent870|freegoagent872|freegoagent874|freegoagent875|freegoagent876|freegoagent877|freegoagent879|freegoagent881|freegoagent889|freegoagent894|freegoagent898|freegoagent900|freegoagent905|freegoagent909|freegoagent910|freegoagent914|freegoagent915|freegoagent919|freegoagent923|freegoagent926|freegoagent927|freegoagent928|freegoagent929|freegoagent932|freegoagent934|freegoagent945|freegoagent949|freegoagent950|freegoagent951|freegoagent954|freegoagent956|freegoagent957|freegoagent958|freegoagent963|freegoagent965|freegoagent966|freegoagent968|freegoagent971|freegoagent972|freegoagent973|freegoagent974|freegoagent975|freegoagent976|freegoagent978|freegoagent981|freegoagent987|freegoagent993|freegoagent994|freegoagent998
'''

import ConfigParser, os, re, urlparse, os.path as ospath, random
from cStringIO import StringIO

def rulefiles(v):
    v = v.strip()
    i = v.find('string://')
    if i < 0:
        return v.split('|')
    if i == 0:
        return [v.replace(r'\n', '\n')]
    return v[:i-1].split('|') + [v[i:].replace(r'\n', '\n')]

class Common(object):
    v = '''def %s(self, *a):
    try:
        return self.CONFIG.%s(*a[:-1])
    except:
        return a[-1]
'''
    for k in ('get', 'getint', 'getfloat', 'getboolean', 'items', 'remove_option'):
        exec(v % (k, k))
    del k, v

    def parse_pac_config(self):
        v = self.get('pac', 'py_default', '') or 'FORWARD'
        self.PY_DEFAULT = (v.split('|') * 3)[:3]
        if self.PAC_FILE:
            v = self.get('pac', 'default', '') or self._PAC_DEFAULT
            self.PAC_DEFAULT = (v.split('|') * 3)[:3]
        else:
            self.PAC_DEFAULT = self.PY_DEFAULT
        def get_rule_cfg(key, default):
            PAC_RULELIST = v = self.get('pac', key, default)
            if v.startswith('!'):
                if self.PAC_FILE:
                    v = self.items(v.lstrip('!').strip(), ())
                    v = [(rulefiles(v),k.upper()) for k,v in v if k and v]
                else:
                    v = self.items('py_'+v.lstrip('!').strip(), ())
                    sp = {'FORBID':'False', 'WEB':'None'}
                    v = [(rulefiles(v),sp.get(k.upper()) or k.upper()) for k,v in v if k and v]
                PAC_RULELIST = v
            elif v:
                TARGET_PAC = self.TARGET_PAAS
                if self.PAC_FILE:
                    TARGET_PAC = self.TARGET_LISTEN
                    if not TARGET_PAC:
                        TARGET_PAC = '*:*'
                    elif ':' not in TARGET_PAC:
                        TARGET_PAC = '*:' + TARGET_PAC
                    TARGET_PAC = 'PROXY %s;DIRECT' % TARGET_PAC
                PAC_RULELIST = [(rulefiles(v), TARGET_PAC)]
            return PAC_RULELIST
        self.PAC_RULELIST = get_rule_cfg('rulelist', '')
        self.PAC_IPLIST = get_rule_cfg('iplist', '')

    def __init__(self, INPUT):
        ConfigParser.RawConfigParser.OPTCRE = re.compile(r'(?P<option>[^=\s][^=]*)\s*(?P<vi>[=])\s*(?P<value>.*)$')
        CONFIG = self.CONFIG = ConfigParser.ConfigParser()
        for file in (INPUT, ospath.join(ospath.dirname(INPUT), 'user.ini')):
            try:
                CONFIG.read(file)
            except ConfigParser.MissingSectionHeaderError:
                with open(file, 'rb') as fp: v = fp.read()
                v = v[v.find('['):]
                try:
                    with open(file, 'wb') as fp: fp.write(v)
                except IOError:
                    pass
                CONFIG.readfp(StringIO(v), file)

        self.LISTEN_IP          = self.get('listen', 'ip', '0.0.0.0')
        self.LISTEN_PORT        = self.getint('listen', 'port', 8086)
        self.USERNAME           = self.get('listen', 'username', None)
        self.WEB_USERNAME       = self.get('listen', 'web_username', 'admin')
        self.WEB_PASSWORD       = self.get('listen', 'web_password', 'admin')
        self.WEB_AUTHLOCAL      = self.getboolean('listen', 'web_authlocal', False)
        if self.USERNAME is not None:
            self.PASSWORD       = self.get('listen', 'password', '')
            self.BASIC_AUTH     = self.getboolean('listen', 'basic_auth', True)
            self.DISABLE_SOCKS4 = self.getboolean('listen', 'disable_socks4', False)
            self.DISABLE_SOCKS5 = self.getboolean('listen', 'disable_socks5', False)
        self.CERT_WILDCARD      = self.getboolean('listen', 'cert_wildcard', True)
        self.TASKS_DELAY        = self.getint('listen', 'tasks_delay', 0)

        self.FETCH_KEEPALIVE    = self.getboolean('urlfetch', 'keep_alive', True)
        self.FETCH_TIMEOUT      = self.getfloat('urlfetch', 'timeout', -1)
        self.FORWARD_TIMEOUT    = self.getfloat('urlfetch', 'fwd_timeout', -1)
        self.FETCH_ARGS = v = {}
        k = self.getfloat('urlfetch', 'gae_timeout', -1)
        if k >= 0: v['timeout'] = k or None
        k = self.getint('urlfetch', 'gae_crlf', 0)
        if k > 0: v['crlf'] = k
        self.DEBUG_LEVEL        = self.getint('urlfetch', 'debug', -1)

        GAE_PROFILE = 'gae'; self.GAE_HANDLER = False
        self.GAE_ENABLE         = self.getboolean('gae', 'enable', CONFIG.has_section('gae'))
        if self.GAE_ENABLE:
            self.GAE_LISTEN     = self.get('gae', 'listen', '8087')
            if self.LISTEN_PORT == 8087 and self.GAE_LISTEN == '8087':
                self.LISTEN_PORT = 8086
            v = self.get('gae', 'appid', '').replace('.appspot.com', '')
            if not v or v == 'appid1|appid2':
                self.GAE_APPIDS = v = re.sub(r'\s+', '', PUBLIC_APPIDS).split('|')
                random.shuffle(v)
            else:
                self.GAE_APPIDS = v.split('|')
            self.GAE_PASSWORD   = self.get('gae', 'password', '')
            self.GAE_PATH       = self.get('gae', 'path', '/fetch.py')
            GAE_PROFILE         = self.get('gae', 'profile', GAE_PROFILE)
            self.GAE_MAXTHREADS = self.getint('gae', 'max_threads', 0)
            v = self.getint('gae', 'fetch_mode', 0)
            self.GAE_FETCHMOD   = 0 if v <= 0 else (2 if v >= 2 else 1)
            self.GAE_PROXY      = self.get('gae', 'proxy', 'default')
            self.GAE_HANDLER    = self.GAE_LISTEN and self.getboolean('gae', 'find_handler', True)

        self.PAAS_ENABLE        = self.getboolean('paas', 'enable', CONFIG.has_section('paas'))
        if self.PAAS_ENABLE:
            self.PAAS_LISTEN        = self.get('paas', 'listen', '')
            self.PAAS_PASSWORD      = self.get('paas', 'password', '')
            self.PAAS_FETCHSERVER   = CONFIG.get('paas', 'fetchserver').split('|')
            self.PAAS_PROXY         = self.get('paas', 'proxy', 'default')

        self.SOCKS5_ENABLE      = self.getboolean('socks5', 'enable', CONFIG.has_section('socks5'))
        if self.SOCKS5_ENABLE:
            self.SOCKS5_LISTEN      = self.get('socks5', 'listen', '')
            self.SOCKS5_PASSWORD    = self.get('socks5', 'password', '')
            self.SOCKS5_FETCHSERVER = CONFIG.get('socks5', 'fetchserver')
            self.SOCKS5_PROXY       = self.get('socks5', 'proxy', 'default')

        OLD_PLUGIN = []
        d = {'gaeproxy':'OGAE', 'forold':'OOLD', 'goagent':'OGA', 'simple':'OSP', 'simple2':'OSP2'}
        for k in d:
            if self.getboolean(k, 'enable', CONFIG.has_section(k)):
                url = self.get(k, 'url', '')
                if url: url = url.split('|')
                else:
                    url = self.get(k, 'appid', '')
                    if not url: continue
                    url = ['https://%s.appspot.com/%s.py' % (i,k) for i in url.split('|')]
                crypto = (self.get(k, 'crypto', '') + '|'*200).split('|')
                key = self.get(k, 'password', '').decode('string-escape')
                key = (key + ('|'+key)*200).split('|')
                proxy = [v.split(',') if ',' in v else v for v in (self.get(k, 'proxy', 'default')+'|'*200).split('|')]
                configs = []
                for url,crypto,key,proxy in zip(url,crypto,key,proxy):
                    config = {'url':url, 'key':key}
                    if crypto: config['crypto'] = crypto
                    if proxy == 'none':
                        config['proxy'] = None
                    elif proxy:
                        config['proxy'] = proxy
                    configs.append(config)
                for v in ('max_threads', 'range0', 'range'):
                    configs[0][v] = self.getint(k, v, 0)
                OLD_PLUGIN.append((d[k], k, configs, self.get(k, 'listen', '')))
        self.OLD_PLUGIN = OLD_PLUGIN or False

        self.TARGET_PAAS        = self.GAE_ENABLE and 'GAE' or self.PAAS_ENABLE and 'PAAS' or self.SOCKS5_ENABLE and 'SOCKS5' or self.OLD_PLUGIN and self.OLD_PLUGIN[0][0]
        self.TARGET_LISTEN = self.GAE_ENABLE and self.GAE_LISTEN or self.PAAS_ENABLE and self.PAAS_LISTEN or self.SOCKS5_ENABLE and self.SOCKS5_LISTEN or self.OLD_PLUGIN and self.OLD_PLUGIN[0][3]

        v = self.getint('proxy', 'enable', 0)
        self._PAC_DEFAULT = 'DIRECT'; self.GLOBAL_PROXY = None
        if v > 0:
            PROXIES = []
            for i in xrange(1,v+1):
                v = self.get('proxy', 'proxy%d'%i, '')
                if not v: break
                PROXIES.append(v)
            if not PROXIES:
                PROXY_HOST      = CONFIG.get('proxy', 'host')
                PROXY_PORT      = CONFIG.getint('proxy', 'port')
                PROXY_USERNAME  = self.get('proxy', 'username', '')
                PROXY_PASSWROD  = self.get('proxy', 'password', '')
                self._PAC_DEFAULT= 'PROXY %s:%s;DIRECT' % (PROXY_HOST, PROXY_PORT)
                if PROXY_USERNAME:
                    PROXY_HOST = '%s:%s@%s' % (PROXY_USERNAME, PROXY_PASSWROD, PROXY_HOST)
                PROXIES.append('http://%s:%s' % (PROXY_HOST, PROXY_PORT))
            self.GLOBAL_PROXY   = PROXIES[0] if len(PROXIES) == 1 else tuple(PROXIES)

        self.HTTPS_TARGET = {}
        if self.getboolean('forward', 'enable', CONFIG.has_section('forward')):
            self.remove_option('forward', 'enable', '')
            for k,v in self.items('forward', ()):
                self.HTTPS_TARGET[k.upper()] = '(%s)'%v if '"' in v or "'" in v else repr(v)

        self.PAC_ENABLE = self.getboolean('pac', 'enable', True)
        v = self.getint('pac', 'https_mode', 2)
        self.PAC_HTTPSMODE = 0 if v <= 0 else (2 if v >= 2 else 1)
        v = self.get('pac', 'file', '').replace('goagent', 'proxy')
        self.PAC_FILE = v and v.split('|')
        self.parse_pac_config()

        self.GOOGLE_MODE        = self.get(GAE_PROFILE, 'mode', 'http')
        v = self.get(GAE_PROFILE, 'hosts', '')
        self.GOOGLE_HOSTS       = ' '.join(v and tuple(v.split('|')) or ())
        v = self.get(GAE_PROFILE, 'sites', '')
        self.GOOGLE_SITES       = v and tuple(v.split('|')) or ()
        v = self.get(GAE_PROFILE, 'forcehttps', ''); v = v and v.split('|') or ()
        GOOGLE_FORCEHTTPS = [(i if '/' in i else ('http://%s/'%('*'+i if i.startswith('.') else i))) for i in v]
        v = self.get(GAE_PROFILE, 'noforcehttps', ''); v = v and v.split('|') or ()
        GOOGLE_FORCEHTTPS.extend(['@@%s'%(i if '/' in i else ('http://%s/'%('*'+i if i.startswith('.') else i))) for i in v])
        self.GOOGLE_FORCEHTTPS = ' \n '.join(GOOGLE_FORCEHTTPS)
        v = self.get(GAE_PROFILE, 'withgae', '')
        GOOGLE_WITHGAE          = v and tuple(v.split('|')) or ()
        self.TRUE_HTTPS = self.TARGET_PAAS and self.get(GAE_PROFILE, 'truehttps', '').replace('|', ' ').strip()
        self.NOTRUE_HTTPS = self.TRUE_HTTPS and self.get(GAE_PROFILE, 'notruehttps', '').replace('|', ' ').strip()

        self.FETCHMAX_LOCAL     = self.getint('fetchmax', 'local', 3)
        self.FETCHMAX_SERVER    = self.getint('fetchmax', 'server', 0)

        self.AUTORANGE_ENABLE   = self.getboolean('autorange', 'enable', False)
        def get_rules(opt, key, d=''):
            v = self.get(opt, key, d)
            if v.startswith('!'):
                v = v.lstrip('!').strip()
                return v and rulefiles(v)
            else:
                return v.replace(r'\n', '\n').strip()
        self.AUTORANGE_RULES = get_rules('autorange', 'rules')
        v = self.get('autorange', 'hosts', ''); v = v and v.split('|') or ()
        v = ' \n '.join([(i if '/' in i else ('||%s'%i.lstrip('.') if i.startswith('.') else 'http*://%s/'%i)) for i in v])
        if isinstance(self.AUTORANGE_RULES, list):
            self.AUTORANGE_RULES.append('string://' + v)
        elif v:
            self.AUTORANGE_RULES = ' \n '.join((v, self.AUTORANGE_RULES))
        self.AUTORANGE_MAXSIZE  = self.getint('autorange', 'maxsize', 1000000)
        self.AUTORANGE_WAITSIZE = self.getint('autorange', 'waitsize', 500000)
        self.AUTORANGE_BUFSIZE  = self.getint('autorange', 'bufsize', 8192)

        assert self.AUTORANGE_BUFSIZE <= self.AUTORANGE_WAITSIZE <= self.AUTORANGE_MAXSIZE

        self.REMOTE_DNS = self.DNS_RESOLVE = self.CRLF_RULES = self.HOSTS_RULES = ''; self.HOSTS = {}
        if self.getboolean('hosts', 'enable', CONFIG.has_section('hosts')):
            self.REMOTE_DNS = v = self.get('hosts', 'dns', '')
            if v: self.REMOTE_DNS = v if ',' in v else repr(v)
            self.DNS_RESOLVE = self.get('hosts', 'resolve', '').replace('|', ' ').strip()
            self.HOSTS_CRLF = self.getint('hosts', 'crlf', 0)
            self.CRLF_RULES = self.HOSTS_CRLF > 0 and get_rules('hosts', 'crlf_rules')
            self.HOSTS_RULES = self.TARGET_PAAS and get_rules('hosts', 'rules')
            for v in ('enable', 'rules', 'crlf', 'crlf_rules', 'dns', 'resolve'):
                self.remove_option('hosts', v, '')
            for k,v in self.items('hosts', ()):
                if v.startswith('profile:'):
                    v = self.get(GAE_PROFILE, v[8:], '')
                else:
                    m = re.match(r'\[(\w+)\](\w+)', v)
                    if m:
                        v = v.replace(m.group(0), self.get(m.group(1), m.group(2), ''))
                v = v.replace('|', ' ').strip()
                if k and v: self.HOSTS[k] = v

        self.THIRD_APPS = []
        if self.getboolean('third', 'enable', CONFIG.has_section('third')):
            self.remove_option('third', 'enable', '')
            self.THIRD_APPS = [(k,v if v[0] in ('"',"'") else repr(v)) for k,v in self.items('third', ()) if v]

        self.USERAGENT_STRING   = self.getboolean('useragent', 'enable', True) and self.get('useragent', 'string', '')
        self.USERAGENT_MATCH    = self.USERAGENT_STRING and self.get('useragent', 'match', '')
        self.USERAGENT_RULES    = self.USERAGENT_MATCH and get_rules('useragent', 'rules')
        self.FALLBACK_RULES     = self.TARGET_PAAS and get_rules('urlfetch', 'nofallback',
            r'/^https?:\/\/(?:[\w-]+|127(?:\.\d+){3}|10(?:\.\d+){3}|192\.168(?:\.\d+){2}|172\.[1-3]\d(?:\.\d+){2}|\[.+?\])(?::\d+)?\//')
        v = self.get('urlfetch', 'redirects', '')
        try:
            if v.startswith('!'):
                with open(ospath.join(ospath.dirname(INPUT), 'misc', v.lstrip('!').strip()), 'U') as fp:
                    v = fp.read()
            for p,r in eval(v): ''+p+r
            self.REDIRECT_RULES = '(%s)'%v
        except:
            self.REDIRECT_RULES = ''

        self.AUTORANGE_RULES    = (self.GAE_ENABLE or self.OLD_PLUGIN) and self.AUTORANGE_ENABLE and self.AUTORANGE_RULES
        self.PAC_ENABLE         = (self.PAC_RULELIST or self.PAC_IPLIST) and self.PAC_ENABLE and 'PAC_ENABLE'
        self.GOOGLE_WITHGAE     = False
        if self.TARGET_PAAS and self.GOOGLE_SITES and not self.GLOBAL_PROXY:
            self.GOOGLE_WITHGAE = ' \n '.join([(i if '/' in i else '||%s'%i.lstrip('.')) for i in GOOGLE_WITHGAE])
            v = ' \n '.join(['||%s'%i.lstrip('.') for i in self.GOOGLE_SITES])
            if isinstance(self.HOSTS_RULES, basestring):
                self.HOSTS_RULES = ' \n '.join((self.HOSTS_RULES, v))
            else:
                self.HOSTS_RULES.append('string://' + v)
        self.NEED_PAC           = self.GOOGLE_FORCEHTTPS or self.USERAGENT_RULES or self.FALLBACK_RULES or self.AUTORANGE_RULES or self.CRLF_RULES or self.HOSTS_RULES or self.GOOGLE_WITHGAE or self.PAC_ENABLE


def tob(s, enc='utf-8'):
    return s.encode(enc) if isinstance(s, unicode) else bytes(s)
def touni(s, enc='utf-8', err='strict'):
    return s.decode(enc, err) if isinstance(s, str) else unicode(s)

class SimpleTemplate(object):
    """SimpleTemplate from bottle"""
    blocks = ('if', 'elif', 'else', 'try', 'except', 'finally', 'for', 'while',
              'with', 'def', 'class')
    dedent_blocks = ('elif', 'else', 'except', 'finally')
    re_pytokens = re.compile(r'''
            (''(?!')|""(?!")|'{6}|"{6}    # Empty strings (all 4 types)
             |'(?:[^\\']|\\.)+?'          # Single quotes (')
             |"(?:[^\\"]|\\.)+?"          # Double quotes (")
             |'{3}(?:[^\\]|\\.|\n)+?'{3}  # Triple-quoted strings (')
             |"{3}(?:[^\\]|\\.|\n)+?"{3}  # Triple-quoted strings (")
             |\#.*                        # Comments
            )''', re.VERBOSE)

    def __init__(self, source, encoding='utf-8'):
        self.source = source
        self.encoding = encoding
        self._str = lambda x: touni(repr(x), encoding)
        self._escape = lambda x: touni(x, encoding)

    @classmethod
    def split_comment(cls, code):
        """ Removes comments (#...) from python code. """
        if '#' not in code: return code
        #: Remove comments only (leave quoted strings as they are)
        subf = lambda m: '' if m.group(0)[0]=='#' else m.group(0)
        return re.sub(cls.re_pytokens, subf, code)

    @property
    def co(self):
        # print self.code
        return compile(self.code, '<string>', 'exec')

    @property
    def code(self):
        stack = [] # Current Code indentation
        lineno = 0 # Current line of code
        ptrbuffer = [] # Buffer for printable strings and token tuple instances
        codebuffer = [] # Buffer for generated python code
        multiline = dedent = oneline = False
        template = self.source

        def yield_tokens(line):
            for i, part in enumerate(re.split(r'\{\{(.*?)\}\}', line)):
                if i % 2:
                    if part.startswith('!'): yield 'RAW', part[1:]
                    else: yield 'CMD', part
                else: yield 'TXT', part

        def flush(): # Flush the ptrbuffer
            if not ptrbuffer: return
            cline = ''
            for line in ptrbuffer:
                for token, value in line:
                    if token == 'TXT': cline += repr(value)
                    elif token == 'RAW': cline += '_str(%s)' % value
                    elif token == 'CMD': cline += '_escape(%s)' % value
                    cline +=  ', '
                cline = cline[:-2] + '\\\n'
            cline = cline[:-2]
            if cline[:-1].endswith('\\\\\\\\\\n'):
                cline = cline[:-7] + cline[-1] # 'nobr\\\\\n' --> 'nobr'
            cline = '_printlist([' + cline + '])'
            del ptrbuffer[:] # Do this before calling code() again
            code(cline)

        def code(stmt):
            for line in stmt.splitlines():
                codebuffer.append('  ' * len(stack) + line.strip())

        for line in template.splitlines(True):
            lineno += 1
            line = touni(line, self.encoding)
            sline = line.lstrip()
            if lineno <= 2:
                m = re.match(r"%\s*#.*coding[:=]\s*([-\w.]+)", sline)
                if m: self.encoding = m.group(1)
                if m: line = line.replace('coding','coding (removed)')
            if sline and sline[0] == '%' and sline[:2] != '%%':
                line = line.split('%',1)[1].lstrip() # Full line following the %
                cline = self.split_comment(line).strip()
                cmd = re.split(r'[^a-zA-Z0-9_]', cline)[0]
                flush() # You are actually reading this? Good luck, it's a mess :)
                if cmd in self.blocks or multiline:
                    cmd = multiline or cmd
                    dedent = cmd in self.dedent_blocks # "else:"
                    if dedent and not oneline and not multiline:
                        cmd = stack.pop()
                    code(line)
                    oneline = not cline.endswith(':') # "if 1: pass"
                    multiline = cmd if cline.endswith('\\') else False
                    if not oneline and not multiline:
                        stack.append(cmd)
                elif cmd == 'end' and stack:
                    code('#end(%s) %s' % (stack.pop(), line.strip()[3:]))
                else:
                    code(line)
            else: # Line starting with text (not '%') or '%%' (escaped)
                if line.strip().startswith('%%'):
                    line = line.replace('%%', '%', 1)
                ptrbuffer.append(yield_tokens(line))
        flush()
        return '\n'.join(codebuffer) + '\n'

    def execute(self, _stdout, *args, **kwargs):
        for dictarg in args: kwargs.update(dictarg)
        env = {}
        env.update({'_stdout': _stdout, '_printlist': _stdout.extend,
               '_str': self._str, '_escape': self._escape, 'get': env.get,
               'setdefault': env.setdefault, 'defined': env.__contains__})
        env.update(kwargs)
        eval(self.co, env)
        return env

    def render(self, *args, **kwargs):
        """ Render the template using keyword arguments as local variables. """
        for dictarg in args: kwargs.update(dictarg)
        stdout = []
        self.execute(stdout, kwargs)
        return ''.join(stdout)


template = r"""# -*- coding: utf-8 -*-
# 是否使用ini作为配置文件，0不使用
ini_config = {{MTIME}}
# 监听ip
listen_ip = '{{LISTEN_IP}}'
# 监听端口
listen_port = {{LISTEN_PORT}}
# 是否使用通配符证书
cert_wildcard = {{int(CERT_WILDCARD)}}
# 更新PAC时也许还没联网，等待tasks_delay秒后才开始更新
tasks_delay = {{!TASKS_DELAY}}
# WEB界面是否对本机也要求认证
web_authlocal = {{int(WEB_AUTHLOCAL)}}
# 登录WEB界面的用户名
web_username = {{!WEB_USERNAME}}
# 登录WEB界面的密码
web_password = {{!WEB_PASSWORD}}
# 全局代理
global_proxy = {{!GLOBAL_PROXY}}
# URLFetch参数
fetch_keepalive = {{int(FETCH_KEEPALIVE)}}
%if FETCH_TIMEOUT >= 0:
fetch_timeout = {{!FETCH_TIMEOUT or None}}
%end
%if FORWARD_TIMEOUT >= 0:
forward_timeout = {{!FORWARD_TIMEOUT or None}}
%end
%if DEBUG_LEVEL >= 0:
debuglevel = {{!DEBUG_LEVEL}}
%end
check_update = 0

def config():
    Forward, set_dns, set_resolve, set_hosts, check_auth, redirect_https = import_from('util')
%for k,v in HTTPS_TARGET.iteritems():
    {{k}} = Forward({{v}})
%HTTPS_TARGET[k] = k
%end
    RAW_FORWARD = FORWARD = Forward()
%if REMOTE_DNS:
    set_dns({{REMOTE_DNS}})
%end
%if DNS_RESOLVE:
    set_resolve({{!DNS_RESOLVE}})
%end
    google_sites = {{!GOOGLE_SITES}}
    google_hosts = {{!GOOGLE_HOSTS}}
    set_hosts(google_sites, google_hosts)
%for k,v in HOSTS.iteritems():
%if k and v:
    set_hosts({{!k}}, {{repr(v) if v != GOOGLE_HOSTS else 'google_hosts'}})
%end
%end

    from plugins import misc; misc = install('misc', misc)
    PAGE = misc.Page('page.html')
%if REDIRECT_RULES:
    redirect_rules = misc.Redirects({{REDIRECT_RULES}})
%end
%HTTPS_TARGET.update({'FORWARD':'FORWARD', 'RAW_FORWARD':'RAW_FORWARD', 'False':'False', 'None':'None','PAGE':'None'})
%if TARGET_PAAS:

    from plugins import paas; paas = install('paas', paas)
%end #TARGET_PAAS
%if GAE_ENABLE:
%HTTPS_TARGET['GAE'] = 'None'
    GAE = paas.GAE(appids={{!GAE_APPIDS}}\\
%if GAE_LISTEN:
, listen={{!GAE_LISTEN}}\\
%end
%if GAE_PASSWORD:
, password={{!GAE_PASSWORD}}\\
%end
%if GAE_PATH:
, path={{!GAE_PATH}}\\
%end
%if GOOGLE_MODE == 'https':
, scheme='https'\\
%end
%if GAE_PROXY != 'default':
, proxy={{!GAE_PROXY}}\\
%end
, hosts=google_hosts\\
%if AUTORANGE_MAXSIZE and AUTORANGE_MAXSIZE != 1000000:
, maxsize={{!AUTORANGE_MAXSIZE}}\\
%end
%if AUTORANGE_WAITSIZE and AUTORANGE_WAITSIZE != 500000:
, waitsize={{!AUTORANGE_WAITSIZE}}\\
%end
%if AUTORANGE_BUFSIZE and AUTORANGE_BUFSIZE != 8192:
, bufsize={{!AUTORANGE_BUFSIZE}}\\
%end
%if FETCHMAX_LOCAL and FETCHMAX_LOCAL != 3:
, local_times={{!FETCHMAX_LOCAL}}\\
%end
%if FETCHMAX_SERVER and FETCHMAX_SERVER != 3:
, server_times={{!FETCHMAX_SERVER}}\\
%end
%if GAE_MAXTHREADS:
, max_threads={{!GAE_MAXTHREADS}}\\
%end
%if GAE_FETCHMOD:
, fetch_mode={{!GAE_FETCHMOD}}\\
%end
%if FETCH_ARGS:
, fetch_args={{!FETCH_ARGS}}\\
%end
)
%end #GAE_ENABLE
%if PAAS_ENABLE:
%HTTPS_TARGET['PAAS'] = 'None'
%for i,k in enumerate(PAAS_FETCHSERVER):
    PAAS{{i+1 if len(PAAS_FETCHSERVER) > 1 else ''}} = paas.PAAS(url={{!k}}\\
%if PAAS_LISTEN and i == 0:
, listen={{!PAAS_LISTEN}}\\
%end
%if PAAS_PASSWORD:
, password={{!PAAS_PASSWORD}}\\
%end
%if PAAS_PROXY != 'default':
, proxy={{!PAAS_PROXY}}\\
%end
%if FETCH_ARGS:
, fetch_args={{!FETCH_ARGS}}\\
%end
)
%end
%if len(PAAS_FETCHSERVER) > 1:
%k = ['PAAS%d'%i for i in xrange(1, len(PAAS_FETCHSERVER)+1)]
%HTTPS_TARGET.update(dict.fromkeys(k,'None'))
    PAASS = ({{', '.join(k)}})
    from random import choice
    PAAS = lambda req: choice(PAASS)(req)
    server = paas.data.get('PAAS_server')
    if server:
        def find_handler(req):
            if req.proxy_type.endswith('http'):
                return PAAS
        server.find_handler = find_handler
%end
%end #PAAS_ENABLE
%if SOCKS5_ENABLE:
%HTTPS_TARGET['SOCKS5'] = 'SOCKS5'
    SOCKS5 = paas.SOCKS5(url={{!SOCKS5_FETCHSERVER}}\\
%if SOCKS5_LISTEN:
, listen={{!SOCKS5_LISTEN}}\\
%end
%if SOCKS5_PASSWORD:
, password={{!SOCKS5_PASSWORD}}\\
%end
%if SOCKS5_PROXY != 'default':
, proxy={{!SOCKS5_PROXY}}\\
%end
)
%end #SOCKS5_ENABLE
%if OLD_PLUGIN:
    from old import old; old = install('old', old)
%for n,k,c,p in OLD_PLUGIN:
    {{n}} = old.{{k}}({{!c}}, {{!p}})
%HTTPS_TARGET[n] = 'None'
%end
%end #OLD_PLUGIN
%if NEED_PAC:

    PacFile, RuleList, HostList = import_from('pac')
    def apnic_parser(data):
        from re import findall
        return '\n'.join(findall(r'(?i)\|cn\|ipv4\|((?:\d+\.){3}\d+\|\d+)\|', data))
%PAC_IPLIST = [('[%s]'%(', '.join(('(%r, apnic_parser)'%i) if 'delegated-apnic-latest' in i else repr(i) for i in v)),t) for v,t in PAC_IPLIST]
%end #NEED_PAC
%if GOOGLE_FORCEHTTPS:
    forcehttps_sites = RuleList({{!GOOGLE_FORCEHTTPS}})
%end
%if AUTORANGE_RULES:
    autorange_rules = RuleList({{!AUTORANGE_RULES}})
%if GAE_ENABLE:
    _GAE = GAE; GAE = lambda req: _GAE(req, autorange_rules.match(req.url, req.proxy_host[0]))
%end
%if OLD_PLUGIN:
%for n,k,c,p in OLD_PLUGIN:
    _{{n}} = {{n}}; {{n}} = lambda req: _{{n}}(req, autorange_rules.match(req.url, req.proxy_host[0]))
%end
%end #OLD_PLUGIN
%end
%if USERAGENT_RULES:
    import re; useragent_match = re.compile({{!USERAGENT_MATCH}}).search
    useragent_rules = RuleList({{!USERAGENT_RULES}})
%end
%if GOOGLE_WITHGAE:
    withgae_sites = RuleList({{!GOOGLE_WITHGAE}})
%end #GOOGLE_WITHGAE
%if TRUE_HTTPS:
%if NOTRUE_HTTPS:
    notruehttps_sites = HostList({{!NOTRUE_HTTPS}})
%end
    truehttps_sites = HostList({{!TRUE_HTTPS}})
%end #TRUE_HTTPS
%if CRLF_RULES:
    crlf_rules = RuleList({{!CRLF_RULES}})
%end #CRLF_RULES
%if HOSTS_RULES:
    hosts_rules = RuleList({{!HOSTS_RULES}})
%end #HOSTS_RULES
    unparse_netloc = import_from('utils')
    def build_fake_url(scheme, host):
        if scheme == 'https' and host[1] != 80 or host[1] % 1000 == 443:
            scheme, dport = 'https', 443
        else: scheme, dport = 'http', 80
        return '%s://%s/' % (scheme, unparse_netloc(host, dport))
%if TARGET_PAAS:
    _HttpsFallback = ({{TARGET_PAAS}},)
%if FALLBACK_RULES:
    nofallback_rules = RuleList({{!FALLBACK_RULES}})
    def FORWARD(req):
        if req.proxy_type.endswith('http'):
            if nofallback_rules.match(req.url, req.proxy_host[0]):
                return RAW_FORWARD(req)
            return RAW_FORWARD(req, {{TARGET_PAAS}})
        url = build_fake_url(req.proxy_type, req.proxy_host)
        if nofallback_rules.match(url, req.proxy_host[0]):
            return RAW_FORWARD(req)
        return RAW_FORWARD(req, _HttpsFallback)
%else:
    def FORWARD(req):
        if req.proxy_type.endswith('http'):
            return RAW_FORWARD(req, {{TARGET_PAAS}})
        return RAW_FORWARD(req, _HttpsFallback)
%end
%end
%PY_DEFAULT = (([v for v in PY_DEFAULT if v in HTTPS_TARGET] or ['FORWARD']) * 3)[:3]
%if PAC_ENABLE:
%if PAC_FILE:
%NEED_PAC = NEED_PAC != 'PAC_ENABLE'

    rulelist = (
%for k,v in PAC_RULELIST:
        ({{!k}}, {{!v}}),
%end #PAC_RULELIST
    )
    iplist = (
%for k,v in PAC_IPLIST:
        ({{k}}, {{!v}}),
%end #PAC_IPLIST
    )
    PacFile(rulelist, iplist, {{!PAC_FILE}}, {{!PAC_DEFAULT}})
%else:
%PAC_DEFAULT = PY_DEFAULT
%PAC_RULELIST = [(k,v) for k,v in PAC_RULELIST if v in HTTPS_TARGET]
%PAC_IPLIST = [(k,v) for k,v in PAC_IPLIST if v in HTTPS_TARGET]
%PAC_ENABLE = PAC_RULELIST or PAC_IPLIST
%NEED_PAC = NEED_PAC != 'PAC_ENABLE' or PAC_ENABLE
%if PAC_RULELIST:

    rulelist = (
%for k,v in PAC_RULELIST:
        (RuleList({{!k}}), {{v}}),
%end #PAC_RULELIST
    )
%if PAC_HTTPSMODE == 2:
    httpslist = (
%for i,k in enumerate(PAC_RULELIST):
        (rulelist[{{i}}][0], {{HTTPS_TARGET[k[1]]}}),
%end #PAC_RULELIST
    )
%end #PAC_HTTPSMODE
%end #PAC_RULELIST
%if PAC_IPLIST:
    IpList, makeIpFinder = import_from('pac')
    iplist = (
%for k,v in PAC_IPLIST:
        (IpList({{k}}), {{v}}),
%end #PAC_IPLIST
    )
    findHttpProxyByIpList = makeIpFinder(iplist, [{{', '.join(PAC_DEFAULT)}}])
    findHttpsProxyByIpList = makeIpFinder(iplist, [{{', '.join([HTTPS_TARGET[v] for v in PAC_DEFAULT])}}])
%end #PAC_IPLIST
%end #PAC_FILE
%end #PAC_ENABLE
%if THIRD_APPS:

    from plugins import third; third = install('third', third)
%for k,v in THIRD_APPS:
    third.run({{v}}) #{{k}}
%end
%end

%if USERNAME:
    auth_checker = check_auth({{!USERNAME}}, {{!PASSWORD}}\\
%if DISABLE_SOCKS4:
, socks4=False\\
%end
%if DISABLE_SOCKS5 and not SOCKS5_ENABLE:
, socks5=False\\
%end
%if BASIC_AUTH:
, digest=False\\
%end
)
%end #USERNAME
%if GAE_ENABLE:
%if GAE_HANDLER:
%if USERNAME:
    @auth_checker
%end
    def find_gae_handler(req):
        proxy_type = req.proxy_type
        host, port = req.proxy_host
        if proxy_type.endswith('http'):
            url = req.url
%if USERAGENT_RULES:
            if useragent_match(req.headers.get('User-Agent','')) and useragent_rules.match(url, host):
                req.headers['User-Agent'] = {{!USERAGENT_STRING}}
%end
%if GOOGLE_WITHGAE:
            if withgae_sites.match(url, host):
                return GAE
%end
%if GOOGLE_FORCEHTTPS:
            needhttps = req.scheme == 'http' and forcehttps_sites.match(url, host) and req.content_length == 0
            if needhttps and getattr(req, '_r', '') != url:
                req._r = url
                return redirect_https
%end
%if REDIRECT_RULES:
            handler = redirect_rules(req)
            if handler: return handler
%end
%if CRLF_RULES:
            if crlf_rules.match(url, host):
                req.crlf = {{HOSTS_CRLF}}
                return FORWARD
%end
%if HOSTS_RULES:
            if \\
%if GOOGLE_FORCEHTTPS:
not needhttps and \\
%end
hosts_rules.match(url, host):
                return FORWARD
%end
            return GAE
%if TRUE_HTTPS:
%if NOTRUE_HTTPS:
        if notruehttps_sites.match(host): return
%end
        if truehttps_sites.match(host): return FORWARD
%end
%else:
    def find_gae_handler(req):
        if req.proxy_type.endswith('http'): return GAE
%end #GAE_HANDLER
    paas.data['GAE_server'].find_handler = find_gae_handler

%end #GAE_ENABLE
%if USERNAME:
    @auth_checker
%end
    def find_proxy_handler(req):
%if TARGET_PAAS or NEED_PAC:
        proxy_type = req.proxy_type
        host, port = req.proxy_host
        if proxy_type.endswith('http'):
            url = req.url
%if USERAGENT_RULES:
            if useragent_match(req.headers.get('User-Agent','')) and useragent_rules.match(url, host):
                req.headers['User-Agent'] = {{!USERAGENT_STRING}}
%end
%if GOOGLE_WITHGAE:
            if withgae_sites.match(url, host):
                return {{TARGET_PAAS}}
%end
%if GOOGLE_FORCEHTTPS:
            needhttps = req.scheme == 'http' and forcehttps_sites.match(url, host) and req.content_length == 0
            if needhttps and getattr(req, '_r', '') != url:
                req._r = url
                return redirect_https
%end
%if REDIRECT_RULES:
            handler = redirect_rules(req)
            if handler: return handler
%end
%if CRLF_RULES:
            if crlf_rules.match(url, host):
                req.crlf = {{HOSTS_CRLF}}
                return FORWARD
%end
%if HOSTS_RULES:
            if \\
%if GOOGLE_FORCEHTTPS:
not needhttps and \\
%end
hosts_rules.match(url, host):
                return FORWARD
%end
%if PAC_ENABLE and not PAC_FILE:
%if PAC_RULELIST:
            for rule,target in rulelist:
                if rule.match(url, host):
                    return target
%end
%if PAC_IPLIST:
            return findHttpProxyByIpList(host)
%else:
            return {{PY_DEFAULT[0]}}
%end
%elif TARGET_PAAS:
            return {{TARGET_PAAS}}
%else:
            return FORWARD
%end
%if TRUE_HTTPS:
%if NOTRUE_HTTPS:
        if notruehttps_sites.match(host): return
%end
        if truehttps_sites.match(host): return FORWARD
%end
%if PAC_ENABLE and not PAC_FILE and PAC_HTTPSMODE == 2:
%if PAC_RULELIST:
        url = build_fake_url(proxy_type, (host, port))
        for rule,target in httpslist:
            if rule.match(url, host):
                return target
%end
%if PAC_IPLIST:
        return findHttpsProxyByIpList(host)
%else:
        return {{HTTPS_TARGET[PY_DEFAULT[0]]}}
%end
%elif PAC_HTTPSMODE == 0:
        return {{HTTPS_TARGET[PY_DEFAULT[0]]}}
%end
%else:
        return FORWARD
%end
    return find_proxy_handler
"""

def make_config(INPUT=None, OUTPUT=None):
    if not (INPUT and OUTPUT):
        if INPUT:
            OUTPUT = ospath.join(ospath.dirname(INPUT), 'config.py')
        elif OUTPUT:
            INPUT = ospath.join(ospath.dirname(OUTPUT), 'proxy.ini')
        else:
            if globals().get('__loader__'):
                DIR = ospath.dirname(__loader__.archive)
            else:
                DIR = ospath.dirname(__file__)
            INPUT = ospath.join(DIR, 'proxy.ini')
            OUTPUT = ospath.join(DIR, 'config.py')
    config = Common(INPUT).__dict__
    # from pprint import pprint
    # pprint(config)
    config['MTIME'] = 1 #int(os.stat(INPUT).st_mtime)
    code = SimpleTemplate(template).render(**config)
    # print code
    return tob(code), OUTPUT

if __name__ == '__main__':
    code, OUTPUT = make_config()
    with open(OUTPUT, 'wb') as fp:
        fp.write(code)

########NEW FILE########
__FILENAME__ = old
# -*- coding: utf-8 -*-

def old():
    import_from, global_proxy = config.import_from(config)

    # ================================ util.crypto =================================
    import hashlib, itertools

    class XOR:
        '''XOR with pure Python in case no PyCrypto'''
        def __init__(self, key):
            self.key = key

        def encrypt(self, data):
            xorsize = 1024
            key = itertools.cycle(map(ord, self.key))
            dr = xrange(0, len(data), xorsize)
            ss = [None] * len(dr)
            for i,j in enumerate(dr):
                dd = [ord(d)^k for d,k in itertools.izip(data[j:j+xorsize], key)]
                ss[i] = ''.join(map(chr, dd))
            return ''.join(ss)
        decrypt = encrypt

    class NUL:
        def encrypt(self, data):
            return data
        decrypt = encrypt

    class Crypto:
        _BlockSize = {'AES':16, 'ARC2':8, 'ARC4':1, 'Blowfish':8, 'CAST':8,
                      'DES':8, 'DES3':8, 'IDEA':8, 'RC5':8, 'XOR':1}
        _Modes = ['ECB', 'CBC', 'CFB', 'OFB', 'PGP'] #CTR needs 4 args
        _KeySize = {'AES':[16,24,32], 'CAST':xrange(5,17),
                    'DES':[8], 'DES3':[16,24], 'IDEA':[16]}

        def __init__(self, mode='AES-CBC-32'):
            mode = mode.split('-')
            mode += [''] * (3 - len(mode))
            #check cipher
            self.cipher = mode[0] if mode[0] else 'AES'
            if self.cipher not in self._BlockSize:
                raise ValueError('Invalid cipher: '+self.cipher)
            #check ciphermode
            if self._BlockSize[self.cipher] == 1:
                self.ciphermode = ''
            else:
                self.ciphermode = mode[1] if mode[1] in self._Modes else 'CBC'
            #check keysize
            try:
                self.keysize = int(mode[2])
            except ValueError:
                self.keysize = 32
            if self.keysize != 0:
                if self.cipher in self._KeySize:
                    keysize = self._KeySize[self.cipher]
                    if self.keysize not in keysize:
                        self.keysize = keysize[-1]
            #avoid Memmory Error
            if self.cipher=='RC5' and self.keysize in (1, 57): self.keysize=32
            #try to import Crypto.Cipher.xxxx
            try:
                cipherlib = __import__('Crypto.Cipher.'+self.cipher, fromlist='x')
                self._newobj = cipherlib.new
                if self._BlockSize[self.cipher] != 1:
                    self._ciphermode = getattr(cipherlib, 'MODE_'+self.ciphermode)
            except ImportError:
                if self.cipher == 'XOR': self._newobj = XOR
                else: raise

        def paddata(self, data):
            blocksize = self._BlockSize[self.cipher]
            if blocksize != 1:
                padlen = (blocksize - len(data) - 1) % blocksize
                data = '%s%s%s' % (chr(padlen), ' '*padlen, data)
            return data

        def unpaddata(self, data):
            if self._BlockSize[self.cipher] != 1:
                padlen = ord(data[0])
                data = data[padlen+1:]
            return data

        def getcrypto(self, key):
            if self.keysize==0 and key=='':
                return NUL()
            khash = hashlib.sha512(key).digest()
            if self.keysize != 0:
                key = khash[:self.keysize]
            blocksize = self._BlockSize[self.cipher]
            if blocksize == 1:
                return self._newobj(key)
            return self._newobj(key, self._ciphermode, khash[-blocksize:])

        def encrypt(self, data, key):
            crypto = self.getcrypto(key)
            data = self.paddata(data)
            return crypto.encrypt(data)

        def decrypt(self, data, key):
            crypto = self.getcrypto(key)
            data = crypto.decrypt(data)
            return self.unpaddata(data)

        def getmode(self):
            return '%s-%s-%d' % (self.cipher, self.ciphermode, self.keysize)

        def __str__(self):
            return '%s("%s")' % (self.__class__, self.getmode())

        def getsize(self, size):
            blocksize = self._BlockSize[self.cipher]
            return (size + blocksize - 1) // blocksize * blocksize

    class Crypto2(Crypto):
        def paddata(self, data):
            blocksize = self._BlockSize[self.cipher]
            if blocksize != 1:
                padlen = (blocksize - len(data) - 1) % blocksize
                data = '%s%s%s' % (data, ' '*padlen, chr(padlen))
            return data

        def unpaddata(self, data):
            if self._BlockSize[self.cipher] != 1:
                padlen = ord(data[-1])
                data = data[:-(padlen+1)]
            return data

    # =============================== plugins._base ================================
    HeaderDict, Proxy, URLInfo, del_bad_hosts, start_new_server, unparse_netloc = import_from(utils)
    import time, re, random, threading, socket, os, traceback

    class Handler(object):
        _dirty_headers = ('Connection', 'Proxy-Connection', 'Proxy-Authorization',
                         'Content-Length', 'Host', 'Vary', 'Via', 'X-Forwarded-For')
        _range_re = re.compile(r'(\d+)?-(\d+)?')
        _crange_re = re.compile(r'bytes\s+(\d+)-(\d+)/(\d+)')
        crypto = Crypto('XOR--32'); key = ''
        proxy = global_proxy
        headers = HeaderDict('Content-Type: application/octet-stream')
        range0 = 100000; range = 500000; max_threads = 10

        def __init__(self, config):
            dic = {'crypto': Crypto, 'key': lambda v:v, 'headers': HeaderDict,
                   'proxy': lambda v:global_proxy if v=='default' else Proxy(v),
                   'range0': lambda v:v if v>=10000 else self.__class__.range0,
                   'range': lambda v:v if v>=100000 else self.__class__.range,
                   'max_threads': lambda v:v if v>0 else self.__class__.max_threads,}
            self.url = URLInfo(config['url'])
            for k,v in dic.iteritems():
                if k in config:
                    setattr(self.__class__, k, v(config[k]))
                setattr(self, k, getattr(self.__class__, k))

        def __str__(self):
            return ' %s %s %d %d %d' % (self.url.url, self.crypto.getmode(),
                    self.range0, self.range, self.max_threads)

        def dump_data(self, data):
            raise NotImplementedError

        def load_data(self, data):
            raise NotImplementedError

        def process_request(self, req, force_range):
            data, headers = req.read_body(), req.headers
            for k in self._dirty_headers:
                del headers[k]
            if req.command == 'GET':
                rawrange, range = self._process_range(req.headers)
                if force_range:
                    headers['Range'] = range
            else:
                rawrange, range = '', ''
            request = {'url':req.url, 'method':req.command,
                       'headers':headers, 'payload':data, 'range':range}
            return request, rawrange

        def _process_range(self, headers):
            range = headers.get('Range', '')
            m = self._range_re.search(range)
            if m:
                m = m.groups()
                if m[0] is None:
                    if m[1] is None: m = None
                    else:
                        m = 1, int(m[1])
                        if m[1] > self.range0: range = 'bytes=-1024'
                else:
                    if m[1] is None:
                        m = 0, int(m[0])
                        range = 'bytes=%d-%d' % (m[1], m[1]+self.range0-1)
                    else:
                        m = 2, int(m[0]), int(m[1])
                        if m[2]-m[1]+1 > self.range0:
                            range = 'bytes=%d-%d' % (m[1], m[1]+self.range0-1)
            if m is None:
                range = 'bytes=0-%d' % (self.range0 - 1)
            return m, range

        def _fetch(self, data):
            data = self.crypto.encrypt(data, self.key)
            url = self.url
            opener = self.proxy.get_opener(url)
            try:
                resp = opener.open(url, data, 'POST', self.headers, 0)
            except Exception, e:
                return -1, e
            if resp.status != 200:
                opener.close()
                return -1, '%s: %s' % (resp.status, resp.reason)
            return 0, resp

        def fetch(self, data):
            raise NotImplementedError

        def read_data(self, type, data):
            if type == 1: return data
            resp, crypto = data
            data = self.crypto.unpaddata(crypto.decrypt(resp.read()))
            resp.close()
            return data

        def write_data(self, req, type, data):
            sendall = req.socket.sendall
            if type == 1:
                sendall(data)
            else:
                resp, crypto = data
                size = self.crypto.getsize(16384)
                data = crypto.decrypt(resp.read(size))
                sendall(self.crypto.unpaddata(data))
                data = resp.read(size)
                while data:
                    sendall(crypto.decrypt(data))
                    data = resp.read(size)
                resp.close()

        def _need_range_fetch(self, req, res, range):
            headers = res[2]
            m = self._crange_re.search(headers.get('Content-Range', ''))
            if not m: return None
            m = map(int, m.groups())#bytes %d-%d/%d
            if range is None:
                start=0; end=m[2]-1
                code = 200
                del headers['Content-Range']
            else:
                if range[0] == 0: #bytes=%d-
                    start=range[1]; end=m[2]-1
                elif range[0] == 1: #bytes=-%d
                    start=m[2]-range[1]; end=m[2]-1
                else: #bytes=%d-%d
                    start=range[1]; end=range[2]
                code = 206
                headers['Content-Range'] = 'bytes %d-%d/%d' % (start, end, m[2])
            headers['Content-Length'] = str(end-start+1)
            req.start_response(code, headers)
            if start == m[0]: #Valid
                self.write_data(req, res[0], res[3])
                start = m[1] + 1
            return start, end

        def range_fetch(self, req, handler, request, start, end):
            t = time.time()
            if self._range_fetch(req, handler, request, start, end):
                t = time.time() - t
                t = (end - start + 1) / 1000.0 / t
                print '>>>>>>>>>> Range Fetch ended (all @ %sKB/s)' % t
            else:
                req.close_connection = 1
                print '>>>>>>>>>> Range Fetch failed'

        def _range_fetch(self, req, handler, request, start, end):
            request['range'] = '' # disable server auto-range-fetch
            i, s, thread_size, tasks = 0, start, 10, []
            while s <= end:
                e = s + (i < thread_size and self.range0 or self.range) - 1
                if e > end: e = end
                tasks.append((i, s, e))
                i += 1; s = e + 1
            task_size = len(tasks)
            thread_size = min(task_size, len(handler)*2, self.max_threads)
            print ('>>>>>>>>>> Range Fetch started: threads=%d blocks=%d '
                    'bytes=%d-%d' % (thread_size, task_size, start, end))
            if thread_size == 1:
                return self._single_fetch(req, handler, request, tasks)
            handler = list(handler); random.shuffle(handler)
            if thread_size > len(handler): handler *= 2
            results = [None] * task_size
            mutex = threading.Lock()
            threads = {}
            for i in xrange(thread_size):
                t = threading.Thread(target=handler[i]._range_thread,
                        args=(request, tasks, results, threads, mutex))
                threads[t] = set()
                t.setDaemon(True)
            for t in threads: t.start()
            i = 0; t = False
            while i < task_size:
                if results[i] is not None:
                    try:
                        self.write_data(req, 1, results[i])
                        results[i] = None
                        i += 1
                        continue
                    except:
                        mutex.acquire()
                        del tasks[:]
                        mutex.release()
                        break
                if not threads: #All threads failed
                    if t: break
                    t = True; continue
                time.sleep(1)
            else:
                return True
            return False

        def _single_fetch(self, req, handler, request, tasks):
            try:
                for task in tasks:
                    request['headers']['Range'] = 'bytes=%d-%d' % task[1:]
                    data = self.dump_data(request)
                    for i in xrange(3):
                        self = random.choice(handler)
                        res = self.fetch(data)
                        if res[0] == -1:
                            time.sleep(2)
                        elif res[1] == 206:
                            #print res[2]
                            print '>>>>>>>>>> block=%d bytes=%d-%d' % task
                            self.write_data(req, res[0], res[3])
                            break
                    else:
                        raise StopIteration('Failed')
            except:
                return False
            return True

        def _range_thread(self, request, tasks, results, threads, mutex):
            ct = threading.current_thread()
            while True:
                mutex.acquire()
                try:
                    if threads[ct].intersection(*threads.itervalues()):
                        raise StopIteration('All threads failed')
                    for i,task in enumerate(tasks):
                        if task[0] not in threads[ct]:
                            task = tasks.pop(i)
                            break
                    else:
                        raise StopIteration('No task for me')
                    request['headers']['Range'] = 'bytes=%d-%d' % task[1:]
                    data = self.dump_data(request)
                except StopIteration, e:
                    #print '>>>>>>>>>> %s: %s' % (ct.name, e)
                    del threads[ct]
                    break
                finally:
                    mutex.release()
                success = False
                for i in xrange(2):
                    res = self.fetch(data)
                    if res[0] == -1:
                        time.sleep(2)
                    elif res[1] == 206:
                        try: data = self.read_data(res[0], res[3])
                        except: continue
                        if len(data) == task[2]-task[1]+1:
                            success = True
                            break
                mutex.acquire()
                if success:
                    print '>>>>>>>>>> block=%d bytes=%d-%d'%task, len(data)
                    results[task[0]] = data
                else:
                    threads[ct].add(task[0])
                    tasks.append(task)
                    tasks.sort(key=lambda x: x[0])
                mutex.release()

        def handle(self, handler, req, force_range):
            req.handler_name = handler[0].handler_name
            if len(handler) == 1:
                handlers = handler[0], handler[0]
            else:
                handlers = random.sample(handler, 2)
            request, range = self.process_request(req, force_range)
            data = self.dump_data(request)
            errors = []
            for self in handlers:
                res = self.fetch(data)
                if res[0] != -1: break
                e = res[1]; es = str(e); errors.append(es)
                if not es.startswith('Server: '): del_bad_hosts()
            else:
                return req.send_error(502, str(errors))
            if res[1]==206 and req.command=='GET':
                data = self._need_range_fetch(req, res, range)
                if data:
                    start, end = data
                    if start > end: return #end
                    return self.range_fetch(req, handler, request, start, end)
            req.start_response(res[1], res[2])
            self.write_data(req, res[0], res[3])

    def _base_init(cls, config, listen=None):
        name = cls.handler_name
        print 'Initializing %s for old version.' % name
        server = [None] * len(config)
        for i,v in enumerate(config):
            if isinstance(v, basestring):
                v = {'url': v}
            try:
                server[i] = cls(v)
                print server[i]
            except:
                traceback.print_exc()
        def handler(req, force_range=False):
            return server[0].handle(server, req, force_range)
        if listen:
            def find_handler(req):
                if req.proxy_type.endswith('http'):
                    return handler
            listen = data['%s_server'%name] = start_new_server(listen, find_handler)
            print ' %s listen on: %s' % (name, unparse_netloc(listen.server_address[:2]))
        return handler

    # ============================== plugins.gaeproxy ==============================
    import zlib, struct, cPickle as pickle

    class GAEHandler(Handler):
        handler_name = 'OGAE'
        def dump_data(self, data):
            return zlib.compress(pickle.dumps(data, 1))

        def load_data(self, data):
            return pickle.loads(data)

        def process_request(self, req, force_range):
            data, headers = req.read_body(), req.headers
            for k in self._dirty_headers:
                del headers[k]
            if req.command == 'GET':
                rawrange, range = self._process_range(req.headers)
                if force_range:
                    headers['Range'] = range
            else:
                rawrange, range = '', ''
            request = {'url':req.url, 'method':req.command, 'payload':data,
                       'headers':headers.__getstate__(), 'range':range}
            return request, rawrange

        def fetch(self, data):
            data, resp = self._fetch(data)
            if data == -1: return data, resp
            crypto = self.crypto.getcrypto(self.key)
            headers = HeaderDict()
            try:
                raw_data = resp.read(7)
                zip, code, hlen = struct.unpack('>BHI', raw_data)
                if zip == 1:
                    data = self.crypto.unpaddata(crypto.decrypt(resp.read()))
                    data = zlib.decompress(data)
                    content = data[hlen:]
                    if code == 555:
                        raise ValueError('Server: '+content)
                    headers.__setstate__(self.load_data(data[:hlen]))
                    resp.close()
                    return 1, code, headers, content
                elif zip == 0:
                    h = crypto.decrypt(resp.read(hlen))
                    headers.__setstate__(self.load_data(self.crypto.unpaddata(h)))
                    if code == 555:
                        content = crypto.decrypt(resp.read())
                        raise ValueError('Server: '+self.crypto.unpaddata(content))
                    return 0, code, headers, (resp, crypto)
                else:
                    raw_data += resp.read()
                    raise ValueError('Data format not match(%s:%s)'%(self.url.url, raw_data))
            except Exception, e:
                resp.close()
                return -1, e

    def gaeproxy(*a, **kw):
        return _base_init(GAEHandler, *a, **kw)

    # =============================== plugins.forold ===============================
    class OldHandler(Handler):
        handler_name = 'OOLD'
        crypto = Crypto2('XOR--32')

        _unquote_map = {'0':'\x10', '1':'=', '2':'&'}
        def _quote(self, s):
            return str(s).replace('\x10', '\x100').replace('=','\x101').replace('&','\x102')
        def dump_data(self, dic):
            return zlib.compress('&'.join('%s=%s' % (self._quote(k),
                    self._quote(v)) for k,v in dic.iteritems()))
        def _unquote(self, s):
            res = s.split('\x10')
            for i in xrange(1, len(res)):
                item = res[i]
                try:
                    res[i] = self._unquote_map[item[0]] + item[1:]
                except KeyError:
                    res[i] = '\x10' + item
            return ''.join(res)
        def load_data(self, qs):
            pairs = qs.split('&')
            dic = {}
            for name_value in pairs:
                if not name_value:
                    continue
                nv = name_value.split('=', 1)
                if len(nv) != 2:
                    continue
                if len(nv[1]):
                    dic[self._unquote(nv[0])] = self._unquote(nv[1])
            return dic

        def __init__(self, config):
            if 'crypto' in config:
                self.__class__.crypto = Crypto2(config.pop('crypto'))
            Handler.__init__(self, config)

        def fetch(self, data):
            data, resp = self._fetch(data)
            if data == -1: return data, resp
            try:
                raw_data = resp.read(); resp.close()
                data = self.crypto.decrypt(raw_data, self.key)
                if data[0] == '0':
                    data = data[1:]
                elif data[0] == '1':
                    data = zlib.decompress(data[1:])
                else:
                    return -1, 'Data format not match(%s:%s)' % (self.url.url,raw_data)
                code, hlen, clen = struct.unpack('>3I', data[:12])
                if len(data) != 12+hlen+clen:
                    return -1, 'Data length not match'
                content = data[12+hlen:]
                if code == 555:     #Urlfetch Failed
                    return -1, 'Server: '+content
                headers = HeaderDict(self.load_data(data[12:12+hlen]))
                return 1, code, headers, content
            except Exception, e:
                return -1, e

    def forold(*a, **kw):
        return _base_init(OldHandler, *a, **kw)

    # =============================== plugins.goagent ==============================
    from binascii import a2b_hex, b2a_hex

    class GAHandler(OldHandler):
        handler_name = 'OGA'
        crypto = Crypto('XOR--0'); key = ''
    
        def dump_data(self, dic):
            return zlib.compress('&'.join('%s=%s' % (k,b2a_hex(str(v))) for k,v in dic.iteritems()))
    
        def load_data(self, qs):
            return dict((k,a2b_hex(v)) for k,v in (x.split('=') for x in qs.split('&')))
    
        def __init__(self, config):
            config.pop('crypto', None)
            self.password = config.pop('key', '')
            OldHandler.__init__(self, config)
    
        def process_request(self, req, force_range):
            request, rawrange = OldHandler.process_request(self, req, force_range)
            request['password'] = self.password
            return request, rawrange

    def goagent(*a, **kw):
        return _base_init(GAHandler, *a, **kw)

    # =============================== plugins.simple ===============================
    class SPHandler(GAEHandler):
        handler_name = 'OSP'
        def dump_data(self, dic):
            return zlib.compress('&'.join('%s=%s' % (k,b2a_hex(str(v))) for k,v in dic.iteritems()))

        def load_data(self, qs):
            return dict((k,a2b_hex(v)) for k,v in (x.split('=') for x in qs.split('&'))) if qs else {}

        process_request = Handler.process_request

    def simple(*a, **kw):
        return _base_init(SPHandler, *a, **kw)

    # =============================== plugins.simple2 ==============================
    import marshal

    class SP2Handler(Handler):
        handler_name = 'OSP2'
        def dump_data(self, data):
            return marshal.dumps(tuple((k,str(v)) for k,v in data.iteritems()))

        def load_data(self, data):
            return dict(marshal.loads(data))

        def fetch(self, data):
            data, resp = self._fetch(data)
            if data == -1: return data, resp
            crypto = self.crypto.getcrypto(self.key)
            try:
                raw_data = resp.read(7)
                mix, code, hlen = struct.unpack('>BHI', raw_data)
                if mix == 0:
                    headers = self.crypto.unpaddata(crypto.decrypt(resp.read(hlen)))
                    if code == 555:
                        content = self.crypto.unpaddata(crypto.decrypt(resp.read()))
                        raise ValueError('Server: '+content)
                    headers = HeaderDict(headers)
                    return 0, code, headers, (resp, crypto)
                elif mix == 1:
                    data = self.crypto.unpaddata(crypto.decrypt(resp.read()))
                    content = data[hlen:]
                    if code == 555:
                        raise ValueError('Server: '+content)
                    headers = HeaderDict(data[:hlen])
                    resp.close()
                    return 1, code, headers, content
                else:
                    raw_data += resp.read()
                    raise ValueError('Data format not match(%s:%s)'%(self.url.url, raw_data))
            except Exception, e:
                resp.close()
                return -1, e

    def simple2(*a, **kw):
        return _base_init(SP2Handler, *a, **kw)

    # ==============================================================================
    globals().update(gaeproxy=gaeproxy, forold=forold, 
        goagent=goagent, simple=simple, simple2=simple2)

########NEW FILE########
__FILENAME__ = plugins
# -*- coding: utf-8 -*-
from __future__ import with_statement

def paas():
    # this part is compatible with goagent 1.1.0 by phus.lu@gmail.com and others
    print 'Initializing PAAS for proxy based on cloud service.'
    set_hosts, Forward = config.import_from('util')
    HeaderDict, Proxy, URLInfo, unparse_netloc, del_bad_hosts = config.import_from(utils)
    import re, zlib, socket, struct, time, random, threading
    from binascii import a2b_hex, b2a_hex
    from base64 import b64encode
    try:
        import ssl
    except ImportError:
        ssl = None

    class HTTPError(Exception):
        #noinspection PyMissingConstructor
        def __init__(self, code, msg):
            self.code = code
            self.msg = msg

        def __str__(self):
            return 'HTTP Error %s: %s' % (self.code, self.msg)

    _range_re = re.compile(r'(\d+)?-(\d+)?')
    _crange_re = re.compile(r'bytes\s+(\d+)-(\d+)/(\d+)')
    def _process_range(headers, max_range):
        range = headers.get('Range', '')
        m = _range_re.search(range)
        if m:
            m = m.groups()
            if m[0]:
                max_range -= 1
                if m[1]:
                    m = 2, int(m[0]), int(m[1])
                    if m[2] - m[1] > max_range:
                        range = 'bytes=%d-%d' % (m[1], m[1] + max_range)
                else:
                    m = 0, int(m[0])
                    range = 'bytes=%d-%d' % (m[1], m[1] + max_range)
            else:
                if m[1]:
                    m = 1, int(m[1])
                    if m[1] > max_range:
                        range = 'bytes=-1024'
                else:
                    m = None,
                    range = 'bytes=0-%d' % (max_range - 1)
        else:
            m = None,
            range = 'bytes=0-%d' % (max_range - 1)
        return m, range

    _setcookie_re = re.compile(r', ([^ =]+(?:=|$))')
    def _fix_setcookie(headers):
        hdr = headers.get('Set-Cookie')
        if hdr:
            headers['Set-Cookie'] = _setcookie_re.sub(r'\r\nSet-Cookie: \1', hdr)
        return headers

    def GAE(**kw):
        self = _GAEHandler
        v = kw.get('appids', '')
        self.appids = v = v.split() if isinstance(v, str) else list(v)
        if not v: raise ValueError('no appids specified')
        scheme = kw.get('scheme', 'http').lower()
        if scheme not in ('http', 'https'):
            raise ValueError('invalid scheme: '+scheme)
        self.url = URLInfo('%s://%s.appspot.com%s?' % (
            scheme, self.appids[0], kw.get('path', '/fetch.py')))
        self.password = kw.get('password', '')
        v = kw.get('proxy', 'default')
        self.proxy = config.global_proxy if v == 'default' else Proxy(v)
        v = kw.get('hosts')
        if v: v = v.split() if isinstance(v, str) else list(v)
        if not v:
            v = ('eJxdztsNgDAMQ9GNIvIoSXZjeApSqc3nUVT3ZojakFTR47wSNEhB8qXhorXg+kM'
                 'jckGtQM9efDKf91Km4W+N4M1CldNIYMu+qSVoTm7MsG5E4KPd8apInNUUMo4bet'
                 'RQjg==').decode('base64').decode('zlib').split('|')
        set_hosts('.appspot.com', v, 0)
        if self.proxy.value:
            self.hosts = v
            self.proxy = self.proxy.new_hosts((v[0], self.url.port))
        self.headers = HeaderDict(kw.get('headers',
            'Content-Type: application/octet-stream'))
        v = kw.get('max_threads', 0)
        self.max_threads = min(10 if v <= 0 else v, len(self.appids))
        self.bufsize = kw.get('bufsize', 8192)
        self.maxsize = kw.get('maxsize', 1000000)
        self.waitsize = kw.get('waitsize', 500000)
        assert self.bufsize <= self.waitsize <= self.maxsize
        self.local_times = kw.get('local_times', 3)
        self.server_times = kw.get('server_times')
        self.fetch_mode = kw.get('fetch_mode', 0)
        self.fetch_args = kw.get('fetch_args', {})
        print '  Init GAE with appids: %s' % '|'.join(self.appids)
        print '  max_threads when range fetch: %d' % self.max_threads
        v = kw.get('listen')
        if v:
            def find_handler(req):
                if req.proxy_type.endswith('http'):
                    return self
            v = data['GAE_server'] = utils.start_new_server(v, find_handler)
            print '  GAE listen on: %s' % unparse_netloc(v.server_address[:2])
        return self

    class GAEHandler(object):
        skip_headers = frozenset(['Proxy-Connection', 'Content-Length', 'Host',
            'Vary', 'Via', 'X-Forwarded-For', 'X-ProxyUser-IP'])

        def build_params(self, req, force_range):
            method = req.command; headers = req.headers
            if method == 'GET':
                req.rangeinfo, range = _process_range(headers, self.maxsize)
                if force_range or req.rangeinfo[0] == 0:
                    headers['Range'] = range
            else:
                req.rangeinfo, range = (None,), ''
            skip_headers = self.skip_headers
            headers.data = dict(kv for kv in headers.iteritems()
                if kv[0] not in skip_headers)
            params = {'url':req.url, 'method':method,
                'headers':headers, 'payload':req.read_body()}
            if range:
                params['range'] = range
            if self.password:
                params['password'] = self.password
            if self.server_times:
                params['fetchmax'] = self.server_times
            return params, dict(self.fetch_args, proxy_auth=req.userid)

        def fetch(self, (params, fetch_args), server=None):
            params = zlib.compress('&'.join(['%s=%s' % (k, b2a_hex(str(v)))
                for k,v in params.iteritems()]), 9)
            errors = []
            url = server or self.url
            opener = self.proxy.get_opener(url, fetch_args)
            ti = si = 0; tend = self.local_times; send = len(self.appids)
            while ti < tend and si < send:
                flag = 0
                try:
                    resp = opener.open(url, params, 'POST', self.headers, 0)
                    if resp.status != 200:
                        resp.close()
                        raise HTTPError(resp.status, resp.reason)
                except Exception, e:
                    opener.close()
                    if isinstance(e, HTTPError):
                        errors.append(str(e))
                        if e.code in (503, 404, 403):
                            if e.code == 503:
                                errors[-1] = 'Bandwidth Over Quota(%s)'%self.appids[0]
                            else:
                                errors[-1] = '%s(%s)'%(errors[-1],self.appids[0])
                                if self.proxy.value:
                                    self.hosts.append(self.hosts.pop(0)); flag |= 2
                                    print 'GAE: switch host to %s' % self.hosts[0]
                                else:
                                    del_bad_hosts()
                            ti -= 1
                            if server:
                                url = self.url; server.__init__(url); server = None
                            else:
                                si += 1
                                self.appids.append(self.appids.pop(0)); flag |= 1
                                url.hostname = '%s.appspot.com' % self.appids[0]
                                print 'GAE: switch appid to %s' % self.appids[0]
                        elif e.code == 502:
                            if url.scheme != 'https':
                                ti -= 1
                                url.scheme = 'https'; url.port = 443; flag |= 3
                                print 'GAE: switch scheme to https'
                    elif isinstance(e, socket.error):
                        k = e.args[0]
                        if url.scheme != 'https' and k in (10054, 54, 20054, 104):
                            ti -= 1
                            url.scheme = 'https'; url.port = 443; flag |= 3
                            print 'GAE: switch scheme to https'
                        elif self.proxy.value:
                            errors.append('Connect other proxy failed: %s' % e)
                            self.hosts.append(self.hosts.pop(0)); flag |= 2
                            print 'GAE: switch host to %s' % self.hosts[0]
                        else:
                            errors.append('Connect fetchserver failed: %s' % e)
                            if del_bad_hosts() and k in (10054, 54, 20054, 104, 10047): ti -= 1
                    else:
                        errors.append('Connect fetchserver failed: %s' % e)
                    if flag & 1:
                        url.rebuild()
                    if flag & 2:
                        if self.proxy.value:
                            self.proxy = self.proxy.new_hosts(
                                (self.hosts[0], url.port))
                        opener = self.proxy.get_opener(url, fetch_args)
                else:
                    try:
                        flag = resp.read(1)
                        if flag == '0':
                            code, hlen, clen = struct.unpack('>3I', resp.read(12))
                            headers = HeaderDict([(k, a2b_hex(v))
                                for k,_,v in (x.partition('=')
                                for x in resp.read(hlen).split('&'))])
                            if self.fetch_mode == 1 or (code == 206 and self.fetch_mode == 2):
                                resp = resp.read()
                        elif flag == '1':
                            rawdata = zlib.decompress(resp.read()); resp.close()
                            code, hlen, clen = struct.unpack('>3I', rawdata[:12])
                            headers = HeaderDict([(k, a2b_hex(v))
                                for k,_,v in (x.partition('=')
                                for x in rawdata[12:12+hlen].split('&'))])
                            resp = rawdata[12+hlen:12+hlen+clen]
                        else:
                            raise ValueError('Data format not match(%s)' % url)
                        headers.setdefault('Content-Length', str(clen))
                        return 0, (code, headers, resp)
                    except Exception, e:
                        errors.append(str(e))
                ti += 1
            return -1, errors

        def write_content(self, req, resp, first=False):
            sendall = req.socket.sendall
            if isinstance(resp, str):
                sendall(resp)
            else:
                bufsize = self.bufsize
                data = resp.read(self.waitsize if first else bufsize)
                while data:
                    sendall(data)
                    data = resp.read(bufsize)
                resp.close()

        def need_range_fetch(self, req, headers, resp):
            m = _crange_re.search(headers.get('Content-Range', ''))
            if not m: return None
            m = map(int, m.groups())#bytes %d-%d/%d
            info = req.rangeinfo
            t = info[0]
            if t is None:
                start = 0; end = m[2]; code = 200
                del headers['Content-Range']
            else:
                #noinspection PySimplifyBooleanCheck
                if t == 0: #bytes=%d-
                    start = info[1]; end = m[2]
                elif t == 1: #bytes=-%d
                    start = m[2] - info[1]; end = m[2]
                else: #bytes=%d-%d
                    start = info[1]; end = info[2] + 1
                code = 206
                headers['Content-Range'] = 'bytes %d-%d/%d' % (start, end-1, m[2])
            headers['Content-Length'] = str(end - start)
            req.start_response(code, _fix_setcookie(headers))
            if start == m[0]: #Valid
                return [start, end, m[1] + 1, resp]
            return [start, end, start, None]

        def range_fetch(self, req, params, data):
            params[0].pop('range', None) # disable server auto-range-fetch
            length = data[1] - data[0]
            if self.max_threads > 1 and data[1] - data[2] > self.maxsize:
                handle = self._thread_range
            else:
                handle = self._single_range
            t = time.time()
            if handle(req, params, data):
                t = length / 1000.0 / ((time.time() - t) or 0.0001)
                print '>>>>>>>>>> Range Fetch ended (all @ %sKB/s)' % t
            else:
                req.close_connection = True
                print '>>>>>>>>>> Range Fetch failed'

        #noinspection PyUnboundLocalVariable,PyUnusedLocal
        def _single_range(self, req, params, data):
            start0, end, start, resp = data; del data[:]
            end -= 1; step = self.maxsize; failed = 0; iheaders = params[0]['headers']
            print ('>>>>>>>>>> Range Fetch started%s: bytes=%d-%d, step=%d'
                % (req.proxy_host, start0, end, step))
            if resp:
                self.write_content(req, resp, True)
            while start <= end:
                if failed > 16: return False
                iheaders['Range'] = 'bytes=%d-%d' % (start, min(start+step, end))
                flag, data = self.fetch(params)
                if flag != -1:
                    code, headers, resp = data
                    m = _crange_re.search(headers.get('Content-Range', ''))
                if flag == -1 or code >= 400:
                    failed += 1
                    seconds = random.randint(2*failed, 2*(failed+1))
                    time.sleep(seconds)
                elif 'Location' in headers:
                    failed += 1
                    params[0]['url'] = headers['Location']
                elif not m:
                    failed += 1
                else:
                    print '>>>>>>>>>> %s' % headers['Content-Range']
                    failed = 0
                    self.write_content(req, resp)
                    start = int(m.group(2)) + 1
            return True

        def _thread_range(self, req, params, info):
            tasks, task_size, info, write_content = \
                self._start_thread_range(req, params, info)
            i = 0
            while i < task_size:
                if info[1]: #All threads failed
                    print '>>>>>>>>>> failed@%d bytes=%d-%d' % tuple(info[1][2:5])
                    return False
                task = tasks[i]
                if not isinstance(task[0], int):
                    if task[0]:
                        write_content(task[0], task)
                    i += 1
                    continue
                time.sleep(0.001)
            return True

        def _start_thread_range(self, req, params, info):
            task0, end, start, resp = info; del info[:]
            s = self.maxsize; t = s - 1; tasks = []; i = 1
            while start < end:
                tasks.append([0, set(), i, start, start+t])
                start += s; i += 1
            end -= 1; tasks[-1][-1] = end
            task_size = len(tasks)
            thread_size = min(task_size, self.max_threads)
            lock = threading.Lock(); wlock = threading.Lock()
            info = [1, None, thread_size]
            def write_content(resp, task):
                #noinspection PyBroadException
                try:
                    buf = None
                    if info[0] != task[2] or not wlock.acquire(0):
                        buf = []
                        data = resp.read(8192)
                        while data:
                            buf.append(data)
                            if info[0] == task[2] and wlock.acquire(0):
                                break
                            data = resp.read(8192)
                        else:
                            resp.close()
                            lock.acquire(); task[0] = ''.join(buf); lock.release()
                            return
                    try:
                        info[0] += 1
                        print '>>>>>>>>>> block=%d bytes=%d-%d' % tuple(task[2:5])
                        if buf: req.socket.sendall(''.join(buf))
                        self.write_content(req, resp)
                        task[0] = None
                    finally:
                        wlock.release()
                except:
                    lock.acquire(); del tasks[:]; info[1] = task; lock.release()
            # appids = random.sample(self.appids, thread_size)
            appids = self.appids[1:]; random.shuffle(appids)
            appids.append(self.appids[0]); appids = appids[:thread_size]
            print ('>>>>>>>>>> Range Fetch started: threads=%d blocks=%d '
                'bytes=%d-%d appids=%s' % (thread_size, task_size, task0, end,
                '|'.join(appids)))
            task0 = 0, (), 0, task0, tasks[0][3] - 1
            #noinspection PyBroadException
            try:
                with wlock:
                    for i in xrange(thread_size):
                        t = threading.Thread(target=self._range_thread, args=(
                            appids[i], params, tasks, lock, info, write_content))
                        t.setDaemon(True)
                        t.start()
                    if resp:
                        print '>>>>>>>>>> block=%d bytes=%d-%d' % task0[2:5]
                        self.write_content(req, resp, True)
            except:
                lock.acquire(); del tasks[:]; info[1] = task0; lock.release()
            return tasks, task_size, info, write_content

        def _range_thread(self, server, params, tasks, lock, info, write_content):
            server = URLInfo(self.url, hostname='%s.appspot.com' % server)
            ct = params[0].copy()
            ct['headers'] = headers = HeaderDict(ct['headers'])
            params = ct, params[1]
            ct = threading.current_thread()
            while 1:
                with lock:
                    try:
                        for task in tasks:
                            #noinspection PySimplifyBooleanCheck
                            if task[0] == 0:
                                failed = task[1]
                                if len(failed) == info[2]:
                                    failed.clear()
                                if ct not in failed:
                                    task[0] = 1
                                    break
                        else:
                            for task in tasks:
                                task[1].discard(ct)
                            info[2] -= 1
                            raise StopIteration('No task for me')
                    except StopIteration:
                        break
                headers['Range'] = 'bytes=%d-%d' % (task[3], task[4])
                while 1:
                    if not tasks: return
                    flag, resp = self.fetch(params, server)
                    if not tasks: return
                    if flag != -1 and resp[0] == 206:
                        resp = resp[2]
                        if isinstance(resp, str):
                            lock.acquire(); task[0] = resp; lock.release()
                        else:
                            write_content(resp, task)
                        break
                    with lock:
                        if task[0] >= 2:
                            failed.add(ct); task[0] = 0; break
                        task[0] += 1

        def __call__(self, req, force_range=False):
            req.handler_name = 'GAE'
            params = self.build_params(req, force_range)
            flag, data = self.fetch(params)
            if flag == -1:
                return req.send_error(502, str(data))
            code, headers, resp = data
            if code == 206 and req.command == 'GET':
                data = self.need_range_fetch(req, headers, resp)
                if data:
                    del code, headers, resp
                    return self.range_fetch(req, params, data)
            req.start_response(code, _fix_setcookie(headers))
            self.write_content(req, resp)

    _GAEHandler = GAEHandler()

    def PAAS(**kw):
        self = PAASHandler()
        self.url = url = URLInfo(kw['url'])
        self.password = kw.get('password', '')
        v = kw.get('proxy', 'default')
        self.proxy = config.global_proxy if v == 'default' else Proxy(v)
        self.hosts = None
        v = kw.get('hosts')
        if v:
            v = v.split() if isinstance(v, str) else list(v)
            if self.proxy.value:
                if len(v) > 1: self.hosts = v
                self.proxy = self.proxy.new_hosts((v[0], url.port))
            else:
                set_hosts(url.hostname, v, 0)
        self.headers = HeaderDict(kw.get('headers',
            'Content-Type: application/octet-stream'))
        self.fetch_args = kw.get('fetch_args', {})
        print '  Init PAAS with url: %s' % url
        v = kw.get('listen')
        if v:
            def find_handler(req):
                proxy_type = req.proxy_type
                if proxy_type.endswith('http'):
                    return self
                proxy = self.proxy
                if proxy.https_mode and not proxy.userid and proxy_type == 'https':
                    return self.try_https_auth
            v = data['PAAS_server'] = utils.start_new_server(v, find_handler)
            print '  PAAS listen on: %s' % unparse_netloc(v.server_address[:2])
        return self

    class PAASHandler(object):
        def __call__(self, req):
            req.handler_name = 'PAAS'
            params = {'method':req.command, 'url':req.url, 'headers':req.headers}
            if self.password:
                params['password'] = self.password
            params = '&'.join(['%s=%s' % (k, b2a_hex(str(v)))
                for k,v in params.iteritems()])
            self.headers['Cookie'] = b64encode(zlib.compress(params, 9))
            url = self.url
            try:
                resp = self.proxy.get_opener(url, 
                        dict(self.fetch_args, proxy_auth=req.userid)).open(
                    url, req.read_body(), 'POST', self.headers, 0)
            except Exception, e:
                if self.hosts:
                    self.hosts.append(self.hosts.pop(0))
                    print 'PAAS: switch host to %s' % self.hosts[0]
                    self.proxy = self.proxy.new_hosts((self.hosts[0], url.port))
                    return req.send_error(502, 'Connect other proxy failed: %s' % e)
                return req.send_error(502, 'Connect fetchserver failed: %s' % e)
            req.start_response(resp.status, _fix_setcookie(resp.msg), resp.reason)
            sendall = req.socket.sendall
            data = resp.read(8192)
            while data:
                sendall(data)
                data = resp.read(8192)
            resp.close()

        def try_https_auth(self, req):
            url = self.url
            try:
                resp = self.proxy.get_opener(url,
                        dict(self.fetch_args, proxy_auth=req.userid)).open(
                    url, '', 'POST', self.headers, 0)
            except Exception, e:
                return req.send_error(502, ('Connect fetchserver failed: %s' % e))
            resp.read()
            if resp.status != 407:
                return req.fake_https()
            if 'keep-alive' in resp.msg.get('Proxy-Connection', '').lower():
                req.close_connection = False
            resp.msg['Content-Length'] = '0'
            req.socket.sendall('HTTP/1.0 %d %s\r\n%s\r\n' % (
                resp.status, resp.reason, resp.msg))
            resp.close()

    def SOCKS5(**kw):
        self = SOCKS5Handler()
        url = URLInfo(kw['url'])
        self.scheme = url.scheme
        self.host = url.host
        self.path = url.path
        v = kw.get('password')
        self.auth = v if v is None else ('',v)
        v = kw.get('proxy', 'default')
        self.proxy = config.global_proxy if v == 'default' else Proxy(v)
        if self.scheme == 'https' and self.proxy.https_mode:
            self.proxy = self.proxy.https_mode
        self.value = self.hosts = None
        v = kw.get('hosts')
        if v:
            v = v.split() if isinstance(v, str) else list(v)
            if self.proxy.value:
                if len(v) > 1: self.hosts = v
                self.value = [v[0], url.port]
            else:
                set_hosts(url.hostname, v, 0)
        if not self.value:
            self.value = url.hostname, url.port
        print '  Init SOCKS5 with url: %s' % url
        self = Forward(self)
        self.handler_name = 'SOCKS5'
        v = kw.get('listen')
        if v:
            v = data['SOCKS5_server'] = utils.start_new_server(v, lambda req:self)
            print '  SOCKS5 listen on: %s' % unparse_netloc(v.server_address[:2])
        return self

    class SOCKS5Handler(Proxy):
        __new__ = object.__new__

        def connect(self, addr, timeout, cmd=1):
            try:
                sock = self.proxy.connect(self.value, timeout, 1)
            except Exception:
                if self.hosts:
                    self.hosts.append(self.hosts.pop(0))
                    print 'SOCKS5: switch host to %s' % self.hosts[0]
                    self.value[0] = self.hosts[0]
                raise
            if self.scheme == 'https':
                try:
                    sock = ssl.wrap_socket(sock)
                except Exception, e:
                    raise socket.error(e)
            sock.sendall('PUT %s HTTP/1.1\r\nHost: %s\r\n'
                'Connection: Keep-Alive\r\n\r\n' % (self.path, self.host))
            addr = self.handlers['socks5'](
                sock, sock.makefile('rb', 0), self.auth, 0, addr, cmd)
            return self._proxysocket(sock, addr)

    globals().update(GAE=GAE, PAAS=PAAS, SOCKS5=SOCKS5)

def third(daemons={}, modules=[]):
    print '-' * 78
    print 'Initializing third for other python applications.'

    import sys, os, thread, time
    from types import ModuleType

    del modules[:]

    def run(*argv, **kw):
        if not argv or argv in daemons: return
        mod = daemons[argv] = ModuleType('__main__')
        def register_stop(cb):
            config.server_stop.append(cb)
            modules.append(daemons.pop(argv))
        mod.register_stop = register_stop
        mod.__file__ = argv[0]
        import __main__ as sysmain
        sysdir = os.getcwd(); os.chdir(utils.misc_dir)
        sysargv = sys.argv[:]; syspath = sys.path[:]
        sys.path.insert(0, os.path.abspath(os.path.dirname(argv[0])))
        sys.argv[:] = argv; sys.modules['__main__'] = mod
        try:
            thread.start_new_thread(execfile, (argv[0], mod.__dict__))
            time.sleep(kw.get('wait', 5))
        finally:
            os.chdir(sysdir)
            sys.modules['__main__'] = sysmain
            sys.argv[:] = sysargv; sys.path[:] = syspath
            if getattr(mod, 'register_stop', None) is register_stop:
                del mod.register_stop

    globals().update(run=run)

def misc():
    import os

    def Page(file):
        HeaderDict = utils.HeaderDict
        version = utils.__version__
        listen = 'http://%s/' % utils.unparse_netloc(utils.get_main_address(), 80)
        file = os.path.join(utils.misc_dir, file)
        try:
            with open(file, 'rb') as fp: tpl = fp.read()
        except IOError:
            tpl = ''
        def handler(req):
            req.handler_name = 'PAGE'
            if req.content_length > 1 * 1024 * 1024:
                return req.send_error(413)
            data = tpl.format(listen=listen, version=version, req=req,
                    server=req.server_address, client=req.client_address,
                    method=req.command, url=req.url, headers=req.headers,
                    body=req.read_body())
            headers = HeaderDict()
            headers['Content-Length'] = str(len(data))
            req.start_response(200, headers)
            req.socket.sendall(data)
        return handler

    def Redirects(regexps):
        import re
        from urllib import unquote
        rules = tuple((re.compile(pat),repl) for pat,repl in regexps)
        def handler(req):
            url = req.url
            for pat,repl in rules:
                loc = pat.sub(repl, url)
                if loc != url:
                    loc = 'Location: %s\r\n' % unquote(loc)
                    return lambda req: req.send_error(301, '', loc)
        return handler

    globals().update(Page=Page, Redirects=Redirects)

########NEW FILE########
__FILENAME__ = proxy
# -*- coding: latin-1 -*-
code = 'xڍR�N�0\x0c}�W�\x07��\x06c�4\x01�O�\x07����l\x14ʊ:\x1e\x10�㱓v\x17\x18\x12�*7�s.�K����t��F"\x12\x15�_0���ղށ�����I��X[��Z�!?ڸw�y^6E�k��\x11=6[\x07\x08� 3���\rDM[�Z\x12\x19M�\x0fH,R�y��\x1d���m!���b`@w�-�3\\�I=�>p�!\x1a�.|�.Z7m\x00��!�\x0e/�7s�\'\x0c��Z�|9�E����\t���]�#W�G�;�VB��BS0�ww�|\x02W��\x1e\x16\x0bb+7�\x198=���w\x00C�\x1c�y�N��ǥo������E��\x0b�Ym\x1c�Ф��K��B7��>��:���;\x02�>\\A��蹑\x07\t�P<��\x0b\n�t~$�g]�x����;��\x1a��y�\x0b��Zyx�o\x1e��F��������妏�����Ʒ�ۖ���ӏ�������ȹ�������͉������������ݜպ��ڸ١�淟�ᖬ�Ю�坟������Ƽ���״��������ӲƏ��������ˆ���ٶ����遰ř���ݳ���Ʒ������ӵ���ԧ���������⺕���ǫ���ϧ���ǒ�ο��͜��ߙ��ۦ�������Ō�ș�����И��ҧ��ؿ�ź���ɾ��勎�����������������������ٖ�󶒯������ǻ�������������ݟ�γ���ߤҚ����÷�������߈�����������Ĝ޻���������␟����ȿ�����������������Ǭ������Ϣ����ۨ��Ԭ���Ώ���ܧ�������ȶ����������ÿ�݇���˓������������ߑƩ��������������������������������������ޡ�ݷ��������������Ջ����̃�����������ږ�����޷�ن����麟��ǜ��������������������Ǡ��������ϭ�����������݊����˹����������������Ɖ��ߋ��޶����������ݱ�����ﲎ��������؋�������󥳚������������탅�����ܓɎ��ݦ��ݫ���������̔����⦀��߭��󉓹�מƖϻ���������Ɗ����ߪ���쎹������ҕ�Ȏ������ֵ¼����������אָ������������ٹْ����Ź��ח�������������������ɑ������������󱗥����֞�������筴�����خƞ�﯏����Ձ�������������宒��������ȅ������ۮٶ�����붡�����������������룜�ĭ�������������������ɘ��˽�����Ӿ˿򌿩������������Ҥ������㔃񁞬�簴����٫��ג̇���㎁����퓜�⢞�����Ȯ�����񾖭ǔ���ο�����������������������ͷ����������ۊ���䎼���È�����À�Ѱ������������������������������ߌ����כ��ô�܍���Õ��ي��֬Щ��г�����ފ�ŝ���ْ��ײ�ɵ�������ӡ���̘�Щ������������߻��������ק�������؅�����ҽ���ؘ�����ب������ߪ��Բ���֡ߞ�ˇ��������ţܓ������Ԫ���Ɂ����ָѬ�����를����п�ڃ������������ϵ����՝¥������Þ����̕������Ã��۫������ĸ�ʠԍ��ⷢ��������������ͬ�������×���밷�������ܖ�굮�ݸ�������Ʀ�ב��������Պ�«ǟ�Ԙ��������ف���������޳��ډ���ن׻����톑䮌������������������Ê��۬��ƫ���º������������ا�ٰ����Ҟ���䀭����������������җ�����㺀��ޏ��駣���ܺ��������Ғ�Ȅ�����Ϥ����������������ӏ�ݬ�뾓�Ī�������������َ�����Ê���ې���ߨ����Ң���������������������������������ͩ��񦲔�ڞ�£�ϰ�՝����۸�������񳡆�ۃ�����ԋ�����˻��ػ��΂����аՑ�������ή�����ѭ����ۗ����ް���˼Ұϻ�ߤ�����ק�����������䷧������܅����������߯�ĩ����Ӵ���ޕ���ڶ��������􀍥�����ě�����ϙ���͉������؊�������߬��������������ɏ�ʩ��������ԃ�������ߛ������ͥ�ͯÆ���Ї���ꮹ��֊�͸ͫ�������鼫��ƴɧ�������ԓΖ�ԗڢ�����ڴ�ǳ�����������Ԋ�ŧ������㺄�쏉��ŀ�񦯊Ů�߱���������ެ��и���ާ�ŧ�Ϣ���͞��Ӗ�痹������ݩ�ü�����Ҙ�Ѩ���Ţ���˞Ľ̹ߝ�������ů�ո읒���������������й��ʓ��������ׂ�ɠ����ղ������������єߠ��綔�ļ�����Ҭ�ߺ��������������ՠ��Ɲ��݌�����α��绬�����ݹ�߽����׊�ط���ɪ��ȓ��������Ì�����������ڝ�٢ʂ���������ݩ��ƅ���ҩ���������ӄ���������������ێ�Ѓ�ނ������������������󙣼��̂��ׂŖ����ν����ݛ׸Ӓ�������������ܙ������靿��ъ�������׎������쐖����ȭ�������菦����붞���������Ŀ����򀏁�����難����䎐��ʘ����㙱��������󨖀�ܡ���ܞ���ᠢ����ĥͫ��ߞ��˲��ӕ����������޿麳����Ε����́��뒜鎧�������������ƃ�����������渢ļ����ۧ�̹�㑩����ƴ����쒶����ϟ��ڼ̋��ҷ��ҵ�䘯�扌����������ն�䯾����׷���������߂�ٖ�������ڀ����ƺ���ѩ������д�����յ����眖���������������ќ�嗢����������đ�î������������Ȁ�땆�Ѓ��ؿڙ�����ߞ�����⥡��Ҥ�ֳ��՚�װ�������·Ӥ����٢ՙ̳�����虤٘��������渴��ˆ���˅��մ刄�߅֏Ҭ��Ȝ��჉���⽤������ذ����ޫ���ґ�쇉ٽ������Đ����������ƍ���������������ԥ��୆������ˈ���σ���������Ү���︊ۧ�����ؕ�����̅�ɣ��Ů����߆�����٠���������ێ�ƶ����҂��έ����݉����٦﯋��֠�ɝ�����ԟ��ߤ�������������欤莨ǉ�̝���Ś����������ߛܺ�ݖۊ������տϭ������ғ������Ơ���Ԍ�����Ɂㄉ���ب�������Ȏ�ū��Ρيի�������Ɲ󃩼����®������Ƌ���ѱ�Ҳ��位���������ߋ�����Į��͜������������𔭤���â������ꞡ�����������������ƃ�׸ԝ���������ڶ��󱯟��������ާټ��ʣ����ݧ��雊��ߵ��ԭ�ӎ����������̅��û�󊀱拰�����拌���Ԕ�������������ᏺ�����Ί���֍��؊�Ê�˹�㱄ȳ�����λ�����������������杓��ݖ��鋪������Ûݮ��ȉ�줥���۸�뉠��ж������؛�η����Ҍ���������������ͳ���彭��Ȃі�������������㳓��������������ڃٷ����숑���Ơ�葢�������������悏����Ь���������į�߀�Ϥ��٪������ܭ����ī��ݟ�Կ䇯������ۺꁞ���Ֆ���񞖭ٳ����Ƈׯ尥���Ԓ����厃�ӏ�����㮾�Ϥ�����ڤ��Գǚ���ق������Ӓ����������������顐������Ƹ������埇�م�����ӎƬ豷���ŵ����ι��������ν֎��������������Ǥ��������ȱ�����瓓��ǍϿƳ�����������ܞ�Ұ��Ĕ������������˫������̬���������׍�Ј����������湳�������݉���ҕ���̂ɼ���՗٠�ı����䘢����⣇���Ƥ�������ָ漋��ӆ壐���ô�֎�ղ�ԃ�䈁�����䂡�������򓅘؟����ż��ߕ����ҽ�耭��㥮����ƹ����������¡�٦���܆ۖ��݋�����ڦ�⊣��Ơē����ϳ�ܟ�ٳ�愴��ŋ����ɜ����ϧ��ɦ��ʗ���ģ����������򖡂�����Ѭ�ʌ�Ԫ۰�ĩݽ�밠���ߋ�����̅�����������Ѥ����������ߘ���ڙ���������̤���櫺ӗ�������༊������׺����ɟ�啕�����������Μ�π���ؐύ��������ѫ��礼�څ������Ӥ֞������Ò뀻���̀��������͕��Û���������˷���������ݸ������ӄ�����д�ڐ������ݷ������ڶ����򕉑��۰������ڶ����횝�����⭑�������ͺ�ũ�ɫΚ��ڷ������ٺ������Ű���������ƭϚ��뻈�����������ԉ�����۵������ʰ�����������Ո���ӈ�������֘��ħե䄕�癛�ꑔ������������������Ģ������ϧ������Ի��噺��͕Ʉ��ȩ�؟�����ؖ��������ĺ���������̊���ޡ���ѓ�����沽���է�����������㼷���������Ҽ��������ދѾ��ޱ�������읳�������������������ͯ������걼���ꤿ������飷㛂���������Ŕ�������֝��Ƴ����������ߋ������ٽ������ߙ��������ʤ�ⷈ����٬��������ѻ⨔ʿ���Т�����둪����������������яʥ���������⡛��髠���ݗ�������ֲ���������۪��ئ�ϓ��������򉓾������Ծ�̷���ě�����츧����������̡�¯꒙���������������ɠ����Ū�͓��塙������ݱ��������ﯟ��ʭͬ��¥��������������ό뽻�哖�ŏ�������ͯϰ�����������䳖�ߚ��嫐���������٧�ާ��믖����܈��������������ҷ�Җ����������҇��������򑰐����顧��Ï�������֓���՚���²��������������ԣ�Ҧ�����ދ��ƌ�������᠃���隖������������ѽ��ٯ��ت�ц�Ȥ���ł�������������퐼���ᡮ������Ε��ϯ����씺��������ݙ�ʢ��զ������ա���Ώ����������������ځ�������������������������业��������ӎ���؁���ު���ڗ����������������ީ솬������ٚ�����ꪲ��뫃�������奋��Ѯ�۹陗����ݒ��􉑏ڇ��ЪȌ薘������ﾛ��ۤ�ߦڋ�é�Ѻ��򭉘�؎��Ϟ緥���΅��Ի�Ј����ɵ�쨕��󑄴�א�Řْ��ʻ����߻�뀒���犝���˗���Ƽ�����������ϓ��ç���晖������������ŵ�ǌ���Þ��ۏ�������ǐ�����Ź�쭀����������݁�������������ꅾ���ך��������������ܡ������뒀��̕���ٓ�������ǹ��Ċ�֘戻Ҋ�̑�Ä��������ڤ���̮�̌�������������ϗن�����铱���ݷ���������������ڀ󥳬�ß�Ų��������������챈������Ϣ����Ѩ헢ь��Ҝκ��͓��۞�ۢ���ܠ�Ѿ�Ї����������ח�ځ����ڠ���������������������宅�����ɣ��ߪ����ﯹ�����ʨ�ٞ��٘����׌���ѧ���휏�����̐������Ȑ�򲎺���ި����������������Ү�������؞�Ȏ����٨��ԥ�ى���Ŵ������������ܲ����������߄ժ��У��ؙ���鹳�����­�د�����������߳ٗճ����ͭ��Ϥ��ㄐ�������Þ��������̫��������ؚ������Σ��ԑ�淂���͋���Ǿ���ᰦ����ř����߷��޼������亯�������Έߜ����ʉ˙̔��������ɲ������ۼ���ڼ�����������Ï���������������̜������߹������������Ï������׽����������׏��޲��Ͳ͖��܎���ĕ�������҉����ؤ���޽��Ø�������Ï������Ӻ���𯻔�����ܴ�Ơ��������������ߎ컼��ݰ抗�ˍ��������껼��������ԛ��ٹ���������Ѧ���Б��ˏ���������꽮����ۖ�������Ȥ�������ѳߧ��ϑ�Ŝ���������ײɼ����ϒ����ː�պޝ߁���������󣞋��ئ��ӆ�㦠��ܒ�����������Ͱ˿˰����း夝���؅��������ϕ���������ѷ��ʱ�ǅ����������Ѽň������ܭ�����凑������ꪁ�ˍ��ק���۾����֔�����ˉЄ����ۚ�����Ɍ���耸��ۨ�����㶹ڭ����兕���̱����ĳ��܄���Ϥ��������������������������������뷮������������˖���������끢�������ߑ�����̱�躿�Ĥ���������ת���㨟�˺������멷֠��ϐ����Ǉ��蜰ʖ���ڥ��ϙ���Ț��Ѭ徸�ҍ��Ӎ��Ɲ���ш�������������ѷ����������ԟ�؝��飸��˯����ҵ���ԥ�׬�ߎ������Ǐ�Ž�ڑ���̖�������ɳ����йߊ�ޭ�֙��拙͢����Ե��ᕚ���˛������Վ���������������ㅞ�戀�����Өʤԅ��Ė�������䄣����䫖��������ϗ��ޔ�Ӏ��ݍ���ۦȴ������ˏ������������������ȅ������������ץ˪Ǧ�»��䣂����ۉ����񮦰�랍��̛��ܑ���������Ʃ�����������՘�������ص������������۫���������������ӻ��Ќ�������̬���μ�ţ�����ń������젥��������ãé͠짼۔م�����ڿ�����Ů��������ݽ�������ā�֏�������ߘ�ț�݀��������Ѫ��ݠ��۟䡰����ԉ���ֵ�������א����Ү����ᇜ�������������Ղ�Ȩ��������횜���˿�ه�����������Ӯ�㣷�����������������ң�꾈ʘ˫���ƹ����߸�ᕇ��ϳ��ʕ���������������ځ������ت�����ܠ��������ë��휬�������↾���ͬ����Ӊ���������������ê��������Ƶ�˘�ꚸ�����ۍſ�����Υᴯ��ņ��������ȝ���������������������ˢ����ͨ������Џ��������ҕ������Ͷ�����ا�����Ϧ��������������ͩ������ͨ�Ю���ˀ��풍���˨������씗����Ү��ۛ��۷�˒�������������ϯ���������ݯ������එ�������ߛ����􂐥�������ۓ�ū������Ȍ�əԋ��������������ß�������򅦴ე�ب�����������Ϥ澰Ԍ��������֕�ی��������Ι�������𥀌�����񭋚����������������������������©����������������������ԉ�����﫿ŉ�ӎ����������ň��ٝ������ѳ���ԯ�����舺��ƭױҟ��������̪Й��������яݩ�����˛Ȳ߶�����߽���ᰀ�����Տ��ӆ��Āۆ��������ō��ƹ������������ڭ֥���⤵����ߗ���������ѯ����������й���ڔ��ˑ����Ɗ�������כ왊�Ф���ն�������Ɲ��󚹱٨�ߦ��ϵ�ȽŸ�̻��ַ��Ʌ���ɕ��������������Ӎ���𰣝���ٞ����������ˬ��߰����仵�����Э����͟������˄���؍����ޫ��������������؃Ҩ�ɴ��ࣴ������҈�賫�ݻ����ݝݑ�����ִ��ڡЯ���ʜ����󍏶����ⷅ��ʡ�ִӳ���������������ٖ���������߃��������ŏ�﫫����Պ����ܾ��Њ��ˏ���̡�וʕ���Ւ��޳������㈥����Ш�������ܼ����Ꙓ���߹�������Բ�����������������֗�؋��ב���泩���������������ԟ���ީ���¸��׺����̓ڑտ��������������������҃��޽�ϐ���ɒ������������ၕ��������ȼ��Ų��忈��������Τ�����б����ܰ����չ��ܖ�ο���ڪЗ�ݳ���ڼ��������Ȏ�������糺����ƛЯ��떱�ˡ����ˌƷĘ�ޛ�Å����ĩ���铹������Ц���҆뱎����و����������ٞ��񺴕��������֙�գ��������������Ǳ��ݰۻ��������������������蹧�ɶ���Ƚ��ι��ԫ��柢�������ⱂ����ᑩ񳣑��킿������ɍ���ؐ���ֽ�ճ�������熔������������օ�������ޑ�����Ì����ᚄ����ꩉ�䤙�껷����Ԥ�Ⱦ���ԟ����������㹛��������杽���혔�ا���ċ�������Ť���ĕ����ʛ�ɲ����֊���ƈ���������븭�堥��������������Ǚ�������ض��ÔϨ��������ǫ����Ž���ٓ������ӿџ�����攟�倫����ؠ�����񯿇��Ɯٴ�������ާ����ր���ū���ʏ�Ȉ���ЁΧ�������������ŵ�٘����������Á���у����ٔş��ǯ����ј�Ň������ʷ�ȫ�����ݫ���׍����������ׇͦ����Հ�����ث�����;��ܚ�򕷛¥������ߎ����������ȿ�ݸ򢧘��������ʿ��������ƒ�������궣��إ��������������ˑ�х�������������𴞩��������¥Ѻ��ˋ����ź����Ǌ������а�ÙȐ��ϑ������Ӏ�Ʈ����ܘ��������ٝ���и�����Œ���版��͋�Ѩ���§�ާ�ԡ�ϝ�����Ě����ן�̹�ȋ������٪������Þ�㴕�߫����򇂇䓰ם����ã������׋���ߐ���ԏᏝ�����Ă��������ג��ɷ�ݚᵸ���ҧ����գ��Ɋ����������������ğ�������ٝ����İ�����������﯁���ѡ������������浯ĥ���Ќ������������戀�����Ì������䎌������ȶ�����ʪ�����Ϫ���ܢ����Ф�����Ե�ج��������������ݯמ���������恡��������������������ҫ�華�����ʒ����顗���ݬ������Ь���í݅飢����������閡���������޲���瓻�����߾�ߎ���򶯃飅������ܰ����䶃�䕈������������ʈ�ܥ��կ���ćĚ��������ϕ�׊�������ΊǷ͔�ǽ������ā��������Ԛ����������������������巊��������韛��Ӯݼ���ڐ��������ȭ˯���ڞ�ܺ���ō��߆���ߝ���޴����Ř�筒�����������ŧ����Ѽ���Ő��ܪ��ґĦ���ɞ����㏢���٢�����������������܎��נ��뾅��������ǒ�ׂݏ�ۀŁ��������긍���������񗓀Ȼ��П�Ǭ�����ɇʅ���Ʈ��ŲǍ�ٚ���̅�Ძ���ŒѶ̱͟������������������ŉ�����Įط��Ո�����ѯ������ږ�������ݤ���粽���С�ӗ�װ����ֺ������������ҝ萪�˽ւ����論������܏�ċ�ܿݻ���Ȅ��Б����Ƶ�ۯ�󺊠���ҁ��������̠Õ����ǝ����⛙�旳�����即���������ϐ�ͽԅ�֝��ě��ʸ�߮������ɬ���䛾����ŢŰ����Ƕج��ܽ�����ʹ��ʓӻ��Ȉ䖄����Ǘ�Ԯ������������٫��������騗���������̟ټ�����ݝ�����뾮���Í����������˵���˾ͯ������ͭ��������ф��ѳ�������ʇ��ľ�������ʹ�����Þȃ������۞��Ҫ����������޷����������ѻ�ކ軬���վ�ȋ��������К���������Ѽ������������ޅ�����ƾ�و�؇�Հ��������������Ɏ��ؽ����ܩݍ�إ�����ΰ�ݤ�����ԅ��ٹ���ګ����𛼻��媫���嶳��֭��������������蔆�ٳ�̔�嫧������񸯦������ϛ�����ڢވ����ȷ�䬥����������ķ����������縩ߵ�Ӵҕ���䳷�������ָ�݇�����ݐ����ʔ��Üϧ������Ԑ������˪̴����Ӽ����������˅�񏕑�쪪ٻ���ʴ����������������ګ���̋������ᶝ��������ߤ������⪶֒��ћ������������͟��������ɧ���������ͷ��͝�쾸ֱ�����ʂ�ԝ���쫯˕��������������֨���ͼ�����ƞ���������υ���ꈯ�������ݗ�����������ל���ޖ��������ۄ������ߛ���Ⱥ�����ճ�����꾋���ǌ��雵Œ��՜��������������������ܪ������ɟ������ݭ����ʬ�����츓����������ބ�����ѻ�����ռ��ܶ������ˣ�������ߣ����̖������Ч���ۆ�������׷�܇������蠸�ܾ��啞�����믒�β�����������ȴ�Ӫ��ڤ������������˱�������۰�����Ʈ��ö�������������ԫ������Κ�ɔ�܎�ԭ��ѽ��ɶօ�ɛَ�����Υ�ω�ڻ�����뱨��������������։�ս�Ȃ���ݞ�Ҕ�������������ѩ�Õ����݌�Һ��勾�����ۤ΃頒�����¶ܵ����ۂ���ڏ���Þ���塲����������ӛ�������������ҍў�������ؖ���͂��֒���ޒ��ɧ�ָ�уå��Ѯ�����ه���ո�����ؤ��խ��޷���ʾ��������Ӻ�����������眻��σ�ِ��盘ʡ��������ĳ�������刚�塙��ኺ���ٓ�ȶ��ٞ黑��ӻ↯ڦ������ɝ����⹼������к�����������Ε��雹ކ�ܰ�ĺҪ�硂���ʌ؍�����������������À���̷��ݝ��ꛟ�����������阂������������̰ʣ����㛝����芌��ޝ�ݏ��ۑ�������������ӱݙ���Ҳ���Û����ّ���ҭ�������������ѣ稱����ᄐ�ꂍ�����ξ�����ۍ�����ݔ�Τ��֩鬢٫����ܖ���ߗ�몍ϕӱ��������������豜����¦���͚Օ�㑪���������ꜚ������Ǟ�����Ѻ�쭛訩���������ق�������Ɣ�����ڳ��̚֋����Š�����ݾ���Յ�ט����٬��ǲ��ۤ����˷�ī���������ᭅ���˴��ݿ�̓���������Զ��ꗉ�������������Ì����ց�����������޼���ݣ���˿�芀���������Ȯ�ݷ��ԡ����፠����ꛥŅ�Ծ�陾ɳ᮱ؔ����������٣��ˁ����ΐԓ����݋֏傉򏛾��ⶩ�����飴��ַ�ϡ��ԗ�ݬ��Ӷ����ߝ���������Ъ󵂝���ύ��ե������������ơ䚡�ԝ����������݂�������������Ց����ג�����눾����՘�����щ�����⮤�ĥ����˼�������������Ը�懷��򳓃թ�ۊ�����丄����寅�ݿ֮����ɐ�����𾛎��������ᒀ�������⓼����ڷ����������𘟄��������������Ն�����ĕÑ���ߞ�ʌϡ�֨��ɦݶ�����Ѹ�������ù�����฼����ΝѾ��Ҳ�������ç��������������������堛���׈����ؗ���è������϶恳���ݜ���֘�����׿����������ʭ����Ҿ�����֒���Ǌڃ������㍷������뻭뗍���Һ�������̝����������������������������Ԙ�����ڣѮ�ޫ������ځ�Ƙ�υ�����ި���Ը�ʗ�����վ��ʹ���ң������Ħ����ڡА�����������Ӝ������և��񏫊����ż����͔�������ݨ�ͤ�����������������Պ�������ɼ��������������묲�ע�����������ѱ�������������ޕ���۝���ժ���ɚ������̌����ۥ�������齁ք����ƍ�������𒭄�������ؘ������ڋ�������˙���˪՞������ы���Ԕҙ���坵�����������Ս���ݢ�������ޕ�ܮ�������ݵ����樃����������ٲן���͡�����ϖ������ݾ܅���������ӣ����˭�������ӎ��٪��ʤ��������������É�椉������՘��ߪ�́�����������������ߺ���������������ᤈ���ܲ�������ó����������ۇ�ʨ���������ٽ�����������ӫ���Խ���ɲ��ʊ��������֎����թ����������ߢ���Ħ�Ț�Ԛ�̿�Ӿ����ۭ�񶣡�����҅����ʐ�Ȃ񥛈�������镕��礧ȵŊ���������Ҍ����幑�恂�ݜ´���Ӿ���ᯕ����ׇ����񅝝͇��ė��ң��꼬������������Ҩ������ǂ�۽��ɏ攮���������⟒���ݺϴ����ǅ��ۿ�ސ�������ĕ����������˫����������گ������������ĩǃ�����������ح���Ǎ���������З���Ύ���߂僕����ʬ�Ƣ����َ������ۮܩ�����ײ��ڹ������ӕ�ד��ǐ�ނ�����돳҂��̚������뙝��丅л�������㸀�����ւ���֡����Ѵ��̔��͔����Җ�����Ƒ���ս�ۡ��Ȯ�����߱��������͂�̭�ǐ俾�����힅�������׾������Ҽ���ꋢ�������������㞮������٦���̓���������������˼��邅���ٝ�����Ȉ���������������܌���ˡ�������ĉ������ם���Ո�絾Ζ���Ժ�������Ѿ����ﻚ삣��������휽�ű�����Π��ݼ����ܧ�������ǲ������������������Ö����������܅��ߑ����᭘�ᙪ��Ҋ������ۻ�����胈���׿�������κ꨺��и����ς�����Ԗ��ƞ�������ﱈæ�����ԥ�ת☥������⯋��������������ϳݮ���������ñ�҅������㢓Ԝ�������р���ᣵ�ߧ��ޔ�Ѻ�Ƒ��;������������۹�׌��������Ą�׍Ս�Ǉ�頹�ݳ����Ľ����⦥�趷�Ŝ�����ш�����݋��贘ӗ�̮�����Ҁ���������ʚ���ū�������߂���ľ�����Ƒ�������������߭����ޕ͉�����Ѻ�Ŝ�����Դ���қ��ͭ�퓷�����壳�����À�ê��򓅎����쌰��䋈�컾�Ȋ⠇��Ŝ��Ґ˰�����ٕ������͖���֖ү��܈������޿����ƣ���Ř���펱��Տ�圥�嬂����ŷ���̘����ϓ��̌�������ʿ��������������ؐ�񑜺�ە�����ȑ�������枛���˺Ӭ갶��������έ���ݥ���ρ����ݏ��������ˬ��컑ʡ���ފ���̩�������̖�ڊ����嬬�غ����ڭ��؝ޢ�ۈ��Ǆ���ڕ�����ӕ�ͪ��� �¼����ԃ�溢�����㣲����˪깺���������������˰����𞋓����ڠ����͎�ꋄ���乨��ğ呶Ϫ݀�����������������λܷ����������ֆ������ʞ�������䱏�ߢ������������ݖ�������˖����욂�����������Ä���Σ�Ǔ����У␲������ꉙ�Д̌��ق��õ��������Κ������������Þ��ح������������������鉻�������˒Ɋ�����ѧǪ�૞�����̛����������������Í���껱����������֊ԥ��ƛ��־��ޫ�¦���ʳ��ʙ�ҏ���ֽ���ૉ���É����ɢ���������غ������쟀���̳��ì���ժ���Ϥ�Աǚ��������걧�͒���Ə�҇������㔶����Ȱ����������������՞���������﫜ӽ�������ѫ����������������ⲧϩپҬѦ��������ͳ���Կ��Ջ������ׅ����̬���������۳��־�������������������軋����̜޴��������������߷��粨��ʫ��ꔷ���ސ���������˷λ���ֲ�ص�������Ҿ�Ҿ�������������ؿ�捧��ڶԏ�������ɸ�ҋ���ڌ�������難߉ő��������鱑���������������������������̖�����������݂ܼ���߬�������݀��������ļ�����ʅ����ꇌ������������ế�ե�������������ϱĴ�������؄�����ކ��������ܾ���֒ř���������ĉ�ڀ�������������������ᆤ������ܟ������ɓ��ݠ�����ɣ�������Ѓ�����ۛ��������ͯ�׷������􀸇������毵����֞���쌧�����Ț�拉͙����ڵ��������و̶�������������؈�������٩������ֵ���룚��р����ӳ�����������������ӝ��߫�흸܄�٭ꒂ׫�ܵ�ݓ������ڥ��Ģ��������������ۚ���ʺ����˕����ʡ����������ƕ���兞ߙ�������峂����������ݜ�׉����蜷ͽ����̦������㽩�����ŧ�ƚ����Ț���捝������ې��姿�􉷷��ʜ���ݟۈ�������̮��읩�������ŕ���絛���������������輳�϶����أ���㰖��ͼ��ۅ���������̄��坤��ܶ���ˋ네������րι��¦���Ύ����������������������ز��������������մ���؊䀧��������������ץ�섏���薒��������͠���鷑�������ă����۠Đ����Ů������������޶��ŧ�����������ŧҫ����̈́�Ȝ��ܗ�ۀ��������إ�����Ҩ������嶢������������֮���ޭ��ۑ�ѝ�����׿�Ո���Ǿ��Ӝ���К���ά�˿�������ڜρٜܤ�꫖�������蘑����ߡ�����������������֢�צ���ㆉ����ʥ��������ڌ����򜥋Գ�݆������ǂ������ҡ������ՙ�͚��΍������þ�������둶�����Ӳ��̞����ߊ������۶�܋���ى�μ����ّ���ן�����٦�䜄ʔ��������α��������۸����ֱ�����������ԭԅ����©������˰����������̍���󧐩������󱥞�����と��Κ��֡Ҳ���������Ŗ����Ͱͨ���������������ɲ�ߴɱ����ɖӔ�̫�Ե���ш�����Ë��܊܄������ŭ��΢ˮ略��ߋ�в�ޯ�꽴���Աۥ�ʄ���ش������㮅���񦴅����였�Լ�����܇�ە�ͷ����ɶ����������걆��������������۪��ձ��ע�����������������񅴪��븹�����Éٵ����ǥ���Ǡ�܆����̍�ɢ�ɇ��������˱���������Ɯ������������У������������ۦ��������г������ū��鄦������ۇ������ת�Ȉ�ܔ��忉��΃���݂«홉�����ع��������㕩����������𒁰����������ɉ܂пϟ��ձ���ǀ�򜳢ܢ�������腙˘����������Ƶ챮����ˇ�ޜ���������������ʙ������������ۋ����΀��������������Ƿ���򻙞�������������堷��ԣ���Ŝ����ܔ���򧐉�κ���������ὓ����������ِ�݀���������Ϝ����ӧ�������뾾������ܬ����Ӆ㯁�����՘����䔫�������烱�����຦퉐���Ǵ��������������߈�������꾥����䈀坄����ɝ����׵��̾ˤϹ��ˬ��������λ�ю���ǵ����嫪�������߿�����ڐ����զʨ�אҟ����ǭս�݃������ɵݜ�����Ʒ���̃��ԲΏ����Ĕ�����Н����ુ������������î���������ܦ��ư�������ޣ�ٺ���Ȥ䞘�޽����������嵁������协���뛟�ߗ���⫺�˶������Ɏ��孥ϑ�賴�軣�Ύ���ۅ�����������҆��ܶ��������������ђ��ɕ̞ʌ���쐬������ė�ℝ�����߭�ꄹʿ��ض���֤����͛���۲���Ȅ����˚��ۣ���������呺����Řʡ�����������̶���ƶ�����◛�����ਲ�Ǹ�������Ѳ���������ש�������������֨��������΍�ژ�����Ē�����������۾�������ɘ���݀������Ш�����ܨ���ొ��Հϼ����Ń�������ʑ���������؏����ޣ�����另��������ֱ��������λ�ƾ�����ӌĕ��������٤�����������֯��ԫ��룭�������������Ӕ��Ȼ�����Վ��������󲾝����æ���ϵ�����û������Д�������ҵȗ���˷�뛌����㛜�������ݺ�ԛǼ�ڱ���﬽��Ϋ럑ò�Ī�ل�������ꤷ�˸��ͱ�������ݓ䫺��ߣ���������Ϥ����ߚƭ�͓�������ǁ��и�ͨ����̇��������Ϋ��������͋������ϓ��������������׭�������܇�̠�������ܼ��㧽�ȗ�ܬ۲��㽐��޲��ܪ����ݙ��Ҧ�ࡤ�톼��ܺ��������质������ۣ��Ø��������ֽ�ڏ׌����ݣ����М���Ӌ�������������ˣϏ��¢��ދ��������Լ̮���ן뺤��������ҥ�������ţ���裼�Ť���ѩă�ґ��鶟Ҳ���ғꫜ��̐�ѥ���ת�է�������������ʞ���ǿ�����������ۏ̖�����ſ����ޖ���������ɪ�����������ԝ����Ź�՟섯���㖲��Ѣ��Ө���ֻ���Ǉ��ؿ������������˒�����ᝇ��������Ϸ�����Ȯ�������觻��������Ɗ�������������ӊ���ʒ߱�����߫ᷭʉ֖����������������ͭ���������ф늎��Й���߾��������ȯ��������������Н������ļ��������������æ����攬��÷��ұ��Ē�����ׯ��٩�����ɘ����Ұ֤ڍ����ӑ���諬���Ɏꤾ���ن�Ԝ���������̠���µ�������͊�����������氌啛���˷�ɺ���ީ����߂������ē������������������������������Ս�������۩���౓Ԙ���驇��ŉ�̏����Ƥܭݫ���������������팰ݕ����к��������՞�ڳ홬�������ⷘ�从��ڬ���«�ĵ������ʏ�ؘː���Ȼ���ײ������������Ż����Є����ʸ��䮯��������܊Խ����������������������ݪ��͎������������ͬ�����𨐘����ݚ�����ŗ�������ł̥�񾭿������ԭ��͗��������ئ����������⢝����ɨ�©��˪������ƶ�����޵��į��Â�������ǻ��������������������ȶ������˿ԓ�ِ����٢�傛�����Ԉ�������О�·�������߉���۶����������렙Ċ٢���ǲ����������ʰ���Ի��܉�����������ѷ������������磂������Ԩۙ�շӠ�����Њ˼��������毻����Ҳ������ޭ���՟��������������������҈��������Ӿ�������ߤ����법����ߋ�栟�Ǉ���ׇ������������������ŏ��ڜ̧�������������ӄ��س��ȁ������ǉ����������������ȱ�ԫ�������������������׈��춖���ߛ��������ڌ������Ԩ��������õ���ٴЖηȳ������������̄���ל�����������̬����،�������Ȓ����ދ��ޢ��롦Ĺ��擤˾�����Ţ�ض�漣�̂������������ڎ��ώ������껔��Έ�섂�߳�ؔՔ����������������������Ծڅ����ǿ��͸���ߜ��𲞳ȡ�Ǡ��ޘܶ�ݔ���ê����߰������������Ͳ�ӣ�����͋ԡ����晽��ֺ叉������������ّ��毝���Ǎҁ��ވ�� �����������żؘ������۴����о�����䞁踱��ˉ�����Ȓ�ӄ����ט���ȥ��������ޒ���Ń��ߦ����ę��������ӄ�翜���É��♧������������ǌ��������������������Ђ谽�ߑқ����ٶ���ͅ��������ۍ��̦���Ɲم�߶����ң땊�ޑ��៯�օ��Ύ�ٸ����������ǔ�򡒎�֯��ť������Έ���Ҏ��́��Ē�����҈ތ�ބ��󻱼����������������������������ۄ����׎������£���Ӊʀ����֨˦�ܰ���՗�ĺ�������˝��Ģ������ڂ�����������ɖ����̜����蹹����쬓ť☰�̷��Ǭ���Ѻ����Ԫ�Ŷ�ؒ��ҹ�������������ߘ҅М�ث��������ﰊ����ƨػԸ����������ı��������ݜ���䆧������Ƿ���ꪍ����Վʙ�Ʒ��ࠕ䥾����ބ������ѫ���͆����𡂯���ք�����׻؉�Ҷ���։��ϯ������؀�����د�Ρ������󍟒���֧ɦ����㯀�ͷ������㾭�������Վ�������̤�֍Ӵ��������۶ߴ������쁋���݃�����з�������ū���ǟ�����Ͽ���������ޞ�������������ŧ�ږ����뤎��������������콹���������������������ǟ���ۤꮅ����������ڠ�ɶ��յ����������������������������������؈�߭��������ڌ����������֑�Ր��դ�̶���ք���˖������Ȣߣ����������؇ݧ������ш�Ӣ��̃�ҵ̌֞��������������Ѣ�հ�������˝������ɠ����ث���������ĳ��ϴ���������ޅ��������ϕ�ۑ���򂖣ې����ӍȠ���Ĩ��Δ��鉓���ԗ����������������ۊ�����粴���������䭴����ڟ������㢙����Ѳ������ٸ���둹�������ྩҘ�������ȧ�Ϳ�߮ｃ����������������������႞�ё���ˌ䧸������΁��ܸ�������������ք��������˳Ö������Щ���ۙ�������υ��ү��������̓���󑣩���������ߟޠ�������ڿ����ع��咜��ѝ�Ӊ�����Ғ�����܃��ǩ��е���а���ߦ�ߕ�����ň����犃��ԍ�����������΋Ľ�����Α�촻���٩ݨބ�Ź�ʢ鳾�������Ú����������堑�߬����藴�Ⱥ³ʶ���������ݼ�м�芖�׈�����۳��ĳ�Į�������Ľ�������˟��ܲ��ޘ��׬��ȖҀ�Ԏ�㦠�߯����������ãњ��Ի�㋇�攷��������ۓ�����ڤ���蒪��񈀖򰓤��ə��Â����骧��ؼ�����������ċ֓���¹���엤����߷�������ғ�Ѐ׏���ɐ�ހ�����͈�������������ܠ������̪��������ɬ�����츱�����ὃԒ�����՟���Ţ�������ؒ̚���寲̐������ܓ��ʷ���������䥇��リ�������ֱ�Ù����������ޓ�ږܗ�魵���������吾������������������������ؓ���뿡��ܗտ�ڷ���˰骋�Œ����扁��߅��㵍��沜ʪ���Ƀ���آ���˄�����խ����������Ġ������Й���Ȋ弾�������҈ꃞ�����ߠ���������к��������ψ���������������������פ�����ݷۤ֕�󧇭�ϳ��������������ٙ����뫨�۔܁��񄌁���¬���ʌ��������ū��ƶ�������ȩҏح��͓����齬���������������ی����Ӯ��Н��������Ϡͧ�܁����ڠ���̟������٠���Ռ����ˉ�Ꞣ�������ъ���ӝ���ާ������ڧ��ɰ���������ҵ��鄍������ל���������������Ȳ򗆇ѣ��������ϧ��Ѹ�����將����俨����ܒ߽�����������õ�ϵҚ��Ԃ��������딣ா���������ۥ���܇�����΄��������޴����ꢙ��毐���÷��܍�Л��Π����ي��������ꟙ��볂���鷿������ƾ���ԧ�������󭡫�����݃�����آ�տ���������������������޽��֖ڳ������������͔����������Љͫ�א�����敛�������ﻶ���������܆��������吨���թ�ҕ�Ǜ��՛�՚�蛎�گ÷���іش���������ǫƘ��추���������������ܭ���������ة��ʵς����������Ό������΂�������ؖ�Ӑ��������������Ǫ��ʙ������̛�Ү���ό��ľ�����Ԅ������桾��а�����ᔺ̱�ۄ������҅��������ɻ��ʡ攚������Ӝɣ�ᕵ������Қ���й��������뀓���閂�ඐ��ֆ����И����򬥢��ϭ͕��ĉ蜼������ɖ�מ�э�ޫ�ڟ�Ϗ�ß�è����������ཡ���椹����ƶ����ȡ���������͵��ǋ������ۗ���������򿁿߯�����������ª�ũ��億����������������͐�כܵ��ނ�������²�����֔��݅¤����Ԭ��������������Ŏ�������ͼ�����������������Ǌ����סߣ�􎈝������橲�饁�ˈ�����ݎ�ʥ���赭�������Ϳڢ�������Ɂ�ᫍ��ֵփ��ٲ�Ԁ����ו����рڳ������݂�Ԡ���僅��Í������ё�ٸ������ׅ�Ҿ���ғ���ⱀ����������������Ů��������稆����Ͳ���������󎆂���Ê��������������ﲒ���̪����ֽ�����ߋ��䱁��ݜ��Ш������ğ��Ж�������Ɔ��Є�໩����폑̲��̀����������ξր�τù���������������Ӯ���˙��Ԩ�������������˲���Һ����ʔ����ن����������ء�����脽�����������������������ј�݁����⛷��α��ڸ�������¤�������Ƽ��þ���ޑ�������������������˼���ߐ�ӑԸ𕔈����耩������Ԛ����ƔՄ�݅����񆁅������������ְկ�ӗ��ь������ź�닣�ݾ���������Д�����♒������磹���ѥ���������򝳭����墝���������Ļ����̡��ڪ��ث�Շ����Ӫ퀉�г�ﵠ������������ۓ��̲τ���ߵ�����΃����Ɔ�Շ���ٔ�만񾘱㞴�����ɀ��������������Ί�ϰ�ֿ���ʆ����涵��ͽ�ꕓ�������������󼨻�����ڐ����������퓿�뼇ė��ȝޤ����݂�ҩ�����ӂ��������ī���Ė��о����᢯����ګ�����ً����������������˴̒�Σ����������ۄ֠�����������ֵ������������֐��Ĵ�ʛ�������ۉ�͗���ӳǀǑ��􀞱������߿����ᒮ���ֺ���������ԇ����ੳ��ؚ���֖ˉ����؃���������������������үƪ쳩����ئ؏��������Ԫ�����������������������Ѥ����������뚐�������������ԓ�ψ�ɋί��댻����������ʼ��ْ���˧�����Ԓ���������қ�������Ԥᑐ�ٍ��������Ɩ�̳���ג������������ԭ��������������̕�����������������Ũ�����ͱ�ȳ�����á�������ܒ�ݚâ���Ý��У�����������ƈڲ����ʺ�ÜՆ���ԛ��ԫ�ˠ�˼�����ڟ˪Ɪ�������ו�������˗���ậ���Ʒ�����ԓ膪��پ�����̛犽Ƚ剆������ƺ՜̇���ȓ�蝫Ǘי�������҈ђ���ܧ������Ǭ����؋�����ܱ�吣̠����ů��������Ҡ��Î����������������ͣ���褬ӊ�ܦ���������������ݳ�������£�̼�ꆌ����������Ï�������ڨ�����������������ﳹ���ȶ�����ަͬ�����٦���������������������Õ���ׁ�Ѕ�������󑾫ڱ���Խ������ӆ������뙆����������ߝ���˄�����������Ѓ�ۏ�����ˈ��Ò����斓���������ȭ��ņ����������߫��ێ�����˅�矶�ӕ�����ڂ������ꕦ���՜ͱ�������������Ĝ�靵չ��掝�����������ᣞ����������������ȸ�������������院����·������ܗƭ����γ���������戭��͌��Е�������ð��ف���ؽ���������Ј����ф��ɪ������˜����Ϟ�����Ң��������������˝贽���Ń��������ֵ�����؅�����������ܑž�Φ����ɺ����چ����ǹ�Ѷ�����״���ˍ��ѿ��������س���񢷰Ȣ���ܱ���ܺ�������Ʒ������ם��γ���Ȳ׉٧������ħ�����Õ�������Ƙ��Ų���ߖۃǃ�֨�����ƿ������🌥������Ӈ������������롤��������޼����Ϟߟ����������֕�û�����ԃ��ש��ʆ���������Ƞ��������̗���鳚��ͨ�մ��������˥����������ċ�ߌ�腞���Ձ����첛��������ȑ�ۑ��������Ӂ��趫�������ܬ��ـ������א㌬կ����ʦᖛ��م�����������򞢀����׬ۗ���������ߓ����󯌥�������������֥����᫑�񩻺�Ǥ���Ч��뽷��췕��ֆ֏�實�����ͼ�����Ώ������Ӯ�ﶫ�ɲ���Ί������׮ጙ��방���������թ������ʦ�֛��˪ס��������Ã�ݔ������֖ɮ꓈���׉ԥݮ��Ӥ�蚪���������������������ۀ���ٲ���Ì����Ǖ�������������Ȋ����ʟ��������ˎ��������Ǣн���ϙ⟐Ҩ���������ב����ڙ�ݿ����㡜�Ӭ����旑�������ż։Ą��������ⶶ���Ć͔���سط��������������񚚣������������񑳕�������ٲ���Ճ������ߌɰȉ�����������햕ń�����ۍ�Ő��ڀ������������š���������կ���񛒼����ش���������������������ڨ�ͪ麬�������ׇ������������������Ē������ض������ؒ摔�����晵���˽���ʎ��ձ��ܪ��ћ������Օ¸�䳀�ܥ��𕶩�욠������錌�����Ǩ�՝����������������·��޼����ű��Մ��󬎐Պ�����辋세�ͣ������ͼȨ�����ҁ�����ǡ����������䦧�����ώ��ڥ��������ݍ���������������ٞ�����������쫯Ŭ�죵���ֆ���������铂����Ó�����������ߤ������ͺ���ȹ�������鵋��ӭ��������ܦء˥��ԟ�ֻ���ʨ��ָ�柛�������������꫺�ޗ�����������󠅀牵��������х���������񧼂������������ٕ��򏮕��ئ�ô����ն����Ԗ�Ⱦ�Ւ�򨅲߬䆆�¬���ի��Σ�������Ų�����ϟ�٦��Ǌ���ט���ֆ����������ʹ����ћ��́����ǒŴ�����ճ����͂ĩ�������۽���������������ڇ���ן�����������¶�⸱������������͆������Ϣ�������庐���������͂�Ɨ활獾믫��������Ք���������Ī��Ǥ����������������۸������Ʌ�������ֈ�ӻ���󕒏��հܼ�셜�����������׌��Ϥ���緃�����������������������������Ғ�ú䩷������������Ȑ��̋������������������扄������������������������ﱫ���Ӏ������񅡓���ؔ����Ӵ����ĬՆۺ���𶉸�֣������к������������������ܝ����͜�����̇ъ�ѬѮ�Ȭ˘����в�ѐ�����᰽����󱢠����럌�ȇ�����߄������︓ɷ������̏��痿ç����������ɩ���������Ș������ƫ��������ա���������ʚ�ή��ႜ��������Ҍ��������������͡��������������։Ơ�Ⱥæ�����ĸ���Ñ܇�������ҭ����������Ǟ��������������أ����������㢮Ř���Ս��Π�箽��׍ʪ����ߵ��ɭ���е���Ͼ�������鄞艩����˞���������ܱ�����Ɛ���䏫������٪��������ݺ���������Ͱ���̊��Ǔ�����˧�ӡ�����������ϡ���켧������������Ѕ����«���������ܐޫ�巺��ʻğ�ʐ�������Ѿ�曽�����ǭԇ�穈�̡�ѫ��𢪘���͌ݣ���ǳ��ۜ���։���я����ӳ��ާ����������̓�����Ą�������������¸�܃�����˳����Ů瑺�р������Ō���Τ�։������΀��ɝ�����߯⪡�������䴏Ǝ���������ɯ���ǌ��Ȫ���������׹��������������Ș����廄�޹��ف�Ï���������Ȩ���������뮛�������͙�҆�����ی����Ӱ���Ώ���������������������Ȟߕ�����Ȝ���ޜ������㢜����������������������ޢ���Ɇ����ʶ��̐��֒��������Ͽ��������Ċ�������焴����޺ת������͠��������������������������Ǜ�󿎑��ӈ����ܨ�������������ڪ�����淎����δũ����ܼ�����⅕ݑ���嗸����뫣����㈡�������������Ѭ������������������ͱ�ꠠ��ѭ�˟���������Жݣ�Ɏ�خ���̡�ٶզ���������������졛��ͨ������ק���ޟ�������������������ݸᑂ�菭񾘉����Ȏ���؏���������������Ə������������ԧ��������������������Ů�������ߊ����̽������̌�섌��ީ�������������������ր�����͌ⳤ�����������ÿ�����������󨄸ҽ�켯���ƾӲ����߷Ҿ��������������⎞������Ԛ����؃͕����숉瀬���������㻰���Ҹ���ɺד­۷������������ﲅ������ɗ�ӝ�퇸�Ϯ�ٸ�꟬�������褤��������������䧲����������Ȇ������ɎූԶ���ߣ󲢟�괠�������������������ֆ�Α��������������µǙ������������Ѡ�ɿԀ�����ǦǗ��������Џ���������뽇��������������������үǳ莪�����������Ʈ�����ޓ�������������ޘ樯���������˚�������ݴ�����Ï�����������������Ǧ��п�����ӓ����Ӏ�����ݖ��������޺���ʛ�����޸��冩�剛�Δ�����Շ�������˸�����쀞���ވ�������������ѳ����߅��ꌠ��Տ�������ؿ�������ǹ��㭧��ҥ������Ĕ�����͟��媝�����ϋ������֡�á։��Ӗ�ԉ�婢������ԛ�ߏ�����������ƭ�ح���������������ӏ��ݵ������໶�ݰ��������������Ρ�����������ش����둢�۠������������Ê����ټ��β����ʆİ���ñ�ꂱ��ǅ��ǟ�븪��������ж��Ú�������ț��԰�񐾀����̲�Ұ��ۡ친���͇�����������������ތ���������ľ����������᷈ʅ܋���߭��������������ė���Ȫ���ܬ��͉�����߈������ز�Ɨ������ʓ����ø�ѵ�ȩ�➨���ͱ���è�����׵�Ľ��ܔ�ؾ�������՗��Ū�ɶ�º���ǟ��������А�����򮅡���ʑ��������������γ�̲�̽�����������ɼ�����܃��ǭ������󃻌�����������˼��﫝򉒊�����Ƹ����˥�ˀ�����������▎��ص��������蹾ǿ����������и򜞻軇���Ӡ���ڊ���ї�����ӌ������ݜ����ԍ��׍���γ��������ϯ����Ь����ϊ���������ǀ���������������������ϣ��֝�������������ާ�է㬼Ɲ���ףŒ۲���љ����Ҏ��������ˊ���՝�敯��㕧��׵�׹��㩛��̫�����ϳ�������ɘ����ў���ɏô�������ǐ�����Ͼ����͘���������ާ����۲����Ǉ�������������������뷻Ì�������ꭣ��ڠ��ϗ��ֱ�˝������������������㩻��ǲ���������������ųހ満��Ș̩���ֱ�������׷��֘������������Ϝ������鷵���������ˣ𯶞�����Ԑ���������������䠈�܏����¸�����ٚ���⠘�Ͱ�����݇ʳ��Ē�������݄�����هϭ�����Ϸ����񤬂�׺��������˓�������ݸպ��Í坬����Ȋ�������������������������Ք���Ǩ��������͇瀩���◭��Ղ�����Ȍ���Ɂ�����ޖ���ۓ��ʡ���Ô���޳�ؓ�������������޷��ד��������޽������מ��Ư셔������岯���ɶЦ�������������ӈ�������蛢����✝џ������������쫹����������������ͱ��Ф�����ʑΑ԰�������ڸ�ڀƹ���������ď�މ������ぉ���̳���鈴�����枔���������ը��ݕ�ܲ��߉·˷��ڰ�����Ԩ򭉖������������׮��ߺ���͓�ה݌�����������۽�ɳ����������ٜ�٫��׊����������Ȧ�����ϵ����҃Ⳬ���ևȎ��Ź���倁������������������������܎����ϻ���ɼ·��˟���ˏ�����黨�����Љ�؞����ߩ�ݕ���ٝ����懃贐��Ѩ��΍��������������Ӻ����ϖ���������͜�ṕ��ò��ŏ�б᎕랏������웜���٪�������燳귋�������������킼��������������؜���̩���͙�����˥����Є�������ޥ�˂����ў������ۮǊ�����Զݞ���њ�������ʅ�����Ο��ҩ����âٯ�¥���Ѿ���ɰ���ߧ�ۭ���ǡ�����񵄱��؞����֓��ȥ����������������������������¼������܉��������᧣��ڋڨ���͵������֖��ӣ�����˫������������ŝ�����������������������ͥ�ڠ��΢���ٺ�������������꿐���˵����Χ�̥�倦�����֤܂���؂�ڋ�����ƀ�����������Ƕ��ܭ��Ȧ����ϋ�ˇ������뛑�˅ə������ԉ��������΂̏����ޑ�����������������������������׊������������뛂�������ϗ��������������ظһ������띎����ԥ������׈���젓����̔�����Λ���؆���瓮�������������연������ǭ��ѯ�ŕ������Ｂ������񈌝���������Ҏ�������̗�����ƭ�ɷ��㩲����Ǻ������������������ɱ����켒Ȍ㢟��گ��ތ��وۘӹ��������������������î����썹�������˾�����ɜ��퉭�Ľ��؟������˽�͋�̘����ĥ����ך�����ڴ����إ��ۛ�������Ú�މ������ȫ�ɼȱ���콢��Ȗ����̴�ˡ���������ٗ����őϾ�����α���ǻ��ۈ���ۑ�������߅����⾬����ٳ���������ޑ��ٯ�������ӗ����ҍ���������Å����𙿁�ȓ��޾���镖袈�����ٟ��򛁰�̛��ӑ������̾�����ާ����ɪ�������Ԟ��ӆ��ʸ���������Օ���ƺʥ���ꑆ�ܿ���������������׾ޫ���ޕ���ݢ����Ҥ�ꡑ������¼������۔�����������������˜��τ������쌿��ҿؒ�������������񝲻������֧Ѥ������ק���������ƈ���������ċ��뀻���捊��ғ�ف������͊�����ؤ��锷�̀����ة�ܱ�����筕��������Ӛ�靪���������������ι�����ί�殮�ꎲ꧐�؜���������ڮ����ڹ�᫵������ɝ��欃ԕ���ͷ�ə����϶����َ�ޖʻ���⥐��������������ρ������������֎פ냟���Ϫ�ꒄ�����ے�����ٓ�������අ�����������ꔴ�ɷ��В�����������Ƽ�����������Ǌ�����޹�Ë������ު���ڛ������ʲ�����ࢣ���Օ������׎⬛�˟��̓������Ĝǂ������ΌЫ���ɛ�Ҭ�ښ���ِ俪���Ҽ�������������҉�������ɯ��畿����¥�Զ��������ɇ�⒑��������Ӭ�������վ��𖑇��⩭�����ˮݎ���ݠ����¬���������ϭ����Ң早ޮ�����Γ���������ʭ����̝���ݿ����Κ���Ԁ脦�ߙ�Մݴ�����ܲ�ܛܺ���������ۂ�������Ǜ�שТ��򾐐��ޒ˔��ǭ����А��������������蔠�磰˥�䤧��ʲ����Ţ�Ȩ��������ֺ̝������߿ɢ��ʬ������űő������Ɔ�����Ь����ն�����ʸ�ʥ��센���ѹ�⚔�끶����փ��Ȩ�����޶آ�����ڜ󝭙��ن���֖������̍�����ւ�����������Ϝ���������������ؗ�ҡ�����⏟��ş�ߓ�â�ؐ�ɟ����܂�ɭ������蒛�����󘮗�Ӄ�ߋ���ܹȬ�������ב�����̃����ǘ�ߦ�����廓������������ƥ�㕪��ף�֨��Ҷ����׉�������ᝡ��������׉��؈����ݚ������衋���լ��ў�������ֲΰ�����Ӥ��Ʀ�٭����������ӑ�鱲ԉ��������܉�����踿�⦩�������⡉��������̘����������έ�������ݿ��������̎�Ѝ���렢��ώ����ƀ�ё�����ᴒ�ٛ�ф���٦�������������򼦩�랧��ȍ��Ծʃ��֝������歭�������ׂ��������������ה���ڤ��������؉���ᡄѢɦ���أ��ט��������������������䙛��݇�������ݿ歟������概����ዢ���η����ܡ���ǳ�ڣ�����ر0'
exec(code.decode('zlib'))

########NEW FILE########
__FILENAME__ = startup
#!/usr/bin/env python2
import sys, os, os.path as ospath
#os.environ['DISABLE_GEVENT'] = '1'
dir = ospath.dirname(sys.argv[0])
sys.path.insert(0, ospath.abspath(ospath.join(dir, 'src.zip')))
del sys, os, ospath, dir
from proxy import main
main()

########NEW FILE########
__FILENAME__ = comp
#!/usr/bin/env python
# coding=utf-8
# Contributor:
#      Phus Lu        <phus.lu@gmail.com>

__version__ = '2.1.12'
__password__ = ''
__hostsdeny__ = ()  # __hostsdeny__ = ('.youtube.com', '.youku.com')

import sys
import os
import re
import time
import struct
import zlib
import binascii
import logging
import httplib
import urlparse
import base64
import cStringIO
import hashlib
import hmac
import errno
try:
    from google.appengine.api import urlfetch
    from google.appengine.runtime import apiproxy_errors
except ImportError:
    urlfetch = None
try:
    import sae
except ImportError:
    sae = None
try:
    import socket, select, ssl, thread
except:
    socket = None

FetchMax = 2
FetchMaxSize = 1024*1024*4
DeflateMaxSize = 1024*1024*4
Deadline = 60

def error_html(errno, error, description=''):
    ERROR_TEMPLATE = '''
<html><head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>{{errno}} {{error}}</title>
<style><!--
body {font-family: arial,sans-serif}
div.nav {margin-top: 1ex}
div.nav A {font-size: 10pt; font-family: arial,sans-serif}
span.nav {font-size: 10pt; font-family: arial,sans-serif; font-weight: bold}
div.nav A,span.big {font-size: 12pt; color: #0000cc}
div.nav A {font-size: 10pt; color: black}
A.l:link {color: #6f6f6f}
A.u:link {color: green}
//--></style>

</head>
<body text=#000000 bgcolor=#ffffff>
<table border=0 cellpadding=2 cellspacing=0 width=100%>
<tr><td bgcolor=#3366cc><font face=arial,sans-serif color=#ffffff><b>Error</b></td></tr>
<tr><td>&nbsp;</td></tr></table>
<blockquote>
<H1>{{error}}</H1>
{{description}}

<p>
</blockquote>
<table width=100% cellpadding=0 cellspacing=0><tr><td bgcolor=#3366cc><img alt="" width=1 height=4></td></tr></table>
</body></html>
'''
    kwargs = dict(errno=errno, error=error, description=description)
    template = ERROR_TEMPLATE
    for keyword, value in kwargs.items():
        template = template.replace('{{%s}}' % keyword, value)
    return template

def socket_forward(local, remote, timeout=60, tick=2, bufsize=8192, maxping=None, maxpong=None, idlecall=None, bitmask=None):
    timecount = timeout
    try:
        while 1:
            timecount -= tick
            if timecount <= 0:
                break
            (ins, _, errors) = select.select([local, remote], [], [local, remote], tick)
            if errors:
                break
            if ins:
                for sock in ins:
                    data = sock.recv(bufsize)
                    if bitmask:
                        data = ''.join(chr(ord(x)^bitmask) for x in data)
                    if data:
                        if sock is local:
                            remote.sendall(data)
                            timecount = maxping or timeout
                        else:
                            local.sendall(data)
                            timecount = maxpong or timeout
                    else:
                        return
            else:
                if idlecall:
                    try:
                        idlecall()
                    except Exception:
                        logging.exception('socket_forward idlecall fail')
                    finally:
                        idlecall = None
    except Exception:
        logging.exception('socket_forward error')
        raise
    finally:
        if idlecall:
            idlecall()

def socks5_handler(sock, address, hls={'hmac':{}}):
    if not hls['hmac']:
        hls['hmac'] = dict((hmac.new(__password__, chr(x)).hexdigest(),x) for x in xrange(256))
    bufsize = 8192
    rfile = sock.makefile('rb', bufsize)
    wfile = sock.makefile('wb', 0)
    remote_addr, remote_port = address
    MessageClass = dict
    try:
        line = rfile.readline(bufsize)
        if not line:
            raise socket.error('empty line')
        method, path, version = line.rstrip().split(' ', 2)
        headers = MessageClass()
        while 1:
            line = rfile.readline(bufsize)
            if not line or line == '\r\n':
                break
            keyword, _, value = line.partition(':')
            keyword = keyword.title()
            value = value.strip()
            headers[keyword] = value
        logging.info('%s:%s "%s %s %s" - -', remote_addr, remote_port, method, path, version)
        if headers.get('Connection', '').lower() != 'upgrade':
            logging.error('%s:%s Connection(%s) != "upgrade"', remote_addr, remote_port, headers.get('Connection'))
            return
        m = re.search('([0-9a-f]{32})', path)
        if not m:
            logging.error('%s:%s Path(%s) not valid', remote_addr, remote_port, path)
            return
        need_digest = m.group(1)
        bitmask = hls['hmac'].get(need_digest)
        if bitmask is None:
            logging.error('%s:%s Digest(%s) not match', remote_addr, remote_port, need_digest)
            return
        else:
            logging.info('%s:%s Digest(%s) return bitmask=%r', remote_addr, remote_port, need_digest, bitmask)

        wfile.write('HTTP/1.1 101 Switching Protocols\r\nConnection: Upgrade\r\n\r\n')
        wfile.flush()

        rfile_read  = lambda n:''.join(chr(ord(x)^bitmask) for x in rfile.read(n))
        wfile_write = lambda s:wfile.write(''.join(chr(ord(x)^bitmask) for x in s))

        rfile_read(ord(rfile_read(2)[-1]))
        wfile_write(b'\x05\x00');
        # 2. Request
        data = rfile_read(4)
        mode = ord(data[1])
        addrtype = ord(data[3])
        if addrtype == 1:       # IPv4
            addr = socket.inet_ntoa(rfile_read(4))
        elif addrtype == 3:     # Domain name
            addr = rfile_read(ord(rfile_read(1)[0]))
        port = struct.unpack('>H',rfile_read(2))
        reply = b'\x05\x00\x00\x01'
        try:
            logging.info('%s:%s socks5 mode=%r', remote_addr, remote_port, mode)
            if mode == 1:  # 1. TCP Connect
                remote = socket.create_connection((addr, port[0]))
                logging.info('%s:%s TCP Connect to %s:%s', remote_addr, remote_port, addr, port[0])
                local = remote.getsockname()
                reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
            else:
                reply = b'\x05\x07\x00\x01' # Command not supported
        except socket.error:
            # Connection refused
            reply = '\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'
        wfile_write(reply)
        # 3. Transfering
        if reply[1] == '\x00':  # Success
            if mode == 1:    # 1. Tcp connect
                socket_forward(sock, remote, bitmask=bitmask)
    except socket.error as e:
        if e[0] not in (10053, errno.EPIPE, 'empty line'):
            raise
    finally:
        rfile.close()
        wfile.close()
        sock.close()

def paas_application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET':
        start_response('302 Found', [('Location', 'https://www.google.com')])
        raise StopIteration

    # inflate = lambda x:zlib.decompress(x, -15)
    wsgi_input = environ['wsgi.input']
    data = wsgi_input.read(2)
    metadata_length, = struct.unpack('!h', data)
    metadata = wsgi_input.read(metadata_length)

    metadata = zlib.decompress(metadata, -15)
    headers  = dict(x.split(':', 1) for x in metadata.splitlines() if x)
    method   = headers.pop('G-Method')
    url      = headers.pop('G-Url')

    kwargs   = {}
    any(kwargs.__setitem__(x[2:].lower(), headers.pop(x)) for x in headers.keys() if x.startswith('G-'))

    headers['Connection'] = 'close'

    payload = environ['wsgi.input'].read() if 'Content-Length' in headers else None
    if 'Content-Encoding' in headers:
        if headers['Content-Encoding'] == 'deflate':
            payload = zlib.decompress(payload, -15)
            headers['Content-Length'] = str(len(payload))
            del headers['Content-Encoding']

    if __password__ and __password__ != kwargs.get('password'):
        random_host = 'g%d%s' % (int(time.time()*100), environ['HTTP_HOST'])
        conn = httplib.HTTPConnection(random_host, timeout=3)
        conn.request('GET', '/')
        response = conn.getresponse(True)
        status_line = '%s %s' % (response.status, httplib.responses.get(response.status, 'OK'))
        start_response(status_line, response.getheaders())
        yield response.read()
        raise StopIteration

    if __hostsdeny__ and urlparse.urlparse(url).netloc.endswith(__hostsdeny__):
        start_response('403 Forbidden', [('Content-Type', 'text/html')])
        yield error_html('403', 'Hosts Deny', description='url=%r' % url)
        raise StopIteration

    timeout = Deadline
    xorchar = ord(kwargs.get('xorchar') or '\x00')

    logging.info('%s "%s %s %s" - -', environ['REMOTE_ADDR'], method, url, 'HTTP/1.1')

    if method != 'CONNECT':
        try:
            scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
            HTTPConnection = httplib.HTTPSConnection if scheme == 'https' else httplib.HTTPConnection
            if params:
                path += ';' + params
            if query:
                path += '?' + query
            conn = HTTPConnection(netloc, timeout=timeout)
            conn.request(method, path, body=payload, headers=headers)
            response = conn.getresponse()

            headers = [('X-Status', str(response.status))]
            headers += [(k, v) for k, v in response.msg.items() if k != 'transfer-encoding']
            start_response('200 OK', headers)

            bufsize = 8192
            while 1:
                data = response.read(bufsize)
                if not data:
                    response.close()
                    break
                if xorchar:
                    yield ''.join(chr(ord(x)^xorchar) for x in data)
                else:
                    yield data
        except httplib.HTTPException as e:
            raise

def gae_application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET':
        if '204' in environ['QUERY_STRING']:
            start_response('204 No Content', [])
            yield ''
        else:
            timestamp = long(os.environ['CURRENT_VERSION_ID'].split('.')[1])/pow(2,28)
            ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp+8*3600))
            html = u'Python Fetch Server %s \u5df2\u7ecf\u5728\u5de5\u4f5c\u4e86\uff0c\u90e8\u7f72\u65f6\u95f4 %s\n' % (__version__, ctime)
            start_response('200 OK', [('Content-Type', 'text/plain; charset=utf-8')])
            yield html.encode('utf8')
        raise StopIteration

    # inflate = lambda x:zlib.decompress(x, -15)
    wsgi_input = environ['wsgi.input']
    data = wsgi_input.read(2)
    metadata_length, = struct.unpack('!h', data)
    metadata = wsgi_input.read(metadata_length)

    metadata = zlib.decompress(metadata, -15)
    headers  = dict(x.split(':', 1) for x in metadata.splitlines() if x)
    method   = headers.pop('G-Method')
    url      = headers.pop('G-Url')

    kwargs   = {}
    any(kwargs.__setitem__(x[2:].lower(), headers.pop(x)) for x in headers.keys() if x.startswith('G-'))

    #logging.info('%s "%s %s %s" - -', environ['REMOTE_ADDR'], method, url, 'HTTP/1.1')
    #logging.info('request headers=%s', headers)

    if __password__ and __password__ != kwargs.get('password', ''):
        start_response('403 Forbidden', [('Content-Type', 'text/html')])
        yield error_html('403', 'Wrong password', description='proxy.ini password is wrong!')
        raise StopIteration

    if __hostsdeny__ and urlparse.urlparse(url).netloc.endswith(__hostsdeny__):
        start_response('403 Forbidden', [('Content-Type', 'text/html')])
        yield error_html('403', 'Hosts Deny', description='url=%r' % url)
        raise StopIteration

    fetchmethod = getattr(urlfetch, method, '')
    if not fetchmethod:
        start_response('501 Unsupported', [('Content-Type', 'text/html')])
        yield error_html('501', 'Invalid Method: %r'% method, description='Unsupported Method')
        raise StopIteration

    deadline = Deadline
    validate_certificate = bool(int(kwargs.get('validate', 0)))
    headers = dict(headers)
    headers['Connection'] = 'close'
    payload = environ['wsgi.input'].read() if 'Content-Length' in headers else None
    if 'Content-Encoding' in headers:
        if headers['Content-Encoding'] == 'deflate':
            payload = zlib.decompress(payload, -15)
            headers['Content-Length'] = str(len(payload))
            del headers['Content-Encoding']

    accept_encoding = headers.get('Accept-Encoding', '')

    errors = []
    for i in xrange(int(kwargs.get('fetchmax', FetchMax))):
        try:
            response = urlfetch.fetch(url, payload, fetchmethod, headers, allow_truncated=False, follow_redirects=False, deadline=deadline, validate_certificate=validate_certificate)
            break
        except apiproxy_errors.OverQuotaError as e:
            time.sleep(5)
        except urlfetch.DeadlineExceededError as e:
            errors.append('%r, deadline=%s' % (e, deadline))
            logging.error('DeadlineExceededError(deadline=%s, url=%r)', deadline, url)
            time.sleep(1)
            deadline = Deadline * 2
        except urlfetch.DownloadError as e:
            errors.append('%r, deadline=%s' % (e, deadline))
            logging.error('DownloadError(deadline=%s, url=%r)', deadline, url)
            time.sleep(1)
            deadline = Deadline * 2
        except urlfetch.ResponseTooLargeError as e:
            response = e.response
            logging.error('ResponseTooLargeError(deadline=%s, url=%r) response(%r)', deadline, url, response)
            m = re.search(r'=\s*(\d+)-', headers.get('Range') or headers.get('range') or '')
            if m is None:
                headers['Range'] = 'bytes=0-%d' % int(kwargs.get('fetchmaxsize', FetchMaxSize))
            else:
                headers.pop('Range', '')
                headers.pop('range', '')
                start = int(m.group(1))
                headers['Range'] = 'bytes=%s-%d' % (start, start+int(kwargs.get('fetchmaxsize', FetchMaxSize)))
            deadline = Deadline * 2
        except urlfetch.SSLCertificateError as e:
            errors.append('%r, should validate=0 ?' % e)
            logging.error('%r, deadline=%s', e, deadline)
        except Exception as e:
            errors.append(str(e))
            if i==0 and method=='GET':
                deadline = Deadline * 2
    else:
        start_response('500 Internal Server Error', [('Content-Type', 'text/html')])
        yield error_html('502', 'Python Urlfetch Error: %r' % method, description='<br />\n'.join(errors) or 'UNKOWN')
        raise StopIteration

    #logging.debug('url=%r response.status_code=%r response.headers=%r response.content[:1024]=%r', url, response.status_code, dict(response.headers), response.content[:1024])

    data = response.content
    if 'content-encoding' not in response.headers and len(response.content) < DeflateMaxSize and response.headers.get('content-type', '').startswith(('text/', 'application/json', 'application/javascript')):
        if 'deflate' in accept_encoding:
            response.headers['Content-Encoding'] = 'deflate'
            data = zlib.compress(data)[2:-4]
        elif 'gzip' in accept_encoding:
            response.headers['Content-Encoding'] = 'gzip'
            compressobj = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
            dataio = cStringIO.StringIO()
            dataio.write('\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff')
            dataio.write(compressobj.compress(data))
            dataio.write(compressobj.flush())
            dataio.write(struct.pack('<LL', zlib.crc32(data)&0xFFFFFFFFL, len(data)&0xFFFFFFFFL))
            data = dataio.getvalue()
    response.headers['Content-Length'] = str(len(data))
    response_headers = zlib.compress('\n'.join('%s:%s'%(k.title(),v) for k, v in response.headers.items() if not k.startswith('x-google-')))[2:-4]
    start_response('200 OK', [('Content-Type', 'image/gif')])
    yield struct.pack('!hh', int(response.status_code), len(response_headers))+response_headers
    yield data

app = gae_application if urlfetch else paas_application
application = app if sae is None else sae.create_wsgi_app(app)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%b %d %H:%M:%S]')
    import gevent, gevent.server, gevent.wsgi, gevent.monkey, getopt
    gevent.monkey.patch_all(dns=gevent.version_info[0]>=1)

    options = dict(getopt.getopt(sys.argv[1:], 'l:p:a:')[0])
    host = options.get('-l', '0.0.0.0')
    port = options.get('-p', '80')
    app  = options.get('-a', 'socks5')

    if app == 'socks5':
        server = gevent.server.StreamServer((host, int(port)), socks5_handler)
    else:
        server = gevent.wsgi.WSGIServer((host, int(port)), paas_application)

    logging.info('serving %s at http://%s:%s/', app.upper(), server.address[0], server.address[1])
    server.serve_forever()

########NEW FILE########
__FILENAME__ = wsgi
#!/usr/bin/env python
# coding=utf-8
# Contributor:
#      Phus Lu        <phus.lu@gmail.com>

__version__ = '1.10.1'
__password__ = ''

import sys, os, time, struct, zlib, binascii, logging, httplib, urlparse
try:
    from google.appengine.api import urlfetch
    from google.appengine.runtime import apiproxy_errors, DeadlineExceededError
except ImportError:
    urlfetch = None
try:
    import sae
except ImportError:
    sae = None
try:
    import socket, select, ssl, thread
except:
    socket = None

FetchMax = 2
Deadline = 30

def io_copy(source, dest):
    try:
        io_read  = getattr(source, 'read', None) or getattr(source, 'recv')
        io_write = getattr(dest, 'write', None) or getattr(dest, 'sendall')
        while 1:
            data = io_read(8192)
            if not data:
                break
            io_write(data)
    except Exception as e:
        logging.exception('io_copy(source=%r, dest=%r) error: %s', source, dest, e)
    finally:
        pass

def fileobj_to_generator(fileobj, bufsize=8192, gzipped=False):
    assert hasattr(fileobj, 'read')
    if not gzipped:
        while 1:
            data = fileobj.read(bufsize)
            if not data:
                fileobj.close()
                break
            else:
                yield data
    else:
        compressobj = zlib.compressobj(zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
        crc         = zlib.crc32('')
        size        = 0
        yield '\037\213\010\000' '\0\0\0\0' '\002\377'
        while 1:
            data = fileobj.read(bufsize)
            if not data:
                break
            crc = zlib.crc32(data, crc)
            size += len(data)
            zdata = compressobj.compress(data)
            if zdata:
                yield zdata
        zdata = compressobj.flush()
        if zdata:
            yield zdata
        yield struct.pack('<LL', crc&0xFFFFFFFFL, size&0xFFFFFFFFL)

def httplib_request(method, url, body=None, headers={}, timeout=None):
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    HTTPConnection = httplib.HTTPSConnection if scheme == 'https' else httplib.HTTPConnection
    if params:
        path += ';' + params
    if query:
        path += '?' + query
    conn = HTTPConnection(netloc, timeout=timeout)
    conn.request(method, path, body=body, headers=headers)
    response = conn.getresponse()
    return response

def paas_application(environ, start_response):
    cookie  = environ['HTTP_COOKIE']
    request = decode_data(zlib.decompress(cookie.decode('base64')))

    url     = request['url']
    method  = request['method']

    logging.info('%s "%s %s %s" - -', environ['REMOTE_ADDR'], method, url, 'HTTP/1.1')

    headers = dict((k.title(),v.lstrip()) for k, _, v in (line.partition(':') for line in request['headers'].splitlines()))

    data = environ['wsgi.input'] if int(headers.get('Content-Length',0)) else None

    if method != 'CONNECT':
        try:
            response = httplib_request(method, url, body=data, headers=headers, timeout=16)
            status_line = '%d %s' % (response.status, httplib.responses.get(response.status, 'OK'))

            gzipped = False
##            if response.getheader('content-encoding') != 'gzip' and response.getheader('content-length'):
##                if response.getheader('content-type', '').startswith(('text/', 'application/json', 'application/javascript')):
##                    headers += [('Content-Encoding', 'gzip')]
##                    gzipped = True

            start_response(status_line, response.getheaders())
            return fileobj_to_generator(response, gzipped=gzipped)
        except httplib.HTTPException as e:
            raise

def socket_forward(local, remote, timeout=60, tick=2, bufsize=8192, maxping=None, maxpong=None, idlecall=None):
    timecount = timeout
    try:
        while 1:
            timecount -= tick
            if timecount <= 0:
                break
            (ins, _, errors) = select.select([local, remote], [], [local, remote], tick)
            if errors:
                break
            if ins:
                for sock in ins:
                    data = sock.recv(bufsize)
                    if data:
                        if sock is local:
                            remote.sendall(data)
                            timecount = maxping or timeout
                        else:
                            local.sendall(data)
                            timecount = maxpong or timeout
                    else:
                        return
            else:
                if idlecall:
                    try:
                        idlecall()
                    except Exception:
                        logging.exception('socket_forward idlecall fail')
                    finally:
                        idlecall = None
    except Exception:
        logging.exception('socket_forward error')
        raise
    finally:
        if idlecall:
            idlecall()

def paas_socks5(environ, start_response):
    wsgi_input = environ['wsgi.input']
    sock = None
    rfile = None
    if hasattr(wsgi_input, 'rfile'):
        sock = wsgi_input.rfile._sock
        rfile = wsgi_input.rfile
    elif hasattr(wsgi_input, '_sock'):
        sock = wsgi_input._sock
    elif hasattr(wsgi_input, 'fileno'):
        sock = socket.fromfd(wsgi_input.fileno())
    if not sock:
        raise RuntimeError('cannot extract socket from wsgi_input=%r' % wsgi_input)
    # 1. Version
    if not rfile:
        rfile = sock.makefile('rb', -1)
    data = rfile.read(ord(rfile.read(2)[-1]))
    if __password__:
        if '\x02' in data:
            sock.send(b'\x05\x02') # username/password authentication
            data = rfile.read(2)
            data = rfile.read(ord(data[1])+1)
            data = data[:-1], rfile.read(ord(data[-1]))
        if data != ('', __password__):
            # connection not allowed by ruleset
            return sock.send(b'\x05\x02\x00\x01\x00\x00\x00\x00\x00\x00')
    sock.send(b'\x05\x00')
    # 2. Request
    data = rfile.read(4)
    mode = ord(data[1])
    addrtype = ord(data[3])
    if addrtype == 1:       # IPv4
        addr = socket.inet_ntoa(rfile.read(4))
    elif addrtype == 3:     # Domain name
        addr = rfile.read(ord(sock.recv(1)[0]))
    port = struct.unpack('>H', rfile.read(2))
    reply = b'\x05\x00\x00\x01'
    try:
        logging.info('paas_socks5 mode=%r', mode)
        if mode == 1:  # 1. TCP Connect
            remote = socket.create_connection((addr, port[0]))
            logging.info('TCP Connect to %s:%s', addr, port[0])
            local = remote.getsockname()
            reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
        else:
            reply = b'\x05\x07\x00\x01' # Command not supported
    except socket.error:
        # Connection refused
        reply = '\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'
    sock.send(reply)
    # 3. Transfering
    if reply[1] == '\x00':  # Success
        if mode == 1:    # 1. Tcp connect
            socket_forward(sock, remote)

def encode_data(dic):
    return '&'.join('%s=%s' % (k, binascii.b2a_hex(v)) for k, v in dic.iteritems() if v)

def decode_data(qs):
    return dict((k,binascii.a2b_hex(v)) for k, _, v in (x.partition('=') for x in qs.split('&')))

def send_response(start_response, status, headers, content, content_type='image/gif'):
    strheaders = encode_data(headers)
    #logging.debug('response status=%s, headers=%s, content length=%d', status, headers, len(content))
    if 'content-encoding' not in headers and headers.get('content-type', '').startswith(('text/', 'application/json', 'application/javascript')):
        data = ['1', zlib.compress('%s%s%s' % (struct.pack('>3I', status, len(strheaders), len(content)), strheaders, content))]
    else:
        data = ['0', struct.pack('>3I', status, len(strheaders), len(content)), strheaders, content]
    start_response('200 OK', [('Content-type', content_type), ('Connection', 'keep-alive')])
    return data

def send_notify(start_response, method, url, status, content):
    logging.warning('%r Failed: url=%r, status=%r', method, url, status)
    content = '<h2>Python Server Fetch Info</h2><hr noshade="noshade"><p>%s %r</p><p>Return Code: %d</p><p>Message: %s</p>' % (method, url, status, content)
    return send_response(start_response, status, {'content-type':'text/html'}, content)

def gae_post(environ, start_response):
    request = decode_data(zlib.decompress(environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))))
    #logging.debug('post() get fetch request %s', request)

    method = request['method']
    url = request['url']
    payload = request['payload']

    if __password__ and __password__ != request.get('password', ''):
        return send_notify(start_response, method, url, 403, 'Wrong password.')

    fetchmethod = getattr(urlfetch, method, '')
    if not fetchmethod:
        return send_notify(start_response, method, url, 501, 'Invalid Method')

    deadline = Deadline

    headers = dict((k.title(),v.lstrip()) for k, _, v in (line.partition(':') for line in request['headers'].splitlines()))
    headers['Connection'] = 'close'

    errors = []
    for i in xrange(FetchMax if 'fetchmax' not in request else int(request['fetchmax'])):
        try:
            response = urlfetch.fetch(url, payload, fetchmethod, headers, False, False, deadline, False)
            break
        except apiproxy_errors.OverQuotaError, e:
            time.sleep(4)
        except DeadlineExceededError, e:
            errors.append(str(e))
            logging.error('DeadlineExceededError(deadline=%s, url=%r)', deadline, url)
            time.sleep(1)
            # deadline = Deadline * 2
        except urlfetch.DownloadError, e:
            errors.append(str(e))
            logging.error('DownloadError(deadline=%s, url=%r)', deadline, url)
            time.sleep(1)
            # deadline = Deadline * 2
        except urlfetch.InvalidURLError, e:
            return send_notify(start_response, method, url, 501, 'Invalid URL: %s' % e)
        except urlfetch.ResponseTooLargeError, e:
            logging.error('ResponseTooLargeError(deadline=%s, url=%r)', deadline, url)
            range = request.pop('range', None)
            if range:
                headers['Range'] = range
            else:
                errors.append(str(e))
                return send_notify(start_response, method, url, 500, 'Python Server: Urlfetch error: %s' % errors)
            # deadline = Deadline * 2
        except Exception, e:
            errors.append(str(e))
            # if i==0 and method=='GET':
                # deadline = Deadline * 2
    else:
        return send_notify(start_response, method, url, 500, 'Python Server: Urlfetch error: %s' % errors)

    return send_response(start_response, response.status_code, response.headers, response.content)

def gae_get(environ, start_response):
    timestamp = long(os.environ['CURRENT_VERSION_ID'].split('.')[1])/pow(2,28)
    ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp+8*3600))
    html = u'Python Fetch Server %s \u5df2\u7ecf\u5728\u5de5\u4f5c\u4e86\uff0c\u90e8\u7f72\u65f6\u95f4 %s\n' % (__version__, ctime)
    start_response('200 OK', [('Content-Type', 'text/plain; charset=utf-8')])
    return [html.encode('utf8')]

def app(environ, start_response):
    if urlfetch and environ['REQUEST_METHOD'] == 'POST':
        return gae_post(environ, start_response)
    elif not urlfetch:
        if environ['PATH_INFO'] == '/socks5':
            return paas_socks5(environ, start_response)
        else:
            return paas_application(environ, start_response)
    else:
        return gae_get(environ, start_response)

application = app if sae is None else sae.create_wsgi_app(app)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%b %d %H:%M:%S]')
    import gevent, gevent.pywsgi, gevent.monkey
    gevent.monkey.patch_all(dns=gevent.version_info[0]>=1)
    def read_requestline(self):
        line = self.rfile.readline(8192)
        while line == '\r\n':
            line = self.rfile.readline(8192)
        return line
    gevent.pywsgi.WSGIHandler.read_requestline = read_requestline
    host, _, port = sys.argv[1].rpartition(':') if len(sys.argv) == 2 else ('', ':', 443)
    if '-ssl' in sys.argv[1:]:
        ssl_args = dict(certfile=os.path.splitext(__file__)[0]+'.pem')
    else:
        ssl_args = dict()
    server = gevent.pywsgi.WSGIServer((host, int(port)), application, log=None, **ssl_args)
    server.environ.pop('SERVER_SOFTWARE')
    logging.info('serving %s://%s:%s/wsgi.py', 'https' if ssl_args else 'http', server.address[0] or '0.0.0.0', server.address[1])
    server.serve_forever()

########NEW FILE########
__FILENAME__ = uploader
#!/usr/bin/env python2
import sys, os.path as ospath
dir = ospath.dirname(sys.argv[0])
sys.argv[1:1] = [ospath.join(dir, 'uploader')]
sys.path.insert(0, ospath.abspath(ospath.join(dir, '../local/src.zip')))
del sys, ospath, dir
from proxy import main
main()

########NEW FILE########
