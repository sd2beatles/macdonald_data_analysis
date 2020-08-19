from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sys
import re
import time
from joblib import Memory
from selenium import webdriver
import urllib



def information_gathering(driver,results):
    source=driver.page_source
    soup=BeautifulSoup(source,'html.parser')
    shops=soup.select('tbody > tr > td > a')
    for x in shops[1::3]:
        results.append(x.text)
    return results
    
 
if __name__=='information_gathering':
    results=list()
    driver.find_element_by_css_selector('#Map > area:nth-child(1)').click()

    for page in range(1,16):
        if page%11==1:
            driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[2]/strong').click()
            results=information_gathering(driver,results)
        elif page%11==0:
            driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[2]/a[12]/img').click()
        else:
            page=page%11+1
            driver.find_element_by_xpath(f'//*[@id="contents"]/div[2]/div[2]/a[{page}]').click()
            results=information_gathering(driver,results)
