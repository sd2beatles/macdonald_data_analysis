import requests
from functools import reduce

class getData(object):
    def __init__(self,key):
        self.key=key
    def get_seoul_data(self):
        url=f'http://openapi.seoul.go.kr:8088/{key}/json/SdeTlSccoSigW/1/25/'
        results=requests.get(url).json()
        results=pd.DataFrame(results['SdeTlSccoSigW']['row'])
        results.drop(['OBJECTID','ESRI_PK'],axis=1,inplace=True)
        results.columns=['code','gu_kor','gu_eng','lat','lag']
        return results
    
    def get_population_data(self):
        url=f'http://openapi.seoul.go.kr:8088/{self.key}/json/octastatapi419/1/26/'
        results=requests.get(url)
        results=pd.DataFrame(results.json()['octastatapi419']['row'])
        #Select the relevant information
        results=results.loc[1:,['JACHIGU','GYE_1']]
        results.columns=['gu_kor','registered_pop']
        return results
    
    def get_business_data(self):
        url=f'http://openapi.seoul.go.kr:8088/{self.key}/json/octastatapi104/1/450/'
        results=requests.get(url)
        results=pd.DataFrame(results.json()['octastatapi104']['row'])
        results=results.loc[1:,['JACHIGU','GYE','SAEOPCHESU_1']]
        results.columns=['gu_kor','working_pop','business_no']
        #convert the data types of the chosen columns into float
        results=results.astype({'working_pop':float,'business_no':float})
        results=results.groupby(['gu_kor'])['working_pop','business_no'].sum()
        results=results.reset_index()
        return results
    
    def merged_data(self):
        seoul_data=self.get_seoul_data()
        pop_data=self.get_population_data()
        business_data=self.get_business_data()
        df=[seoul_data,pop_data,business_data]
        df=reduce(lambda left,right:pd.merge(left,right,on='gu_kor',how='left'),df)
        return df
 
key='replace here'
seoul_merged=getData(key).merged_data()
