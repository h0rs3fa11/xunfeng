# coding:utf-8
# author:wolf
import urllib.request, urllib.error, urllib.parse
import base64


def get_plugin_info():
    plugin_info = {
        "name": "Tomcat弱口令",
        "info": "攻击者通过此漏洞可以登陆管理控制台，通过部署功能可直接获取服务器权限。",
        "level": "高危",
        "type": "弱口令",
        "author": "wolf@YSRC",
        "url": "http://huaidan.org/archives/1207.html",
        "keyword": "tag:tomcat",
        "source": 1
    }
    return plugin_info


def check(ip, port, timeout):
    error_i = 0
    flag_list = ['/manager/html/reload', 'Tomcat Web Application Manager']
    user_list = ['admin', 'manager', 'tomcat', 'apache', 'root']
    for user in user_list:
        for pass_ in PASSWORD_DIC:
            try:
                pass_ = str(pass_.replace('{user}', user))
                login_url = 'http://' + ip + ":" + str(port) + '/manager/html'
                request = urllib.request.Request(login_url)
                auth_str_temp = user + ':' + pass_
                auth_str = base64.b64encode(auth_str_temp)
                request.add_header('Authorization', 'Basic ' + auth_str)
                res = urllib.request.urlopen(request, timeout=timeout)
                res_code = res.code
                res_html = res.read()
            except urllib.error.HTTPError as e:
                res_code = e.code
                res_html = e.read()
            except urllib.error.URLError as e:
                error_i += 1
                if error_i >= 3: return
                continue
            if int(res_code) == 404: return
            if int(res_code) == 401 or int(res_code) == 403: continue
            for flag in flag_list:
                if flag in res_html:
                    return 'Tomcat弱口令 %s:%s' % (user, pass_)
