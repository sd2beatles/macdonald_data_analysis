from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sys
import re
import time
from joblib import Memory
memory=Memory(location='cache/',verbose=1)

url='https://www.mcdonalds.co.kr/kor/store/main.do'

def get_details(soup,results):
    details_add=soup.select('tbody > tr')
    for detail in details_add:
        info={'add':None,'24시간':0,'맥드라이브':0,'맥딜리버리':0,'맥모닝':0,'주차':0,'디카페':0}
        if detail.find('dd',class_='road'):
            info['add']=detail.find('dd',class_='road').text
        services=list()
        for label in detail.select('label > span > img'):
            span=re.search('alt="\w+"?',str(label)).span()
            info[str(label)[span[0]+5:span[1]-1]]=1
        results.append(list(info.values()))
    return results


def getRawdata(url):
    driver=webdriver.Chrome(r'C:\Users\user\Downloads\chromedriver_win32\chromedriver.exe')
    driver.get(url)
    
    #time.sleep(5)
    search_button='#searchForm > div > fieldset > div > button'
    
    #search button clicked
    driver.find_element_by_css_selector(search_button).click()
    
    results=list()
    j=0
    for i in range(1,83):
        j+=1
        current_page_button=f'#container > div.content > div.contArea > div > div > div.mcStore > div > span > a:nth-child({j})'
        driver.find_element_by_css_selector(current_page_button).click()
        html=driver.page_source
        soup=BeautifulSoup(html,'html.parser')
        results=get_details(soup,results)
        if i in [i*10 for i in range(1,9)]:
            j=0
            next_arrow='#container > div.content > div.contArea > div > div > div.mcStore > div > a.arrow.next'
            driver.find_element_by_css_selector(next_arrow).click()
            
    results=pd.DataFrame(results,columns=['Address','24-hours','Mac_Drive','Mac_Delivery','Mac_Morning','Parking','Decaffe'])
    return results
 
