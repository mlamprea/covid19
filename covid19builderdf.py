import pandas as pd
import datetime
import requests
import covid19py

class Covid19Builder:
    def __init__(self):
        self.url="https://www.datos.gov.co/resource/gt2j-8ykr.json"
        
    #Deprecated replaced by buildByDate functions
    def buildDailyDF(self,limit=10000):
        today = datetime.date.today().strftime("%Y-%m-%dT00:00:00.000")
        params = {'$limit':limit,'fecha_reporte_web': today}
        resp = requests.get(self.url,params)
        #resp.contentn()))
        return covid19py.Covid19PYSD(pd.DataFrame(resp.json()))

    def buildTotalDF(self,limit=10000):
        params = {'$limit':limit}
        resp = requests.get(self.url,params)
        return covid19py.Covid19PYMD(pd.DataFrame(resp.json()))

    # Params: date with format %Y-%m-%d
    # By default date is today
    def buildByDate(self,date='',limit=10000):
        try:
            if not date:
                date = datetime.date.today().strftime("%Y-%m-%dT00:00:00.000")
            else:
                datetime.datetime.strptime(date,'%Y-%m-%d')
                date = datetime.date.today().strftime(date+"T00:00:00.000")

            params = {'$limit':limit,'fecha_reporte_web': date}
            resp = requests.get(self.url,params)
            #resp.contentn()))
            return covid19py.Covid19PYSD(pd.DataFrame(resp.json()))

        except ValueError as ve:
            print(ve)
            return None
