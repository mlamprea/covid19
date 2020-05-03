import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

url="https://www.datos.gov.co/resource/gt2j-8ykr.json"
today = datetime.date.today().strftime("%Y-%m-%dT00:00:00.000")
params = {'$limit':8000,'fecha_reporte_web': today}
#params = {'$limit':8000}
#params = {'fecha_reporte_web': '2020-04-25T00:00:00.000'}
resp = requests.get(url,params)
#resp.content
data = resp.json()
len(data)
bogota = 'Bogotá D.C.'

df = pd.DataFrame(data)
df.columns

#Curve: Confirmed cases in all Country
df2 = df.sort_values('fecha_reporte_web').groupby(['fecha_reporte_web']).count()['id_de_caso']
df2.plot.barh()


a = pd.Series()
a.empty

df.groupby(['departamento']).count()['id_de_caso'].sort_values(ascending=False)

#Curve: Confirmed cases by department

def getDataByDept(dept):
    return pd.Series(np.cumsum(df[df.departamento==dept].sort_values('fecha_reporte_web').groupby(['fecha_reporte_web']).count()['id_de_caso'].values))

#Curve: Confirmed cases by plotByCity

def getDataByCity(city):
    return pd.Series(np.cumsum(df[df.ciudad_de_ubicaci_n==city].sort_values('fecha_reporte_web').groupby(['fecha_reporte_web']).count()['id_de_caso'].values))

def plotByDept(depts):
    for dept in depts:
        plt.plot(getDataByDept(dept),label=dept)
        plt.legend()
    plt.show()

def plotByCity(cities):
    for city in cities:
        plt.plot(getDataByCity(city),label=city)
        plt.legend()
    plt.show()

def plotByDepTopN(n):
    plotByDept(list(df.groupby('departamento').count()['id_de_caso'].sort_values(ascending=False).index)[0:n])

def plotByCityTopN(n):
    plotByCity(list(df.groupby('ciudad_de_ubicaci_n').count()['id_de_caso'].sort_values(ascending=False).index)[0:n])


depts = ['Cundinamarca','Boyacá','Antioquia',bogota]
plotByDept(depts)


#Growth rate bogota
x1  = np.exp(np.diff(np.log(getDataByDept(bogota))))
plt.plot(x1)

plotByCityTopN(5)
plotByDepTopN(5)

dfAtention = df.groupby(['atenci_n']).count()['id_de_caso']
dfAtention.plot.pie()

# Daily report
url="https://www.datos.gov.co/resource/gt2j-8ykr.json"
today = datetime.date.today().strftime("%Y-%m-%dT00:00:00.000")
params = {'$limit':1000,'fecha_reporte_web': today}
resp = requests.get(url,params)
#resp.content
data = resp.json()
len(data)
