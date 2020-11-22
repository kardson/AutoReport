import sys
import requests
import time
import base64
import json
from lxml import etree
# import urllib.parse
# post

class postBody(object):
    def __init__(self, date=time.strftime("%Y-%m-%d", time.localtime()), # be aware of your sever timezone should be set as utc+8
                        bodyStatus="良好",
                        temperature="36.2",
                        QRCodeColor="绿色",
                        timeMark="上午" if time.strftime("%p", time.localtime())=="AM" else "下午",
                        viewstate=None,
                        viewstategenerator=None):
        self.date = date
        self.bodyStatus = bodyStatus
        self.temperature = temperature
        self.QRCodeColor = QRCodeColor
        self.timeMark = timeMark
        self.viewstate = viewstate
        self.viewstategenerator = viewstategenerator
        self.f_state = None
        self.submitData = None

    def set(self):
        self.f_state = {
            "p1_BaoSRQ": {"Text": self.date},
            "p1_DangQSTZK": {"F_Items": [["良好", "良好", 1], ["不适", "不适", 1]], "SelectedValue": self.bodyStatus},
            "p1_ZhengZhuang": {"Hidden": True, "F_Items": [["感冒", "感冒", 1], ["咳嗽", "咳嗽", 1], ["发热", "发热", 1]],
                               "SelectedValueArray": []},
            "p1_TiWen": {"Text": self.temperature},
            "p1_ZaiXiao": {"SelectedValue": "宝山",
                           "F_Items": [["不在校", "不在校", 1], ["宝山", "宝山校区", 1], ["延长", "延长校区", 1], ["嘉定", "嘉定校区", 1],
                                       ["新闸路", "新闸路校区", 1]]},
            "p1_ddlSheng": {"F_Items": [["-1", "选择省份", 1, "", ""], ["北京", "北京", 1, "", ""], ["天津", "天津", 1, "", ""],
                                        ["上海", "上海", 1, "", ""], ["重庆", "重庆", 1, "", ""], ["河北", "河北", 1, "", ""],
                                        ["山西", "山西", 1, "", ""], ["辽宁", "辽宁", 1, "", ""], ["吉林", "吉林", 1, "", ""],
                                        ["黑龙江", "黑龙江", 1, "", ""], ["江苏", "江苏", 1, "", ""], ["浙江", "浙江", 1, "", ""],
                                        ["安徽", "安徽", 1, "", ""], ["福建", "福建", 1, "", ""], ["江西", "江西", 1, "", ""],
                                        ["山东", "山东", 1, "", ""], ["河南", "河南", 1, "", ""], ["湖北", "湖北", 1, "", ""],
                                        ["湖南", "湖南", 1, "", ""], ["广东", "广东", 1, "", ""], ["海南", "海南", 1, "", ""],
                                        ["四川", "四川", 1, "", ""], ["贵州", "贵州", 1, "", ""], ["云南", "云南", 1, "", ""],
                                        ["陕西", "陕西", 1, "", ""], ["甘肃", "甘肃", 1, "", ""], ["青海", "青海", 1, "", ""],
                                        ["内蒙古", "内蒙古", 1, "", ""], ["广西", "广西", 1, "", ""], ["西藏", "西藏", 1, "", ""],
                                        ["宁夏", "宁夏", 1, "", ""], ["新疆", "新疆", 1, "", ""], ["香港", "香港", 1, "", ""],
                                        ["澳门", "澳门", 1, "", ""], ["台湾", "台湾", 1, "", ""]],
                            "SelectedValueArray": ["上海"]},
            "p1_ddlShi": {"Enabled": True, "F_Items": [["-1", "选择市", 1, "", ""], ["上海市", "上海市", 1, "", ""]],
                          "SelectedValueArray": ["上海市"]},
            "p1_ddlXian": {"Enabled": True,
                           "F_Items": [["-1", "选择县区", 1, "", ""], ["黄浦区", "黄浦区", 1, "", ""], ["卢湾区", "卢湾区", 1, "", ""],
                                       ["徐汇区", "徐汇区", 1, "", ""], ["长宁区", "长宁区", 1, "", ""], ["静安区", "静安区", 1, "", ""],
                                       ["普陀区", "普陀区", 1, "", ""], ["虹口区", "虹口区", 1, "", ""], ["杨浦区", "杨浦区", 1, "", ""],
                                       ["宝山区", "宝山区", 1, "", ""], ["闵行区", "闵行区", 1, "", ""], ["嘉定区", "嘉定区", 1, "", ""],
                                       ["松江区", "松江区", 1, "", ""], ["金山区", "金山区", 1, "", ""], ["青浦区", "青浦区", 1, "", ""],
                                       ["奉贤区", "奉贤区", 1, "", ""], ["浦东新区", "浦东新区", 1, "", ""],
                                       ["崇明区", "崇明区", 1, "", ""]], "SelectedValueArray": ["宝山区"]},
            "p1_FengXDQDL": {"SelectedValue": "否", "F_Items": [["是", "是", 1], ["否", "否", 1]]},
            "p1_TongZWDLH": {"SelectedValue": "否", "F_Items": [["是", "是", 1], ["否", "否", 1]]},
            "p1_XiangXDZ": {"Text": "上海市宝山区上大路99号"},
            "p1_QueZHZJC": {"F_Items": [["是", "是", 1, "", ""], ["否", "否", 1, "", ""]], "SelectedValueArray": ["否"]},
            "p1_DangRGL": {"SelectedValue": "否", "F_Items": [["是", "是", 1], ["否", "否", 1]]},
            "p1_GeLSM": {"Hidden": True, "IFrameAttributes": {}},
            "p1_GeLFS": {"Required": False, "Hidden": True, "F_Items": [["居家隔离", "居家隔离", 1], ["集中隔离", "集中隔离", 1]],
                         "SelectedValue": "null"},
            "p1_GeLDZ": {"Hidden": True},
            "p1_CengFWH": {
                "Label": "2020年9月27日后是否在中高风险地区逗留过<span style='color:red;'>（天津东疆港区瞰海轩小区、天津汉沽街、天津中心渔港冷链物流区A区和B区、浦东营前村、安徽省阜阳市颍上县慎城镇张洋小区、浦东周浦镇明天华城小区、浦东祝桥镇新生小区、浦东张江镇顺和路126弄小区、内蒙古满洲里东山街道办事处、内蒙古满洲里北区街道）</span>",
                "F_Items": [["是", "是", 1], ["否", "否", 1]], "SelectedValue": "否"},
            "p1_CengFWH_RiQi": {"Hidden": True},
            "p1_CengFWH_BeiZhu": {"Hidden": True},
            "p1_JieChu": {
                "Label": "11月08日至11月22日是否与来自中高风险地区发热人员密切接触<span style='color:red;'>（天津东疆港区瞰海轩小区、天津汉沽街、天津中心渔港冷链物流区A区和B区、浦东营前村、安徽省阜阳市颍上县慎城镇张洋小区、浦东周浦镇明天华城小区、浦东祝桥镇新生小区、浦东张江镇顺和路126弄小区、内蒙古满洲里东山街道办事处、内蒙古满洲里北区街道）</span>",
                "SelectedValue": "否", "F_Items": [["是", "是", 1], ["否", "否", 1]]},
            "p1_JieChu_RiQi": {"Hidden": True},
            "p1_JieChu_BeiZhu": {"Hidden": True},
            "p1_TuJWH": {
                "Label": "11月08日至11月22日是否乘坐公共交通途径中高风险地区<span style='color:red;'>（天津东疆港区瞰海轩小区、天津汉沽街、天津中心渔港冷链物流区A区和B区、浦东营前村、安徽省阜阳市颍上县慎城镇张洋小区、浦东周浦镇明天华城小区、浦东祝桥镇新生小区、浦东张江镇顺和路126弄小区、内蒙古满洲里东山街道办事处、内蒙古满洲里北区街道）</span>",
                "SelectedValue": "否", "F_Items": [["是", "是", 1], ["否", "否", 1]]},
            "p1_TuJWH_RiQi": {"Hidden": True},
            "p1_TuJWH_BeiZhu": {"Hidden": True},
            "p1_JiaRen": {"Label": "11月08日至11月22日家人是否有发热等症状"},
            "p1_JiaRen_BeiZhu": {"Hidden": True},
            "p1_SuiSM": {"SelectedValue": "绿色", "F_Items": [["红色", "红色", 1], ["黄色", "黄色", 1], ["绿色", "绿色", 1]]},
            "p1_LvMa14Days": {"SelectedValue": "是", "F_Items": [["是", "是", 1], ["否", "否", 1]]},
            "p1": {"Title": f"每日两报（{self.timeMark}）", "IFrameAttributes": {}}
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
            "p1$ZaiXiao": "宝山",
            "p1$ddlSheng$Value": "上海",
            "p1$ddlSheng": "上海",
            "p1$ddlShi$Value": "上海市",
            "p1$ddlShi": "上海市",
            "p1$ddlXian$Value": "宝山区",
            "p1$ddlXian": "宝山区",
            "p1$FengXDQDL": "否",
            "p1$TongZWDLH": "否",
            "p1$XiangXDZ": "上海市宝山区上大路99号",
            "p1$QueZHZJC$Value": "否",
            "p1$QueZHZJC": "否",
            "p1$DangRGL": "否",
            "p1$GeLDZ": "",
            "p1$CengFWH": "否",
            "p1$CengFWH_RiQi": "",
            "p1$CengFWH_BeiZhu": "",
            "p1$JieChu": "否",
            "p1$JieChu_RiQi": "",
            "p1$JieChu_BeiZhu": "",
            "p1$TuJWH": "否",
            "p1$TuJWH_RiQi": "",
            "p1$TuJWH_BeiZhu": "",
            "p1$JiaRen_BeiZhu": "",
            "p1$SuiSM": self.QRCodeColor,
            "p1$LvMa14Days": "是",
            "p1$Address2": "",
            "F_TARGET": "p1_ctl00_btnSubmit",
            "p1_GeLSM_Collapsed": "false",
            "p1_Collapsed": "false",
            "F_TARGET": "p1_ctl00_btnSubmit",
            "p1_Collapsed": "false",
            "F_STATE": base64.b64encode(json.dumps(self.f_state).encode())
        }
        return self.submitData

class AutoReport(object):

    loginURL = "https://newsso.shu.edu.cn/login/"
    reportURL = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=%s"
    homeURL = "https://selfreport.shu.edu.cn"
    timeMarkDict = {"晨报": 1, "晚报": 2}

    def __init__(self, id, password, tempreture):
        self.session = requests.Session()
        self.id = id
        self.password = password
        self.tempreture = tempreture
        # self.timeMark = timeMark

    def _generateLoginURL(self):
        param = {
            "timestamp": time.time_ns(),
            "responseType": "code",
            "clientId": "WUHWfrntnWYHZfzQ5QvXUCVy",
            "scope": "1",
            "redirectUri": "https://selfreport.shu.edu.cn/LoginSSO.aspx?ReturnUrl=%2f",
            "state": ""
        }
        loginURL = self.loginURL + str(base64.b64encode(json.dumps(param).encode()), encoding='utf8')
        return loginURL
    
    def _login(self):
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
        data = {
            "username": self.id,
            "password": self.password,
            "login_submit": ""
        }
        self.session.post(self._generateLoginURL(), data=data)
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