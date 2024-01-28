from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import re
import datetime
import os

class CovidSearch(object):
    def __init__(self):
        self.sticker = ""
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        chrome_path = r"C:\Users\vchsi\Documents\python_sublime\webscraper\chromedriver.exe"
        self.driver = webdriver.Chrome(options=options, executable_path=chrome_path)

    def findSite(self, sticker):
        sticker = sticker.replace("+","")
        self.driver.implicitly_wait(30)
        self.sticker = sticker
        if self.fileAlreadySaved(sticker):
#            print("read from file")
            self.getSites()
        else:
            print("read from web")
            self.driver.get('https://maps.google.com/maps?q={}+nearby+COVID+vaccine+centers'.format(sticker))
            self.saveWebPageToFile(sticker)

    def getSites(self):
        reader = open(self.sticker +".html", 'r')
        txt = "".join(reader.readlines())
        dictionary = {}
        search_str = "Get directions to"
        search_str2 = 'class="section-result-location" jsan="7.section-result-location">'
        txt2 = "".join(list(txt))
        last_ind = 0
        li = []
        li2 = []
        cur = ""
#        print(txt.count(search_str))
        for i in range((txt.count(search_str))):
            ind = txt.find(search_str)
            ptr = ind + 17
            while (txt[ptr] != '"'):
                cur += txt[ptr]
                ptr += 1
            li.append(cur)
            cur = ""
            txt = txt[ind + 17:]
 #       print(txt.count(search_str))

        for k in range((txt2.count(search_str2))):
            ind = txt2.find(search_str2)
#            print(ind - txt2.find(search_str))
            ptr = ind + len(search_str2)
            while (txt2[ptr] != '<'):
                cur += txt2[ptr]
                ptr += 1
            li2.append(cur)
            cur = ""
            txt2 = txt2[ind + len(search_str2):]
        for l in range(len(li2)):
            dictionary[li2[l]] = li[l]
            print(li2[l], " | ", dictionary[li2[l]])
        return dictionary

    def fileAlreadySaved(self, sticker):
        files = os.listdir()
        for file in files:
            if file == sticker+".html":
                return True
        return False

    def saveWebPageToFile(self, sticker):
        file_name = sticker + ".html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

    def closeDriver(self):
        self.driver.close()

# Run functions above:
user_location = "New York".replace(" ","+")
se = CovidSearch()
se.findSite(user_location)
se.getSites()
se.closeDriver()
