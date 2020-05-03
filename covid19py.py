import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Covid19PY(object):

    def __init__(self, df):
        self.df = df
        self.bogota = 'Bogotá D.C.'

    #Curve: Confirmed cases by department
    def getDataByDept(self,dept):
        dfs = pd.Series(np.cumsum(self.df[self.df.departamento==dept].sort_values('fecha_reporte_web').groupby(['fecha_reporte_web']).count()['id_de_caso'].values))
        return dfs

    #Curve: Confirmed cases by plotByCity
    def getDataByCity(self,city):
        return pd.Series(np.cumsum(self.df[self.df.ciudad_de_ubicaci_n==city].sort_values('fecha_reporte_web').groupby(['fecha_reporte_web']).count()['id_de_caso'].values))


#MD: Multiple Days
class Covid19PYMD(Covid19PY):

#Curve: all confirmed cases in Colombia
    def getAllData(self):
        return pd.Series(np.cumsum(self.df.sort_values('fecha_reporte_web').groupby(['fecha_reporte_web']).count()['id_de_caso'].values))

    def plotAll(self):
        plt.plot(self.getAllData(),label="General")
        plt.legend()
        plt.show()

    def plotByDept(self,depts):
        for dept in depts:
            plt.plot(self.getDataByDept(dept),label=dept)
            plt.legend()
        plt.show()

    def plotByCity(self,cities):
        for city in cities:
            plt.plot(self.getDataByCity(city),label=city)
            plt.legend()
        plt.show()

    def plotByDeptTopN(self,n):
        self.plotByDept(list(self.df.groupby('departamento').count()['id_de_caso'].sort_values(ascending=False).index)[0:n])

    def plotByCityTopN(self,n):
        self.plotByCity(list(self.df.groupby('ciudad_de_ubicaci_n').count()['id_de_caso'].sort_values(ascending=False).index)[0:n])

    #Growth rate by department
    def plotGrowthRateByDept(self,dept):
        x1  = np.exp(np.diff(np.log(self.getDataByDept(dept))))
        plt.plot(x1)

    def plotGrowthRate(self):
        x1  = np.exp(np.diff(np.log(self.getDataAll())))
        plt.plot(x1)

#SD: Single Day
class Covid19PYSD(Covid19PY):

    def getDataDepts(self,top=30):
        if(len(self.df)==0):
            return pd.Series()
        return self.df.groupby(['departamento']).count()['id_de_caso'].sort_values(ascending=True).tail(top)

    def plotDepts(self,top=30):
        if(self.getDataDepts(top).empty):
            return 'empty'
        self.getDataDepts(top).plot.barh()
#        for index, value in enumerate(self.getDataDepts(top)):
#            plt.text(value, index, str(value))
        plt.show()

    def getDataCities(self,top=30):
        if(len(self.df)==0):
            return pd.Series()
        return self.df.groupby(['ciudad_de_ubicaci_n']).count()['id_de_caso'].sort_values(ascending=True).tail(top)

    def plotCities(self,top=30):
        if(self.getDataCities(top).empty):
            return 'empty'
        self.getDataCities(top).plot.barh()
#        for index, value in enumerate(self.getDataCities(top)):
#            plt.text(value, index, str(value))
        plt.show()
