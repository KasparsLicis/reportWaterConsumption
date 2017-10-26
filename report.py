#
# pip install selenium
# install firefox driver


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from datetime import datetime

###
# 
# configuration part
#username and password to the portal. Meter numbers

user = 'yourUsername'
psw = 'yourPassword'
meter = ['meter1','meter2','meter3', 'meter4']

#value storage for debugging
listFromBrowser = []
listSubmitted = []

# in case visual browser is not needed
# install 
# browser = webdriver.PhantomJS()
# screenshot can be taken by driver.save_screenshot('screen.png')
browser = webdriver.Firefox()
try:
    browser.get("https://e-parvaldnieks.lv/")
except:
    sys.exit('Cannot open web page')

browser.find_element_by_id("login_login").send_keys(user)
browser.find_element_by_id("login_password").send_keys(psw)
browser.find_element_by_css_selector("button.simple").click()

browser.get("https://e-parvaldnieks.lv/meters")

###
# if  data are needed to be edited 
#browser.find_element_by_class_name('js_meters_data_edit.toggle').click()

#if value is in <> then get_attribute("value") if just text then text

for id in meter:
    try:
        valueFromBrowser = browser.find_element_by_xpath('//*[@id="meter_%s"]/span[1]' % (id)).text.encode('utf-8') 
    except:
        sys.exit('Cannot open web page')
    #split string, take first part, convert to number and add 1 as new consumption         
    valueToFill = int(valueFromBrowser.split(',')[0])+1
    #only for debugging
    listFromBrowser.append(valueFromBrowser)
    listSubmitted.append(valueToFill)

    fillValue1 = browser.find_element_by_xpath('//*[@id="meter_%s"]/input[1]' % (id))
    fillValue2 = browser.find_element_by_xpath('//*[@id="meter_%s"]/input[2]' % (id))
    fillValue3 = browser.find_element_by_xpath('//*[@id="meter_%s"]/input[3]' % (id))
    fillValue4 = browser.find_element_by_xpath('//*[@id="meter_%s"]/input[4]' % (id))
    fillValue5 = browser.find_element_by_xpath('//*[@id="meter_%s"]/input[5]' % (id))

    if 1000 <= valueToFill <= 9999:
        fillValue2.send_keys(map(int, str(valueToFill))[0])
        fillValue3.send_keys(map(int, str(valueToFill))[1])
        fillValue4.send_keys(map(int, str(valueToFill))[2])
        fillValue5.send_keys(map(int, str(valueToFill))[3])
    
    if 100 <= valueToFill <= 999:
        fillValue3.send_keys(map(int, str(valueToFill))[0])
        fillValue4.send_keys(map(int, str(valueToFill))[1])
        fillValue5.send_keys(map(int, str(valueToFill))[2])

    if 10 <= valueToFill <=99:
        fillValue4.send_keys(map(int, str(valueToFill))[0])
        fillValue5.send_keys(map(int, str(valueToFill))[1])

    if 0 <= valueToFill <=9:
        fillValue5.send_keys(map(int, str(valueToFill))[0])

with open('/tmp/meter.log', 'a') as file:
    file.write(str(datetime.now()) + ':' + str(listFromBrowser) + ':' + str(listSubmitted) + '\n')   

#for debugging
print (listFromBrowser)
print (listSubmitted)

browser.find_element_by_css_selector("button.button-light.button-small").click()
browser.close()
