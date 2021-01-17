import sys, time, base64, json
from selenium import webdriver

class AutoReport(object):

    loginURL = "https://newsso.shu.edu.cn/login/"
    mainpageURL = "https://selfreport.shu.edu.cn"
    reportURL = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=%s"
    historyURL = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport_History.aspx"
    historyReportURL = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?day=%s&t=%s"
    timeMarkDict = {"晨报": 1, "晚报": 2}

    def __init__(self, id="", password="", temperature="36.2"):
        self.id = id
        self.password = password
        self.temperature = temperature
        self.timeMark = "晨报" if time.strftime("%p", time.localtime())=="AM" else "晚报"
        self.date = time.strftime("%Y-%m-%d", time.localtime())
        self.__browser = None
        # TODO logger need to be added

    def __generateLoginURL(self):
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

    def __invokeBrowser(self):
        option = webdriver.ChromeOptions()
        # add --no-sandbox to enalbe chrome running under root account
        option.add_argument("--no-sandbox")
        option.add_argument("--headless")
        option.add_argument("--disable-gpu")
        option.add_argument("--disable-dev-shm-usage")
        # self.__browser = webdriver.Chrome("./chromedriver", options=option)
        self.__browser = webdriver.Chrome(options=option)
        return 1

    def __delBrowser(self):
        self.__browser.close()
        self.__browser.quit()
        
    # TODO handle the situation of wrong id or password
    def login(self):
        self.__browser.get(self.__generateLoginURL())
        self.__browser.implicitly_wait(1)
        idBlock = self.__browser.find_element_by_id("username")
        idBlock.send_keys(self.id)
        passwordBlock = self.__browser.find_element_by_id("password")
        passwordBlock.send_keys(self.password)
        button = self.__browser.find_element_by_id("submit")
        button.click()
        self.__browser.implicitly_wait(1)
        try:
            errorMsg = self.__browser.find_element_by_class_name("showMessage")
        except:
            return 1
        else:
            return 0


    def submitData(self, date, timeMark):
        try:
            URL = self.historyReportURL % (date, self.timeMarkDict[timeMark])
            self.__browser.get(URL)
            self.__browser.implicitly_wait(1)
            # Promise
            undertakeCheckBox = self.__browser.find_element_by_id("p1_ChengNuo-inputEl-icon")
            undertakeClassAttributes = undertakeCheckBox.get_attribute("class")
            if "f-checked" not in undertakeClassAttributes: undertakeCheckBox.click()
            # Body Status
            bodyStatus = self.__browser.find_element_by_id("fineui_0-inputEl-icon")
            bodyStatusClassAttributes = bodyStatus.get_attribute("class")
            if "f-checked" not in bodyStatusClassAttributes: bodyStatus.click()
            # temperature
            temperature = self.__browser.find_element_by_id("p1_TiWen-inputEl")
            temperature.send_keys(self.temperature)
            # on campus or not (Baoshan)
            campusButton = self.__browser.find_element_by_id("fineui_6-inputEl-icon")
            campusButton.click()
            # province, city, district
            province = self.__browser.find_element_by_name("p1$ddlSheng$Value")
            self.__browser.execute_script("arguments[0].setAttribute('value', '上海')", province)
            city = self.__browser.find_element_by_name("p1$ddlShi$Value")
            self.__browser.execute_script("arguments[0].setAttribute('value', '上海市')", city)
            district = self.__browser.find_element_by_name("p1$ddlXian$Value")
            self.__browser.execute_script("arguments[0].setAttribute('value', '宝山区')", district)
            # stay in high-risk area(no)
            stayButton = self.__browser.find_element_by_id("fineui_12-inputEl-icon")
            stayButton.click()
            # live with people from high-risk area(no)
            liveButton = self.__browser.find_element_by_id("fineui_14-inputEl-icon")
            liveButton.click()
            # address
            address = self.__browser.find_element_by_id("p1_XiangXDZ-inputEl")
            address.clear()
            address.send_keys("上海市宝山区上大路99号")
            # contact with people infected
            contactSelection = self.__browser.find_element_by_name("p1$QueZHZJC$Value")
            self.__browser.execute_script("arguments[0].setAttribute('value', '否')", contactSelection)
            # close contact(no)
            contactButton = self.__browser.find_element_by_id("fineui_18-inputEl-icon")
            contactButton.click()
            # pass by(no)
            passbyButton = self.__browser.find_element_by_id("fineui_20-inputEl-icon")
            passbyButton.click()
            # helth code color(green)
            codeButton = self.__browser.find_element_by_id("fineui_26-inputEl-icon")
            codeButton.click()
            # helth code color consistence in 14 days(yes)
            codeConsistenceButton = self.__browser.find_element_by_id("fineui_27-inputEl-icon")
            codeConsistenceButton.click()
            # QRCodeColorRadiusButton = self.__browser.find_element_by_id("fineui_7-inputEl-icon")
            # QRCodeColorRadiusButton.click()
            # breakfastCheckBox = self.__browser.find_element_by_id("fineui_8-inputEl-icon")
            # classStatus = breakfastCheckBox.get_attribute("class")
            # if "f-checked" not in classStatus: breakfastCheckBox.click()
            # lunchCheckBox = self.__browser.find_element_by_id("fineui_9-inputEl-icon")
            # classStatus = lunchCheckBox.get_attribute("class")
            # if "f-checked" not in classStatus: lunchCheckBox.click()
            # dinnerCheckBox = self.__browser.find_element_by_id("fineui_10-inputEl-icon")
            # classStatus = dinnerCheckBox.get_attribute("class")
            # if "f-checked" not in classStatus: dinnerCheckBox.click()
            submitButton = self.__browser.find_element_by_id("p1_ctl00_btnSubmit")
            submitButton.click()
            self.__browser.implicitly_wait(1)
            submitConfirmButton = self.__browser.find_element_by_id("fineui_33")
            submitConfirmButton.click()
            self.__browser.implicitly_wait(1)
            returnMessage = self.__browser.find_element_by_class_name("f-messagebox-message").text
        except Exception as e:
            print(e)
            return 0
        else:
            return 1 if returnMessage == "提交成功" else 0
        # TODO handle error


    def checkHistory(self):
        self.__browser.get(self.historyURL)
        records = self.__browser.find_element_by_class_name("f-datalist-list").text.split("\n")
        unfinishedRecord = [(item[:10], item[10:12]) for item in records if "未填报" in item]
        return unfinishedRecord if unfinishedRecord else None

    def reportUnfinished(self):
        unfinishedRecord = self.checkHistory()
        if unfinishedRecord == None:
            print("None")
            return None
        for item in unfinishedRecord:
            if item[0] == self.date and item[1] != self.timeMark:
                continue
            self.submitData(item[0], item[1])
            print(item)
        return str(unfinishedRecord)

    def report(self):
        self.__invokeBrowser()
        self.login()
        self.reportUnfinished()
        self.__delBrowser()

if __name__ == "__main__":
    flow = AutoReport(id=sys.argv[1], password=sys.argv[2], temperature=sys.argv[3])
    flow.report()