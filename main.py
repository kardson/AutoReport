import sys
import requests
import time
import base64
import json
from lxml import etree
import urllib.parse

# post

class postBody(object):
    def __init__(self, date=time.strftime("%Y-%m-%d", time.localtime()), # be aware of your sever timezone should be set as utc+8
                        bodyStatus="良好", 
                        symptom="", 
                        temperature="36.2",
                        QRCodeColor="绿色", 
                        meal=["早餐", "中餐", "晚餐"],
                        timeMark="上午" if time.strftime("%p", time.localtime())=="AM" else "下午",
                        viewstate=None,
                        viewstategenerator=None):
        self.date = date
        self.bodyStatus = bodyStatus
        self.symptom = symptom
        self.temperature = temperature
        self.QRCodeColor = QRCodeColor
        self.meal = meal
        self.timeMark = timeMark
        self.viewstate = viewstate
        self.viewstategenerator = viewstategenerator
        self.f_state = None
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
        self.set()
        self.submitData = {
            # actually there's no need for the parameters about state
            "__EVENTTARGET": "p1$ctl00$btnSubmit",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": self.viewstate,
            "__VIEWSTATEGENERATOR": self.viewstategenerator,
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
            "F_STATE": base64.b64encode(json.dumps(self.f_state).encode())
        }
        return self.submitData

class AutoReport(object):

    loginURL = "https://newsso.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE2MDQzNjk1ODc2NTA1NDYxMzQsInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6IldVSFdmcm50bldZSFpmelE1UXZYVUNWeSIsInNjb3BlIjoiMSIsInJlZGlyZWN0VXJpIjoiaHR0cHM6Ly9zZWxmcmVwb3J0LnNodS5lZHUuY24vTG9naW5TU08uYXNweD9SZXR1cm5Vcmw9JTJmIiwic3RhdGUiOiIifQ=="
    reportURL = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=%s"
    homeURL = "https://selfreport.shu.edu.cn"
    timeMarkDict = {"晨报": 1, "晚报": 2}

    def __init__(self, id, password, tempreture):
        self.session = requests.Session()
        self.id = id
        self.password = password
        self.tempreture = tempreture
        # self.timeMark = timeMark
    
    def _login(self):
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
        data = {
            "username": self.id,
            "password": self.password,
            "login_submit": ""
        }
        self.session.post(self.loginURL, data=data)
        # self.session.get("https://newsso.shu.edu.cn/oauth/authorize?response_type=code&client_id=WUHWfrntnWYHZfzQ5QvXUCVy&redirect_uri=https%3a%2f%2fselfreport.shu.edu.cn%2fLoginSSO.aspx%3fReturnUrl%3d%252fDefault.aspx&scope=1")
        # self.session.get("https://newsso.shu.edu.cn/oauth/authorize?response_type=code&client_id=WUHWfrntnWYHZfzQ5QvXUCVy&redirect_uri=https%3a%2f%2fselfreport.shu.edu.cn%2fLoginSSO.aspx%3fReturnUrl%3d%252FXueSFX%252FHalfdayReport.aspx%253Ft%253D1%26t%3d1&scope=1")
        return 1

    def _generateData(self):
        self._login()
        URL = self.reportURL % ("1" if time.strftime("%p", time.localtime())=="AM" else "2")
        resp = self.session.get(URL)
        html = etree.HTML(resp.text)
        viewstate = html.xpath('string(//input[@id="__VIEWSTATE"]/@value)')
        viewstategenerator = html.xpath('string(//input[@id="__VIEWSTATEGENERATOR"]/@value)')
        submit_data = postBody(temperature=self.tempreture, viewstate=viewstate, viewstategenerator=viewstategenerator).get()
        return submit_data

    def _postData(self):
        data = self._generateData()
        self.session.headers.update({"X-Requested-With": "XMLHttpRequest"})
        self.session.headers.update({"X-FineUI-Ajax": "true"})
        self.session.headers.update({"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
        URL = self.reportURL % ("1" if time.strftime("%p", time.localtime()) == "AM" else "2")
        resp = self.session.post(URL, data=data)
        return 1

    def do(self):
        self._postData()
        return 1
        

if __name__ == "__main__":
    automation = AutoReport(sys.argv[1], sys.argv[2], sys.argv[3])
    automation.do()