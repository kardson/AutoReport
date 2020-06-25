import sys
import requests
import time
import base64
import json
from lxml import etree
import urllib.parse

loginURL = "https://newsso.shu.edu.cn/login"
reportURL = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=1"
homeURL = "https://selfreport.shu.edu.cn"
# post

class postBody(object):
    def __init__(self, date=time.strftime("%Y-%m-%d", time.localtime()), # be aware of your sever timezone should be set as utc+8
                        bodyStatus="良好", 
                        symptom="", 
                        temperature="36.2",
                        QRCodeColor="绿色", 
                        meal=["早餐", "中餐", "晚餐"],
                        timeMark=""):
        self.date = date
        self.bodyStatus = bodyStatus
        self.symptom = symptom
        self.temperature = temperature
        self.QRCodeColor = QRCodeColor
        self.meal = meal
        self.timeMark = "上午" if timeMark else "下午"
        self.f_state = None
        self.viewstate = None
        self.viewstategenerator = None
        self.submitData = None

    def set(self):
        self.f_state = {
            "p1_BaoSRQ": {
                "Text": self.date
            },
            "p1_DangQSTZK": {
                "F_Items": [
                    ["良好", "良好", 1],
                    ["不适", "不适", 1]
                ],
                "SelectedValue": self.bodyStatus
            },
            "p1_ZhengZhuang": {
                "Hidden": True,
                "F_Items": [
                    ["感冒", "感冒", 1],
                    ["咳嗽", "咳嗽", 1],
                    ["发热", "发热", 1]
                ],
                "SelectedValueArray": []
            },
            "p1_TiWen": {
                "Text": self.temperature
            },
            "p1_SuiSM": {
                "SelectedValue": self.QRCodeColor,
                "F_Items": [
                    ["红色", "红色", 1],
                    ["黄色", "黄色", 1],
                    ["绿色", "绿色", 1]
                ]
            },
            "p1_ShiFJC": {
                "SelectedValueArray": self.meal,
                "F_Items": [
                    ["早餐", "早餐", 1],
                    ["午餐", "午餐", 1],
                    ["晚餐", "晚餐", 1]
                ]
            },
            "p1_ctl00_btnSubmit": {
                "Hidden": False
            },
            "p1": {
                "Title": f"每日两报（{self.timeMark}）",
                "IFrameAttributes": {}
            }
        }


    def get(self):
        self.submitData = {
            "__EVENTTARGET": "p1$ctl00$btnSubmit",
            "__EVENTARGUMENT": "",
            "__VIEWSTATEGENERATOR": "DC4D08A3",
            "p1$ChengNuo": "p1_ChengNuo",
            "p1$BaoSRQ": self.date,
            "p1$DangQSTZK": self.bodyStatus,
            "p1$TiWen": self.temperature,
            "p1$SuiSM": self.QRCodeColor,
            "p1$ShiFJC": self.meal[0],
            "p1$ShiFJC": self.meal[1],
            "p1$ShiFJC": self.meal[2],
            "F_TARGET": "p1_ctl00_btnSubmit",
            "p1_Collapsed": "false",
            "F_STATE": base64.b64encode(json.dumps(self.F_STATE).encode)
        }

class AutoReport(object):

    def __init__(self, id, password, timeMark):
        self.session = requests.Session()
        self.id = id
        self.password = password
        self.timeMark = timeMark
    
    def _login(self):
        self.session.headers.update({"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
        self.session.headers.update({"Accept-Language": "zh-cn"})
        self.session.headers.update({"Accept-Encoding": "gzip, deflate, br"})
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
        self.session.headers.update({"Connection": "keep-alive"})
        self.session.headers.update({"Host": "newsso.shu.edu.cn"})

        # retrieve cookie
        login = self.session.get(loginURL)

        # post data
        data = {
            "username": self.id,
            "password": self.password,
            "login_submit": "登录/Login"
        }
        self.session.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
        self.session.headers.update({"Referer": "https://newsso.shu.edu.cn/login"})
        self.session.headers.update({"Origin": "https://newsso.shu.edu.cn"})
        loginPost = self.session.post(loginURL, data=urllib.parse.urlencode(data), timeout=10, allow_redirects=False)
        self.session.headers.pop("Content-Type")
        self.session.headers.pop("Origin")
        loginPostRedirect = self.session.get("https://newsso.shu.edu.cn"+loginPost.headers["Location"], timeout=10)
        self.session.headers.pop("Referer")

        self.session.headers.update({"Host": "selfreport.shu.edu.cn"})
        mainpage1 = self.session.get(homeURL+"/", allow_redirects=False)
        mainpage2 = self.session.get(homeURL+mainpage1.headers["Location"], allow_redirects=False)
        self.session.headers.update({"Host": "newsso.shu.edu.cn"})
        mainpage3 = self.session.get(mainpage2.headers["Location"], allow_redirects=False)
        self.session.headers.update({"Host": "selfreport.shu.edu.cn"})
        mainpage4 = self.session.get(mainpage3.headers["Location"])
        # resp3 = self.session.get("https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=1", timeout=10)
        html = etree.HTML(resp.text)
        viewstate = html.xpath('string(//input[@id="__viewstate"]/@value)')
        viewstategenerator = html.xpath('string(//input[@id="__viewstategenerator"]/@value')
        return

    def generateData(self):
        resp = self.session.get("https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=2")
        html = etree.HTML(resp.text)
        viewstate = html.xpath('string(//input[@id="__viewstate"]/@value)')
        viewstategenerator = html.xpath('string(//input[@id="__viewstategenerator"]/@value')
        return

    def postData(self):
        pass
        

if __name__ == "__main__":
    automation = AutoReport(sys.argv[1], sys.argv[2], 1)
    automation._login()