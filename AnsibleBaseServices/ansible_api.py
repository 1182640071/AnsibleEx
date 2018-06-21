#-*- coding: utf-8 -*-
'''
python api.py 8090 指定端口运行方式

created by wangminglang
date 2018.6.15


对ansible的api进行封装,实现http/https接口
'''


import web,logging
import sys,json
from ansible_fun import AnsibleApi
from web.wsgiserver import CherryPyWSGIServer


reload(sys)
sys.setdefaultencoding('utf8')


CherryPyWSGIServer.ssl_certificate = "/root/ansibleTest/myserver.crt"
CherryPyWSGIServer.ssl_private_key = "/root/ansibleTest/myserver.key"

urls = (
    '/ansible/api1.0','AnsibleOne',
)


class AnsibleOne:

    def GET(self):
        return 'Please Send Post Request'

    def POST(self):
        web.header('Content-Type', 'application/json;charset=UTF-8')
        data = web.data()
        info = {}
        try:
            info = eval(data)
            name = "xx"
            hosts = info["host"]
            user = info["user"]
            passwd = info["passwd"]
            module = info['module']
            args = info['arg']
        except:
            return "the type of data error"

        Aapi = AnsibleApi()
        rs = Aapi.fun( user , passwd , hosts , module , args)
        return self.analyse(rs)

    def analyse(self , list):
        try:
            dictRs = {}
            dictValue = {}
            for i in list:
                dictRs[i.keys()[0]] = str(i.keys()[0])+'_key'
                dictValue[i.keys()[0]] = i[i.keys()[0]]['stdout']

            rs = json.dumps(dictRs)

            for i in dictRs.keys():
                rs = rs.replace(str(i)+'_key', dictValue[i])
        except Exception , e:
            print e
            rs = '{}'
        return rs


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    web.application(urls,globals()).run()