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

    def getDataByStatus(self):
        if(len(self.df)==0):
            return pd.Series()

        a = self.df[self.df.estado != 'N/A'].groupby(['estado']).count()['id_de_caso']

        if a.index.contains('leve'):
            a.loc['Leve'] = a.loc['leve'] + a.loc['Leve']
            a= a.drop('leve')

        if a.index.contains('LEVE'):
            a.loc['Leve'] = a.loc['LEVE'] + a.loc['Leve']
            a = a.drop('LEVE')

        return a

    def getDataByAttention(self):
        a = self.df[self.df.atenci_n != 'N/A'].groupby(['atenci_n']).count()['id_de_caso']

        if a.index.contains('CASA'):
            a.loc['Casa'] = a.loc['CASA'] + a.loc['Casa']
            a= a.drop('CASA')

        if a.index.contains('casa'):
            a.loc['Casa'] = a.loc['casa'] + a.loc['Casa']
            a = a.drop('casa')

        return a

    def getDataByGenre(self):
        a = self.df[(self.df.sexo != 'N/A') & (self.df.sexo.isin(['f','m','F','M']))].groupby(['sexo']).count()['id_de_caso']

        if a.index.contains('f'):
            a.loc['F'] = a.loc['f'] + a.loc['F']
            a= a.drop('f')

        if a.index.contains('m'):
            a.loc['M'] = a.loc['m'] + a.loc['M']
            a = a.drop('m')

        return a

    def getDataByAge(self):
        a = self.df

        def strToInt(s):
            if(str(s).isnumeric()):
                return int(s)
            return -1

        a.edad = a.edad.map(lambda x: strToInt(x))

        out = {}
        columns = []
        index = []

        segments = [(x,x+10) for x in range(0,100,10)]
        for x1,x2 in segments:
            col = str(x1)+'-'+str(x2)
            rows = a[(a.edad >= x1) & (a.edad < x2)].groupby(['edad']).count()['id_de_caso']
            out[col] = sum(rows.values.tolist())
            columns.append(col)
            index.append(rows.index.tolist())

        return pd.Series(out)

    def plotStatus(self):
        if self.getDataByStatus().empty:
            return 'empty'
        self.getDataByStatus().plot.bar()
        plt.show()

    def plotAttention(self):
        if self.getDataByAttention().empty:
            return 'empty'
        self.getDataByAttention().plot.bar()
        plt.show()

    def plotGenre(self):
        if self.getDataByGenre().empty:
            return 'empty'
        self.getDataByGenre().plot.bar()
        plt.show()

    def plotAge(self):
        if self.getDataByAge().empty:
            return 'empty'
        self.getDataByAge().plot.bar()
        plt.show()


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
