
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
browser = webdriver.Chrome('chromedriver.exe')
import time
browser.get("https://gains.trade/trading#BTC-USD")
time.sleep(1)
import pprint
continue_button = browser.find_element(By.XPATH,"/html/body/div/div/div[3]/div/div/div/button/span")
# switch to the pop-up window
# browser.switch_to.window(browser.window_handles[-1])

# locate and click the continue button by tag name


continue_button.click()
time.sleep(1)
price = browser.find_element(By.XPATH,"/html/body/div/div/div[2]/div/section/section[1]/div[1]/div[1]/div[2]/div[1]/div/h4")
open_long=browser.find_element(By.XPATH,"/html/body/div/div/div[2]/div/section/section[1]/div[1]/div[1]/div[2]/div[2]/div/div[1]/span"),
open_short=browser.find_element(By.XPATH,"/html/body/div/div/div[2]/div/section/section[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/span"),
funding_long=browser.find_element(By.XPATH,"/html/body/div/div/div[2]/div/section/section[1]/div[1]/div[1]/div[2]/div[2]/div/div[3]/span"),
funding_short=browser.find_element(By.XPATH,"/html/body/div/div/div[2]/div/section/section[1]/div[1]/div[1]/div[2]/div[2]/div/div[4]/span"),
rollover=browser.find_element(By.XPATH,"/html/body/div/div/div[2]/div/section/section[1]/div[1]/div[1]/div[2]/div[2]/div/div[5]/span")


def parse_suffix(s):
    if not s[-1].isdigit():
        suffix=s[-1]
        if suffix=='M':
            s=s.replace('M','')
            return str(round(float(s)*1000000))
        elif suffix=='k':
            s=s.replace('k','')
            return str(round(float(s)*1000))
        else:
            return s    


result_dict={'type':'Btc',
'price':price.text,
'open_long':parse_suffix(open_long[0].text.split('/')[0].strip()),
'open_short':parse_suffix(open_short[0].text.split('/')[0].strip()),
'funding_long':funding_long[0].text.replace('%',''),
'funding_short':funding_short[0].text.replace('%',''),
'rollover':rollover.text.replace('%','')}
pprint.pprint(result_dict)



