import sys
import time
from selenium import webdriver

class AutoReport(object):

    loginURL = "https://newsso.shu.edu.cn/login"
    reportURL = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=%s"
    historyURL = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport_History.aspx"
    historyReportURL = "https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?day=%s&t=%s"
    timeMarkDict = {"晨报": 1, "晚报": 2}

    def __init__(self, username="", password="", timeMark="", temperature="36.2"):
        self.browser = webdriver.Chrome("./chromedriver")
        self.id = username
        self.password = password
        self.timeMark = self.timeMarkDict[timeMark]
        self.temperature = temperature

    def longin(self):
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

    def checkHistory(self):
        self.browser.get(self.historyURL)
        records = self.browser.find_element_by_class_name("f-datalist-list").text.split("\n")
        unfinished = [item for item in records if "未填报" in item]
        for item in unfinished:
            self.submitData(self.historyReportURL%(item[:10], self.timeMarkDict[item[10:12]]))
        return str(unfinished) if unfinished else "None unfinised report"

    def __del__(self):
        self.browser.close()
        self.browser.quit()

if __name__ == "__main__":
    flow = AutoReport(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    flow.longin()
    # flow.submitData()
    flow.checkHistory()