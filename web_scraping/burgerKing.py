from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sys
import re
import time
from joblib import Memory
from selenium import webdriver
import urllib

def get_info(soup):
    shops=soup.select('div > ul > li > div')
    store_lists=list()
    for shop in shops:
        results={'gu':None,'store':None,'딜리버리':0,'킹오더':0,'아침메뉴':0,'주차가능':0,'24시간매장':0,'드라이브스루':0}
        add=shop.find('p',class_='addr').text
        gu=re.search('[\s]+[\w]+',add).group().strip()
        results['gu']=gu
        store=' '.join(add.split(' ')[2:])
        results['store']=store.strip()
        services=shop.find_all('span')
        for service in services:
            service=service.text
            if service in results:
                results[service]=1
        store_lists.append(results)
    return store_lists


if __name_=='get_info':
  url='https://www.burgerking.co.kr/#/store'

  driver=webdriver.Chrome(r'C:\Users\user\Downloads\chromedriver_win32\chromedriver.exe')
  driver.get(url)

  selectors=['#app > div > div.headerWrap > div > div > div.GNBWrap > ul > li:nth-child(2) > button',
             '#app > div > div.headerWrap > div > div > div.GNBWrap > ul > li:nth-child(2) > ul > li > a',
             '#app > div > div.contentsWrap > div.contentsBox01.nopadding > div > div.map_searchWrap > div.map_search_head > div.tab01 > ul > li:nth-child(3) > button',
             '#app > div > div.contentsWrap > div.contentsBox01.nopadding > div > div.map_searchWrap > div.map_search_head > div.searchWrap > div:nth-child(5) > div > select:nth-child(1)',
             '#app > div > div.contentsWrap > div.contentsBox01.nopadding > div > div.map_searchWrap > div.map_search_head > div.searchWrap > div:nth-child(5) > div > select:nth-child(1) > option:nth-child(2)']

  for index,selector in enumerate(selectors):
      if index==3:
          time.sleep(5)
      driver.find_element_by_css_selector(selector).click()
  source=driver.page_source
  soup=BeautifulSoup(source,'html.parser')
  store_lists=get_info(soup)
  store_lists=pd.DataFrame(store_lists)
  store_lists.columns=['gu','Store','Delivery','KingOrder','Morning','Parking','24-hours','Drive-Through']
  
  
