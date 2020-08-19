from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sys
import re
import time
from joblib import Memory
from selenium import webdriver
import urllib



def detailed_info(driver,index,page):
    results={'gu':None,'store':None}
    index+=2
    driver.find_element_by_css_selector(f'#devCallShopList > div.bx_flex.bx_list > div.roundArea > table > tbody > tr:nth-child({index}) > td.first.num > a').click()
    source=driver.page_source
    soup=BeautifulSoup(source,'html.parser')
    soup.select('tbody > tr > td')
    print(soup)
    add=soup.find('td',class_='rt').text.strip()
    add=add.split(' ')
    results['gu']=add[1]
    results['store']=' '.join(add[2:])
    driver.back()
    time.sleep(1)
    initiator(driver,page)
    return results

def lists_store(driver,results,page):
    assert type(results)==list
    #repeat the sepcification of area
    source=driver.page_source
    soup=BeautifulSoup(source,'html.parser')
    list_no=len(soup.find_all('tr',class_='shopSearch'))
    for index in range(list_no):
        result=detailed_info(driver,index,page)
        results.append(result)
    return results

def initiator(driver,page):
    driver.find_element_by_css_selector('#content > div > div.bx_flex.bx_list_02.clfix > div.mapAreaWrap > ul > li:nth-child(1) > a > img').click()
    time.sleep(1)
    if page%11==1:
        driver.find_element_by_xpath('//*[@id="devCallShopList"]/div[2]/span/strong').click()
        time.sleep(1)
    elif page==0:
        driver.find_element_by_css_selector('#devCallShopList > div.paging_basic > span > a.go.next > img').click()
        time.sleep(1)
    else:
        page=page%11+1
        driver.find_element_by_xpath(f'//*[@id="devCallShopList"]/div[2]/span/a[{page}]').click()
        time.sleep(1)

def services(driver,merged_results):
    source=driver.page_source
    soup=BeautifulSoup(source,'html.parser')
    services=soup.select('td > ul')
    for service in services:
        service=service.find_all('img')
        service_results={'24시간':0,'와이파이':0,'D/T':0,'홈서비스':0,'단체주문':0,'리아오더':0}
        for info in service:
            info=re.search('alt="[\w]+"',str(info)).group()
            info=re.sub('[alt\="]','',info)
            if info in service_results:
                service_results[info]=1
    
        merged_results.append(service_results)  
    return merged_results
    

for page in range(1,22):
    results=results
    merged_results=merged_results
    initiator(driver,page) 
    merged_results=services(driver,merged_results)
    services_info.append(service_results)
    results=lists_store(driver,results,page)
    driver.find_element_by_css_selector('#navigation > ul > li:nth-child(3) > a > img').click()
  
lotteria=pd.read_csv('cache/lottery.csv')
lotteria=lotteria.iloc[:,1:]
columns=['gu','store','24-hours','wifi','d/t','delivery','volume orders','lia-order']
lotteria.columns=columns
lt_agg=lotteria.groupby('gu')['wifi'].count()
lt_agg=pd.DataFrame(lt_agg).reset_index()
lt_agg.columns=['gu','lt_no']
  
