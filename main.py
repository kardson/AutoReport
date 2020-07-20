import sys, time
from selenium import webdriver

class AutoReport(object):

    loginURL = "https://newsso.shu.edu.cn/login"
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


    def __invokeBrowser(self):
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument("--disable-gpu")
        option.add_argument("--disable-dev-shm-usage")
        self.__browser = webdriver.Chrome("./chromedriver", options=option)
        return 1

    def __delBrowser(self):
        self.__browser.close()
        self.__browser.quit()
        
    # TODO handle the situation of wrong id or password
    def login(self):
        self.__browser.get(self.loginURL)
        self.__browser.implicitly_wait(1)
        idBlock = self.__browser.find_element_by_id("username")
        idBlock.send_keys(self.id)
        passwordBlock = self.__browser.find_element_by_id("password")
        passwordBlock.send_keys(self.password)
        button = self.__browser.find_element_by_id("login-submit")
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
            undertakeCheckBox = self.__browser.find_element_by_id("p1_ChengNuo-inputEl-icon")
            classStatus = undertakeCheckBox.get_attribute("class")
            if "f-checked" not in classStatus: undertakeCheckBox.click()
            temperature = self.__browser.find_element_by_id("p1_TiWen-inputEl")
            temperature.send_keys(self.temperature)
            QRCodeColorRadiusButton = self.__browser.find_element_by_id("fineui_7-inputEl-icon")
            QRCodeColorRadiusButton.click()
            breakfastCheckBox = self.__browser.find_element_by_id("fineui_8-inputEl-icon")
            classStatus = breakfastCheckBox.get_attribute("class")
            if "f-checked" not in classStatus: breakfastCheckBox.click()
            lunchCheckBox = self.__browser.find_element_by_id("fineui_9-inputEl-icon")
            classStatus = lunchCheckBox.get_attribute("class")
            if "f-checked" not in classStatus: lunchCheckBox.click()
            dinnerCheckBox = self.__browser.find_element_by_id("fineui_10-inputEl-icon")
            classStatus = dinnerCheckBox.get_attribute("class")
            if "f-checked" not in classStatus: dinnerCheckBox.click()
            submitButton = self.__browser.find_element_by_id("p1_ctl00_btnSubmit")
            submitButton.click()
            self.__browser.implicitly_wait(1)
            submitConfirmButton = self.__browser.find_element_by_id("fineui_14")
            submitConfirmButton.click()
            self.__browser.implicitly_wait(1)
            returnMessage = self.__browser.find_element_by_class_name("f-messagebox-message")
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
            print(str(unfinishedRecord))
        return str(unfinishedRecord)

    def report(self):
        self.__invokeBrowser()
        self.login()
        self.reportUnfinished()
        self.__delBrowser()

if __name__ == "__main__":
    flow = AutoReport(id=sys.argv[1], password=sys.argv[2], temperature=sys.argv[3])
    flow.report()