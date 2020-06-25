import sys
import time
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
        self.timeMark = 1 if time.strftime("%p", time.localtime())=="AM" else 2
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument("--disable-dev-shm-usage")
        self.browser = webdriver.Chrome("./chromedriver", chrome_options=option)

    def login(self):
        self.browser.get(self.loginURL)
        idBlock = self.browser.find_element_by_id("username")
        idBlock.send_keys(self.id)
        passwordBlock = self.browser.find_element_by_id("password")
        passwordBlock.send_keys(self.password)
        button = self.browser.find_element_by_id("login-submit")
        button.click()

    def submitData(self, URL):
        self.browser.get(URL)
        undertakeCheckBox = self.browser.find_element_by_id("p1_ChengNuo-inputEl-icon")
        classStatus = undertakeCheckBox.get_attribute("class")
        if "f-checked" not in classStatus: undertakeCheckBox.click()
        temperature = self.browser.find_element_by_id("p1_TiWen-inputEl")
        temperature.send_keys(self.temperature)
        QRCodeColorRadiusButton = self.browser.find_element_by_id("fineui_7-inputEl-icon")
        QRCodeColorRadiusButton.click()
        breakfastCheckBox = self.browser.find_element_by_id("fineui_8-inputEl-icon")
        classStatus = breakfastCheckBox.get_attribute("class")
        if "f-checked" not in classStatus: breakfastCheckBox.click()
        lunchCheckBox = self.browser.find_element_by_id("fineui_9-inputEl-icon")
        classStatus = lunchCheckBox.get_attribute("class")
        if "f-checked" not in classStatus: lunchCheckBox.click()
        dinnerCheckBox = self.browser.find_element_by_id("fineui_10-inputEl-icon")
        classStatus = dinnerCheckBox.get_attribute("class")
        if "f-checked" not in classStatus: dinnerCheckBox.click()
        submitButton = self.browser.find_element_by_id("p1_ctl00_btnSubmit")
        submitButton.click()
        submitConfirmButton = self.browser.find_element_by_id("fineui_14")
        submitConfirmButton.click()
        returnMessage = self.browser.find_element_by_id("f-messagebox-message").text.strip()
        return 1 if returnMessage=="提交成功" else 0

    def checkHistory(self):
        self.browser.get(self.historyURL)
        records = self.browser.find_element_by_class_name("f-datalist-list").text.split("\n")
        unfinished = [item for item in records if "未填报" in item]
        return unfinished if unfinished else None

    def reportUnfinished(self):
        unfinished = self.checkHistory()
        if unfinished == None:
            return None
        for item in unfinished:
            self.submitData(self.historyReportURL%(item[:10], self.timeMarkDict[item[10:12]]))
        return str(unfinished)

    def __del__(self):
        self.browser.close()
        self.browser.quit()

if __name__ == "__main__":
    flow = AutoReport(id=sys.argv[1], password=sys.argv[2], temperature=sys.argv[3])
    flow.login()
    # flow.submitData()
    flow.checkHistory()