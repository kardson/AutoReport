import requests
import time
import base64
import json

loginURL = "https://newsso.shu.edu.cn/login"
reportURL = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=1"
post

class postBody(object):
    def __init__(self, date=time.strftime("%Y-%m-%d", time.localtime()), # be aware of your sever timezone should be set as utc+8
                        bodyStatus="良好", 
                        symptom="", 
                        temperature="36.2",
                        QRCodeColor="绿色", 
                        meal=["早餐", "中餐", "晚餐"]):
        self.date = date
        self.bodyStatus = bodyStatus
        self.symptom = symptom
        self.temperature = temperature
        self.QRCodeColor = QRCodeColor
        self.meal = meal
        self.submitData = None

    def set(self):
        self.F_STATE = {
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
                "Title": "每日两报（上午）",
                "IFrameAttributes": {}
            }
        }
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
            "p1_Collapsed": "false"
            "F_STATE": base64.b64encode(json.dumps(self.F_STATE).encode)
        }

    def get(self):
        self

class AutoReport(object):

    def __init__(self, id, password, timeMark):
        self.session = requests.Session()
        self.id = id
        self.password = password
        self.timeMark = timeMark
    
    def _login(self):
        data = {
            "username": self.id,
            "password": self.password,
            "login_submit": "登录/Login"
        }
        # self.session.post(loginURL, data=data, timeout=5)
        resp = self.session.get("https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=1")
        return
    
    def postData(self):
        
        

if __name__ == "__main__":
    automation = AutoReport("*", "*", 1)
    automation._login()